import sys


with open("D:/jsonlonly.log", "w") as f:
    i = 0
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            break
        if not line.startswith(b"{"):
            print(
                "[ERROR] After",
                repr(i),
                "proper JSONL, This trash line from par2 was dropped:",
                repr(line),
                file=f,
            )
            i = 0
            continue
        i += 1
        sys.stdout.buffer.write(line)
