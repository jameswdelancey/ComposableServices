# Origionally I thought that if this closed, it would close the rest of the pipe, but not so
# at least in Windows. I need to find a way to not rely on ffmpeg taking the 'q' through stdin
# as that has lead to the pipeline getting stuck open without another watchdog.
import os
import sys
import time

if len(sys.argv) != 2:
    print("Usage: python check.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
OLD_FILE_MAX_TIME = 20 * 60  # 20 min
time.sleep(OLD_FILE_MAX_TIME)

while True:
    try:
        last_modified = os.path.getmtime(filename)
        current_time = time.time()

        if current_time - last_modified > OLD_FILE_MAX_TIME:
            print(
                f"WARN: Max time exceeded. Sending 'q' to quit ffmpeg.", file=sys.stderr
            )
            print("q")
            sys.stdout.flush()
            sys.exit(0)
        else:
            time.sleep(OLD_FILE_MAX_TIME)
    except FileNotFoundError:
        print(f"FATAL ERROR: The file '{filename}' was not found.", file=sys.stderr)
        sys.exit(1)
