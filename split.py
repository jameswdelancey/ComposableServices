import datetime as dt
import os
import sys
from typing import Protocol, cast


class SupportsReadInto(Protocol):
    def readinto(self, b: bytearray) -> int: ...


# arg parse
if len(sys.argv) != 4:
    print(
        "split.py -- Takes stdin and splits it every 15 min into floored quarter-hour chunks and periodically touches a file\nUsage: python split.py <outdirname> <outbasenametmpl> <touchfile>"
    )
    sys.exit(1)
g_strOutdirname = sys.argv[1]
g_strOutbasenametmpl = sys.argv[2]
g_strTouchfile = sys.argv[3]
if not os.path.exists(g_strOutdirname):
    print(
        f"FATAL ERROR: <outdirname> '{g_strOutdirname}' does not exist", file=sys.stderr
    )
    sys.exit(1)
try:
    dt.datetime.now().strftime(g_strOutbasenametmpl)
except ValueError:
    print(
        f"FATAL ERROR: <outbasenametmpl> '{g_strOutbasenametmpl}' is not a valid strftime template",
        file=sys.stderr,
    )
    sys.exit(1)

# init loop
f2 = open(g_strTouchfile, "w")
f2.write(" ")
f2.close()
g_cBuf = bytearray(8192)
g_mvcBuf = memoryview(g_cBuf)
tmp_dt = dt.datetime.now()
g_strOutbasename = tmp_dt.replace(
    minute=(tmp_dt.minute // 15) * 15, second=0, microsecond=0
).strftime(g_strOutbasenametmpl)
g_sizeacc = 0
g_hOutFile = open(f"{g_strOutdirname}/{g_strOutbasename}", "ab")
buffer = cast(SupportsReadInto, sys.stdin.buffer)
while True:
    # No Try here because we plan to fail hard if we cannot write a file or have some issue.
    # This is meant to be restarted already for when the upstream ffmpeg binary or rtsp
    # Issue happens. It will be restarted.
    size = buffer.readinto(g_cBuf)
    g_sizeacc += size
    if size == 0:
        break
    elif g_sizeacc > 1024 * 1024:
        g_sizeacc = 0
        tmp_dt = dt.datetime.now()
        localoutbasename = tmp_dt.replace(
            minute=(tmp_dt.minute // 15) * 15, second=0, microsecond=0
        ).strftime(g_strOutbasenametmpl)
        if localoutbasename != g_strOutbasename:
            g_hOutFile.close()
            g_strOutbasename = localoutbasename
            g_hOutFile = open(f"{g_strOutdirname}/{g_strOutbasename}", "ab")
            f2 = open(g_strTouchfile, "w")
            f2.write("")
            f2.close()
    g_hOutFile.write(g_mvcBuf[:size])
g_hOutFile.close()
