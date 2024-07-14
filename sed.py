import sys

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    line = line.replace(b'"D:/dot80/file_storage"', b'"F:/file_storage"')
    sys.stdout.buffer.write(line)
