import datetime as dt
import json
import subprocess
import sys

while True:
    line = sys.stdin.buffer.readline()
    if not line.strip():
        break
    d = json.loads(line.decode("utf-8"))
    for k in list(d):
        if k.startswith("ping"):
            ip = k.split("_")[-1]
            p = subprocess.run(
                ["ping", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            d[k] = (
                "reachable"
                if p.returncode == 0 and b"unreachable" not in p.stdout
                else "unreachable"
            )
            d["time"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
    sys.stdout.flush()
