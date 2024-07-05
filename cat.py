import glob
import sys
from typing import Protocol, cast


class SupportsReadInto(Protocol):
    def readinto(self, b: bytearray) -> int: ...


if len(sys.argv) != 2:
    print("Usage: python cat.py <filename or glob pattern>")
    sys.exit(1)

pattern = sys.argv[1]

files = glob.glob(pattern)

sorted_files = sorted(files)

g_cBuf = bytearray(8192)
g_mvcBuf = memoryview(g_cBuf)

for filename in sorted_files:
    try:
        with open(filename, "rb") as file:
            buffer = cast(SupportsReadInto, file)
            while True:
                size = buffer.readinto(g_cBuf)
                if not size:
                    break
                sys.stdout.buffer.write(g_mvcBuf[:size])

    except Exception as e:
        print(f"Error reading file {filename}: {e}")
