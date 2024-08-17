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
        if k.startswith("earliestfile"):
            path = k.split("_", 1)[-1]
            try:
                d[k] = min(
                    (
                        path + "/" + f
                        for f in os.listdir(path)
                        if os.path.isfile(path + "/" + f)
                    ),
                    key=lambda x: os.path.getmtime(x),
                )
            except ValueError:
                d[k] = None
            d[k] = (
                dt.datetime.fromtimestamp(os.path.getmtime(d[k])).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if d[k]
                else None
            )
            d["time"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
    sys.stdout.flush()
