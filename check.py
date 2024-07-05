import os
import sys
import time

if len(sys.argv) != 2:
    print("Usage: python check.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
time.sleep(2)

while True:
    try:
        last_modified = os.path.getmtime(filename)
        current_time = time.time()

        if current_time - last_modified > 10 * 60:
            print("q")
            break
        else:
            time.sleep(10 * 60)
    except FileNotFoundError:
        print(f"FATAL ERROR: The file '{filename}' was not found.", file=sys.stderr)
        sys.exit(1)
