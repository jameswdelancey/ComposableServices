import os
import signal
import subprocess
import sys
import threading
import time

running = True


def signal_handler(sig, frame):
    global running
    print("INFO: Signal Received. Stopping threads...")
    running = False


signal.signal(signal.SIGINT, signal_handler)


def run_commands(command_group):
    global running
    while running:  # Restarts unless fast restarts
        start = time.time()
        try:
            for i, command in enumerate(command_group):
                if i == 0:
                    processes = [
                        subprocess.Popen(command_group[0], stdout=subprocess.PIPE)
                    ]
                elif i != len(command_group) - 1:
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
                    ), f"Return code of {command_group[-1]} is not 0"
                except subprocess.TimeoutExpired:
                    pass
        except Exception as e:
            if time.time() - start < 1 * 60:
                print(f"FATAL ERROR: {e!r}", file=sys.stderr)
                break
            print(f"NON FATAL ERROR: {e}", file=sys.stderr)
    running = False


for i in range(8):
    try:
        os.mkdir(f"D:/ts_cam{i}")
    except FileExistsError:
        pass
    f2 = open(f"D:/ts_cam{i}_touch.txt", "w")
    f2.write("")
    f2.close()

commands = [
    [
        # ["python", "check.py", "D:/ts_cam0_touch.txt"],
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            "rtsp://admin:admin@10.0.0.242:554/11",
            "-y",
            "-c",
            "copy",
            "-f",
            "mpegts",
            "pipe:1",
        ],
        [
            "python",
            "split.py",
            "D:/ts_cam0",
            "%Y-%m-%d_%H-%M.ts",
            "D:/ts_cam0_touch.txt",
        ],
    ],
    [
        # ["python", "check.py", "D:/ts_cam1_touch.txt"],
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            "rtsp://admin:admin@10.0.0.243:554/11",
            "-y",
            "-c",
            "copy",
            "-f",
            "mpegts",
            "pipe:1",
        ],
        [
            "python",
            "split.py",
            "D:/ts_cam1",
            "%Y-%m-%d_%H-%M.ts",
            "D:/ts_cam1_touch.txt",
        ],
    ],
    [
        # ["python", "check.py", "D:/ts_cam2_touch.txt"],
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            "rtsp://admin:admin@10.0.0.244:554/11",
            "-y",
            "-c",
            "copy",
            "-f",
            "mpegts",
            "pipe:1",
        ],
        [
            "python",
            "split.py",
            "D:/ts_cam2",
            "%Y-%m-%d_%H-%M.ts",
            "D:/ts_cam2_touch.txt",
        ],
    ],
    [
        # ["python", "check.py", "D:/ts_cam3_touch.txt"],
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            "rtsp://admin:admin@10.0.0.245:554/11",
            "-y",
            "-c",
            "copy",
            "-f",
            "mpegts",
            "pipe:1",
        ],
        [
            "python",
            "split.py",
            "D:/ts_cam3",
            "%Y-%m-%d_%H-%M.ts",
            "D:/ts_cam3_touch.txt",
        ],
    ],
    [
        # ["python", "check.py", "D:/ts_cam4_touch.txt"],
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            "rtsp://admin:admin@10.0.0.246:554/11",
            "-y",
            "-c",
            "copy",
            "-f",
            "mpegts",
            "pipe:1",
        ],
        [
            "python",
            "split.py",
            "D:/ts_cam4",
            "%Y-%m-%d_%H-%M.ts",
            "D:/ts_cam4_touch.txt",
        ],
    ],
    [
        # ["python", "check.py", "D:/ts_cam5_touch.txt"],
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            "rtsp://admin:1234asdf@10.0.0.240:554/cam/realmonitor?channel=1&subtype=0",
            "-y",
            "-c",
            "copy",
            "-f",
            "mpegts",
            "pipe:1",
        ],
        [
            "python",
            "split.py",
            "D:/ts_cam5",
            "%Y-%m-%d_%H-%M.ts",
            "D:/ts_cam5_touch.txt",
        ],
    ],
    [
        # ["python", "check.py", "D:/ts_cam6_touch.txt"],
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            "rtsp://admin:1234asdf@10.0.0.241:554/cam/realmonitor?channel=1&subtype=0",
            "-y",
            "-c",
            "copy",
            "-f",
            "mpegts",
            "pipe:1",
        ],
        [
            "python",
            "split.py",
            "D:/ts_cam6",
            "%Y-%m-%d_%H-%M.ts",
            "D:/ts_cam6_touch.txt",
        ],
    ],
    [
        # ["python", "check.py", "D:/ts_cam7_touch.txt"],
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            "rtsp://admin:1234asdf@10.0.0.247:554/cam/realmonitor?channel=1&subtype=0",
            "-y",
            "-c",
            "copy",
            "-f",
            "mpegts",
            "pipe:1",
        ],
        [
            "python",
            "split.py",
            "D:/ts_cam7",
            "%Y-%m-%d_%H-%M.ts",
            "D:/ts_cam7_touch.txt",
        ],
    ],
    [
        ["python", "delete.py"],
        # ["ffmpeg", "-loglevel", "quiet", "-i", "rtsp://admin:admin@10.0.0.242:554/11", "-y", "-c", "copy", "-f", "mpegts", "pipe:1"],
        # ["python", "split.py", "D:/ts_cam8", "%Y-%m-%d_%H-%M.ts", "D:/ts_cam8_touch.txt"],
    ],
]

threads = []
for command_group in commands:
    thread = threading.Thread(target=run_commands, args=(command_group,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("INFO: All threads have been stopped.", file=sys.stderr)
