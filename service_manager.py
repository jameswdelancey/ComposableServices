# --------------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2024 James Delancey.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------------------
#
# Title: Service Manager
# Description: Manages concurrent command pipelines, allowing for commands to be
# started in a pipeline where the stdout of a command is piped to the stdin of the
# following command in the pipeline. A service comprises several of these command
# pipelines running concurrently.
#
# Author: James Delancey.
# Date: 2024-07-05
# --------------------------------------------------------------------------------

# Todo:
# - Replace the threads design by piping the pipelines together with a binary
#   that will keep the stdin buffer drained so that the stdout of an upstream
#   process will not stop waiting with a full buffer. Or one that prevents a
#   start until the stdin is closed from the upstream binary, like for timing
#   IO like pulling from the same drive.

import os
import signal
import subprocess
import sys
import threading
import time
from types import FrameType
from typing import List, Optional, TypeVar

__version__ = 0.1

Command = List[str]
CommandPipeline = List[Command]
Service = List[CommandPipeline]

running: bool = True


def signal_handler(sig: int, frame: Optional[FrameType]) -> None:
    global running
    print("INFO: Signal Received. Stopping threads...")
    running = False


signal.signal(signal.SIGINT, signal_handler)


def run_command_pipeline(command_pipeline: CommandPipeline) -> None:
    global running
    while running:  # Restarts unless fast restarts
        start = time.time()
        try:
            for i, command in enumerate(command_pipeline):
                if i == 0:
                    processes = [
                        subprocess.Popen(command_pipeline[0], stdout=subprocess.PIPE)
                    ]
                elif i != len(command_pipeline) - 1:
                    processes.append(
                        subprocess.Popen(
                            command, stdin=processes[-1].stdout, stdout=subprocess.PIPE
                        )
                    )
                else:
                    processes.append(
                        subprocess.Popen(command, stdin=processes[-1].stdout)
                    )
            while running:  # Wakes to check running between communicate
                try:
                    processes[-1].communicate(timeout=5)
                    assert (
                        processes[-1].returncode == 0
                    ), f"Return code of {command_pipeline[-1]} is not 0"
                except subprocess.TimeoutExpired:
                    pass
        except Exception as e:
            if time.time() - start < 1 * 60:
                print(f"FATAL ERROR: {e!r}", file=sys.stderr)
                break
            print(f"NON FATAL ERROR: {e}", file=sys.stderr)
    running = False


if len(sys.argv) != 2:
    print(
        "Usage: python service_manager.py <config_filepath>\n  config_filepath     Path for config file for service. Default: service.cfg"
    )
    sys.exit(1)

config_filepath = sys.argv[1]

with open(config_filepath) as f:
    config_text_lines = f.read().strip().splitlines()
config_text_lines = [line.strip() for line in config_text_lines]

command: Command = []
command_pipeline: CommandPipeline = []
service: Service = []

for line in config_text_lines:
    line = line.strip()
    if not line:
        continue
    if len(line) >= 3 and line[0:3] == "###":
        command_pipeline.append(command) if command else None
        command = []
        continue
    if len(line) >= 2 and line[0:2] == "##":
        service.append(command_pipeline) if command_pipeline else None
        command_pipeline = []
        continue
    if line[0] != "#":
        command.append(line)

command_pipeline.append(command) if command else None
service.append(command_pipeline) if command_pipeline else None

threads = []
for command_pipeline in service:
    thread = threading.Thread(target=run_command_pipeline, args=(command_pipeline,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("INFO: All threads have been stopped.", file=sys.stderr)
