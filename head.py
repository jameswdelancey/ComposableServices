import sys

i = 0
while i < 10:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    sys.stdout.buffer.write(line)
    i += 1
