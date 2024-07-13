import datetime as dt
import json
import os
import sys
import shutil

# Assumes s2_local_path is set for the correct destination
# Assumes that chk for sha256 and par2 will subsequently run
# to update metadata, as this doesn't update metadata.

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    d = json.loads(line.decode("utf-8"))
    try:
        path = d["s1_local_path"] + "/" + d["b_path"]
        exists = True if d["bs1_sha256_error"] == "0" else False
        needs_copy = d["bs1_sha256_error"] == "0" and d["bs2_sha256_error"] != "0"
        if exists and needs_copy:
            src = path
            dest = d["s2_local_path"] + "/" + d["b_path"]
            shutil.copy2(src, dest)
    except Exception as e:
        print("[FATAL ERROR]:", e, file=sys.stderr)
        # d["bs1_comp_sha256"] = ""
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
  
