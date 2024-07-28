import datetime as dt
import json
import os
import sys

while True:
    line = sys.stdin.buffer.readline()
    if not line.strip():
        break
    d = json.loads(line.decode("utf-8"))
    for k in list(d):
        if k.startswith("numbytes"):
            path = k.split("_", 1)[-1]
            try:
                d[k] = sum(
                    os.path.getsize(os.path.join(dirpath, filename))
                    for dirpath, dirnames, filenames in os.walk(path)
                    for filename in filenames
                )
            except ValueError:
                d[k] = None
            d[k] = str(d[k])
            d["time"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
    sys.stdout.flush()
