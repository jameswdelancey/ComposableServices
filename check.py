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
