import datetime as dt
import gzip
import json
import os
import shutil
import sys

bs1headers = [
    "bs1_id",
    "bs1_created_at",
    "bs1_updated_at",
    "bs1_blob_id",
    "bs1_storage_location_id",
    "bs1_comp_iter_error",
    "bs1_comp_iterations",
    "bs1_comp_last_checked",
    "bs1_comp_sha256",
    "bs1_comp_sha256_error",
    "bs1_comp_sha256_last_checked",
    "bs1_compression_type",
    "bs1_is_compressed",
    "bs1_par2_error",
    "bs1_par2_exists",
    "bs1_par2_last_checked",
    "bs1_par2_redundancy_pct",
    "bs1_sha256_error",
    "bs1_sha256_last_checked",
]
bs2headers = [
    "bs2_id",
    "bs2_created_at",
    "bs2_updated_at",
    "bs2_blob_id",
    "bs2_storage_location_id",
    "bs2_comp_iter_error",
    "bs2_comp_iterations",
    "bs2_comp_last_checked",
    "bs2_comp_sha256",
    "bs2_comp_sha256_error",
    "bs2_comp_sha256_last_checked",
    "bs2_compression_type",
    "bs2_is_compressed",
    "bs2_par2_error",
    "bs2_par2_exists",
    "bs2_par2_last_checked",
    "bs2_par2_redundancy_pct",
    "bs2_sha256_error",
    "bs2_sha256_last_checked",
]


if len(sys.argv) != 3:
    print(
        "Usage: python copy1to2.py <yes_origin_to_s1|no_origin_to_s1> <yes_s1_to_s2|no>",
        file=sys.stderr,
    )
    sys.exit(1)

yes_origin_to_s1 = True if sys.argv[1] == "yes_origin_to_s1" else False
yes_s1_to_s2 = True if sys.argv[2] == "yes_s1_to_s2" else False

# Assumes s2_local_path is set for the correct destination
# Assumes that chk for sha256 and par2 will subsequently run
# to update metadata, as this doesn't update metadata.

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    d = json.loads(line.decode("utf-8"))
    try:
        if yes_origin_to_s1:
            origin_path = d["d_legacy_path"] + "/" + d["f_short_file_name"]
            dst_path = d["s1_local_path"] + "/" + d["b_path"]
            exists = os.path.exists(origin_path)

            with open(origin_path, "rb") as src_file:
                with gzip.open(dst_path, "wb") as dst_file:
                    buffer_size = 1024 * 8
                    buffer = bytearray(buffer_size)
                    view = memoryview(buffer)
                    while True:
                        num_bytes_read = src_file.readinto(buffer)
                        if not num_bytes_read:
                            break
                        dst_file.write(view[:num_bytes_read])
        if yes_s1_to_s2:
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
