import os
import sys

current_slug = ""
dirnames = []

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    dirname = (
        os.path.dirname(line.rstrip().decode("utf-8"))
        .encode("utf-8")
        .replace(b".", b"")
        .replace(b"/", b"")
    )
    slug = dirname[:2] if len(dirname) == 4 or len(dirname) == 2 else b"__"
    if slug != current_slug:
        f = open(
            f"E:/new_file_storage/file-storage-working-dir/bs1_{slug.decode('utf-8')}.txt",
            "wb" if slug not in dirnames else "ab",
        )
        current_slug = slug
        dirnames.append(slug)

    f.write(line.rstrip() + b"\n")

f.close()
