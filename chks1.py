import datetime as dt
import hashlib
import json
import sys
import zlib

magic_numbers = {
    "gz": [b"\x1F\x8B"],
    "zip": [b"\x50\x4B\x03\x04", b"\x50\x4B\x05\x06", b"\x50\x4B\x07\x08"],
    "7z": [b"\x37\x7A\xBC\xAF\x27\x1C"],
    "rar": [b"\x52\x61\x72\x21\x1A\x07\x00", b"\x52\x61\x72\x21\x1A\x07\x01\x00"],
}


stale_before = (dt.datetime.now() - dt.timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")

if "--only-check" in sys.argv:
    cnt = 0

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    d = json.loads(line.decode("utf-8"))
    try:
        path = d["s1_local_path"] + "/" + d["b_path"]
        exists = True if d["bs1_sha256_error"] == "0" else False
        sha256_stale = True if d["bs1_sha256_last_checked"] < stale_before else False
        if exists and sha256_stale:
            if "--only-check" in sys.argv:
                cnt += 1
                continue
            # Don't know if the file is compressed, how many times, how it's compressed
            # each time, or which SHA matches.
            ba_0 = bytearray(8192)
            mv_0 = memoryview(ba_0)
            f = open(path, "rb")
            comp_type_0 = None

            first_loop = True
            while True:
                ba_len_0 = f.readinto(ba_0)
                if not ba_len_0:
                    break
                if first_loop:
                    ## Iteration 0
                    sha_obj_0 = hashlib.sha256()
                    for fmt, magic in magic_numbers.items():
                        if any(ba_0.startswith(m) for m in magic):
                            comp_type_0 = fmt
                            break
                    ## Iteration 1 - Let's only check this case and the ones that are not, we will
                    ## Fix in Jupyter notebook. Same for compression that is not done with gz.
                    if comp_type_0 == "gz":
                        decompressor_0_to_1 = zlib.decompressobj(wbits=31)
                        sha_obj_1 = hashlib.sha256()
                    first_loop = not first_loop

                sha_obj_0.update(mv_0[:ba_len_0])
                if comp_type_0 and comp_type_0 == "gz":
                    byte_acc_1 = decompressor_0_to_1.decompress(mv_0[:ba_len_0])
                    sha_obj_1.update(byte_acc_1)

            f.close()
            sha256_0 = sha_obj_0.hexdigest()
            if comp_type_0 and comp_type_0 == "gz":
                byte_acc_1 = decompressor_0_to_1.flush()
                sha_obj_1.update(byte_acc_1)
                sha256_1 = sha_obj_1.hexdigest()

            sha256_match_uncompressed = d["b_sha256"] == sha256_0
            sha256_0.encode()
            if sha256_match_uncompressed:
                d["bs1_sha256_error"] = "0"
                d["bs1_sha256_last_checked"] = dt.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                d["bs1_comp_sha256"] = ""
                d["bs1_comp_sha256_error"] = "0"
                d["bs1_comp_sha256_last_checked"] = ""
                d["bs1_comp_iterations"] = "0"
                d["bs1_comp_iter_error"] = "0"
                d["bs1_updated_at"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                d["bs1_comp_last_checked"] = dt.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                d["bs1_is_compressed"] = "0"
                d["bs1_compression_type"] = ""

            else:
                sha256_match_compressed = (
                    comp_type_0 == "gz" and d["b_sha256"] == sha256_1
                )
                if sha256_match_compressed:
                    d["bs1_sha256_error"] = "0"
                    d["bs1_sha256_last_checked"] = dt.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    d["bs1_comp_sha256"] = sha256_0
                    d["bs1_comp_sha256_error"] = "0"
                    d["bs1_comp_sha256_last_checked"] = dt.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    d["bs1_comp_iterations"] = "1"
                    d["bs1_comp_iter_error"] = "0"
                    d["bs1_updated_at"] = dt.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    d["bs1_comp_last_checked"] = dt.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    d["bs1_is_compressed"] = "1"
                    d["bs1_compression_type"] = "gz"
                else:
                    d["bs1_comp_sha256"] = ""
                    d["bs1_comp_sha256_error"] = "2"
                    d["bs1_comp_sha256_last_checked"] = ""
                    d["bs1_sha256_error"] = "2"
    except Exception as e:
        print("[FATAL ERROR]:", e, file=sys.stderr)
        d["bs1_comp_sha256"] = ""
        d["bs1_comp_sha256_error"] = "2"
        d["bs1_comp_sha256_last_checked"] = ""
        d["bs1_sha256_error"] = "2"
    if "--only-check" in sys.argv:
        continue

    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")

if "--only-check" in sys.argv:
    print(cnt)
