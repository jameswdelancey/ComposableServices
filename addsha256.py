import hashlib
import json
import sys

ba_0 = bytearray(8192)
mv_0 = memoryview(ba_0)
while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    d = json.loads(line.decode("utf-8"))
    try:
        full_file_path = d["d_legacy_path"] + "/" + d["f_short_file_name"]
        sha_obj_0 = hashlib.sha256()
        with open(full_file_path, "rb") as f:
            while True:
                ba_len_0 = f.readinto(ba_0)
                if not ba_len_0:
                    break
                sha_obj_0.update(mv_0[:ba_len_0])
        d["b_sha256"] = sha_obj_0.hexdigest()
    except Exception as e:
        print("[FATAL ERROR]:", e, file=sys.stderr)
        # d["bs1_comp_sha256"] = ""
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
