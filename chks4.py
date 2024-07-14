import ctypes
import datetime as dt
import json
import os
import sys
from ctypes import POINTER, c_char_p, c_int

s = sys.argv[1]

errors = {
    0: "Success.",
    1: "Repairable damage found.",
    2: "Irreparable damage found.",
    3: "Invalid commandline arguments.",
    4: "Parity file unusable.",
    5: "Repair failed.",
    6: "IO error.",
    7: "Internal error.",
    8: "Out of memory.",
}


libpar2 = ctypes.CDLL("./libpar2.dll")
libpar2.par2cmdline.argtypes = [c_int, POINTER(c_char_p)]
libpar2.par2cmdline.restype = c_int

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    d = json.loads(line.decode("utf-8"))
    try:
        base_path = d["s" + s + "_local_path"] + "/" + d["b_path"]
        current_sha256_error = True if d["bs" + s + "_sha256_error"] != "0" else False
        par2_path = base_path + ".par2"
        base_exists = True if os.path.exists(base_path) else False
        par2_exists = True if os.path.exists(par2_path) else False
        if base_exists:
            if not par2_exists and not current_sha256_error:  # Then create
                cmds = [b"c", b"-q", b"-q", base_path.encode("utf-8")]
                argc = len(cmds)
                argv = (c_char_p * argc)(*cmds)
                rc = libpar2.par2cmdline(argc, argv)
                if rc:
                    print(
                        "[FATAL ERROR] libpar2 create error code:",
                        errors.get(rc),
                        "Unknown error code",
                        file=sys.stderr,
                    )
                    # We tried to create but failed
                    d["bs" + s + "_par2_exists"] = "0"
                    d["bs" + s + "_par2_error"] = "1"
                else:
                    # We successfully created
                    d["bs" + s + "_updated_at"] = dt.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    d["bs" + s + "_par2_exists"] = "1"
                    d["bs" + s + "_par2_error"] = "0"
                    d["bs" + s + "_par2_last_checked"] = dt.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            else:  # par2 exists, then validate
                cmds = [b"v", b"-q", b"-q", base_path.encode("utf-8")]
                argc = len(cmds)
                argv = (c_char_p * argc)(*cmds)
                rc = libpar2.par2cmdline(argc, argv)
                if rc:
                    print(
                        "[FATAL ERROR] libpar2 validate error code:",
                        errors.get(rc),
                        "Unknown error code",
                        file=sys.stderr,
                    )
                    # We tried to validate but failed
                    d["bs" + s + "_par2_exists"] = "1"
                    d["bs" + s + "_par2_error"] = "1"
                else:
                    # We validated successfully
                    d["bs" + s + "_updated_at"] = dt.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    d["bs" + s + "_par2_exists"] = "1"
                    d["bs" + s + "_par2_error"] = "0"
                    d["bs" + s + "_par2_last_checked"] = dt.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
    except Exception as e:
        print("[FATAL ERROR] Exception:", e, file=sys.stderr)
        # We tried to create or validate but failed in python, not libpar2
        d["bs" + s + "_par2_error"] = "2"
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
