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
# Version 0.2: Removes use of threads
# --------------------------------------------------------------------------------

# Todo:
# - Replace the threads design by piping the pipelines together with a binary
#   that will keep the stdin buffer drained so that the stdout of an upstream
#   process will not stop waiting with a full buffer. Or one that prevents a
#   start until the stdin is closed from the upstream binary, like for timing
#   IO like pulling from the same drive.

import json
import os
import subprocess
import sys
from typing import List

__version__ = 0.2

Command = List[str]
CommandPipeline = List[Command]
Service = List[CommandPipeline]


if len(sys.argv) != 2 and len(sys.argv) != 3:  # debug is optional
    print(
        "Usage: python service_manager.py <config_filepath> [-d]\n  config_filepath     Path for config file for service. Default: service.cfg"
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
    if not line or line.split()[0] == "#":
        pass
    elif line.split()[0] == "##":
        if command:
            command_pipeline.append(command)
        if command_pipeline:
            service.append(command_pipeline)
        command = []
        command_pipeline = []
    elif line.split()[0] == "###":
        if command:
            command_pipeline.append(command)
        command = []
    else:
        command.append(line)

if command:
    command_pipeline.append(command)
if command_pipeline:
    service.append(command_pipeline)

debug = True if "-d" in sys.argv else False
(
    print(f"[DEBUG] starting {json.dumps(service, indent=4)}", file=sys.stderr)
    if debug
    else None
)
not_stopping = True

for command_pipeline in service:
    command_pipeline.append([])
    command_pipeline.append(0)

while not_stopping:
    try:
        for command_pipeline in service:
            # Check if any are waitable, dead
            if command_pipeline[-2]:
                for p in command_pipeline[-2]:
                    try:
                        p.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        pass
            # Has started but one or more bin is waited
            if command_pipeline[-2] and list(
                filter(lambda x: x.returncode, command_pipeline[-2])
            ):
                for p in command_pipeline[-2]:
                    # Time to kill
                    if p.returncode is None and os.name == "nt":
                        subprocess.run(["taskkill", "/F", "/PID", str(p.pid)])
                    if p.returncode is None and os.name != "nt":
                        p.kill()
                    if p.returncode is None:
                        try:
                            p.wait(timeout=15)
                        except subprocess.TimeoutExpired:
                            print(
                                f"[FATAL] We should be waiting a killed process but it's hung. Crash.\n{p=}",
                                file=sys.stderr,
                            )
                            sys.exit(1)
                # Reset to not started
                command_pipeline[-2] = []
                command_pipeline[-1] = 0
            # Start the unstarted
            if command_pipeline[-1] is not False:  # False means started
                print(f"[INFO] starting {command_pipeline=}", file=sys.stderr)
                for i, command in enumerate(list(command_pipeline[:-2])):
                    p = subprocess.Popen(
                        command,
                        stdin=p0.stdout if i != 0 else None,
                        stdout=(
                            subprocess.PIPE if i + 1 != len(command_pipeline) else None
                        ),
                    )
                    command_pipeline[-2].append(p)
                    if i != 0:
                        p0.stdout.close()
                    p0 = p
                    if i + 1 == len(command_pipeline) - 2:
                        command_pipeline[-1] = False
    except BaseException as e:
        print(f"[WARN] Unhandled exception {e!r}. Closing.", file=sys.stderr)
        not_stopping = False
        break


print("[INFO] All processes have been stopped.", file=sys.stderr)
