import json
import sys


while True:
    acc = []
    while True:
        chunk = sys.stdin.buffer.readline()
        if not chunk:
            break
        acc.append(chunk)
        if chunk.rstrip() == b"}":
            break
    if not chunk:
        break
    d = json.loads(b"".join(acc).decode("utf-8"))

    o = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(o + b"\n")
