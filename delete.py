import json
import os
import shutil
import time

directories = [
    "D:/ts_cam0",
    "D:/ts_cam1",
    "D:/ts_cam2",
    "D:/ts_cam3",
    "D:/ts_cam4",
    "D:/ts_cam5",
    "D:/ts_cam6",
    "D:/ts_cam7",
    "D:/ftproot",
]
dryrun = False
cache_path = "D:/delete_sorted_files.txt"
try:
    with open(cache_path, "r") as f:
        sorted_files = json.load(f)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    # Initialize an empty list to store (mtime, file_path) tuples
    files_with_mtime = []

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for name in files:
                file_path = os.path.join(root, name)
                mtime = os.path.getmtime(file_path)
                files_with_mtime.append((mtime, file_path))
            if len(list(files)) + len(list(dirs)) == 0:
                os.rmdir(root)
    files_with_mtime.sort()
    sorted_files = [file_path for _, file_path in files_with_mtime]

path = "D:/"

while True:
    total, used, free = shutil.disk_usage(path)
    free_percent = (free / total) * 100

    if free_percent > 20:
        with open(cache_path, "w") as f:
            json.dump(sorted_files, f)
        break

    try:
        fn = sorted_files.pop(0)
        i = 0
        while fn and i < 20:
            os.unlink(fn) if not dryrun else print(fn)
            fn = sorted_files.pop(0)
            i += 1
    except (IndexError, FileNotFoundError):
        try:
            os.unlink(cache_path)
        except FileNotFoundError:
            pass
        break
if not dryrun:
    time.sleep(15 * 60)
