import sys
import json

headers = sys.stdin.buffer.readline().decode("utf-8").rstrip("\r\n").split("\t")

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    values = line.decode("utf-8").rstrip("\r\n").split("\t")
    item = dict(zip(headers, values))
    sys.stdout.buffer.write(json.dumps(item).encode("utf-8") + b"\n")
