import json
import os
import sys

first_line = True

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    d = json.loads(line.decode("utf-8"))
    path = d["s"+sys.argv[1]+"_local_path"] + "/" + d["b_path"]
    exists = bool(os.path.exists(path))
    if first_line:
        if not exists:
            print(
                "[FATAL ERROR] I assert we should match on the first file in exists.py",
                file=sys.stderr,
            )
        first_line = not first_line
    d["bs"+sys.argv[1]+"_sha256_error"] = "1" if not exists else "0"
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
