import datetime as dt
import json
import socket
import sys

while True:
    line = sys.stdin.buffer.readline()
    if not line.strip():
        break
    d = json.loads(line.decode("utf-8"))
    for k in list(d):
        if k.startswith("rtspping"):
            ip = k.split("_")[-1]
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((ip, 554))
                if result == 0:
                    ret = "reachable"
                else:
                    ret = "unreachable"
                sock.close()
            except socket.error as err:
                ret = "unreachable"

            d[k] = ret
            d["time"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
    sys.stdout.flush()
