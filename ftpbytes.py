import datetime as dt
import json
import shutil
import sys

while True:
    line = sys.stdin.buffer.readline()
    if not line.strip():
        break
    d = json.loads(line.decode("utf-8"))
    for k in list(d):
        if k.startswith("ftpbytes"):
            path = k.split("_")[-1]
            d[k] = shutil.disk_usage(path)
            d[k] = str(d[k][2] * 100 // d[k][0])
            d["time"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
    sys.stdout.flush()
