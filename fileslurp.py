### OUTPUT EXAMPLE
# {"f_short_file_name": "template.hy", "f_file_name_extension": "hy",
# "f_created": "2017-08-13 07:05:34", "f_accessed": "2024-07-13 07:17:25",
# "f_modified": "2024-07-13 07:17:25", "f_is_deleted": 0, "b_size": 15541,
# "b_is_deleted": 0, "b_record_error_code": 0,
# "d_legacy_path": "C:/Users/Administrator/Desktop/py2hy-master/py2hy-master/tools",
# "d_is_deleted": 0, "d_record_error_code": 0}
import datetime as dt
import hashlib
import json
import os
import sys

base_path = sys.argv[1]
ba_0 = bytearray(8192)
mv_0 = memoryview(ba_0)
for root, dirs, files in os.walk(base_path):
    for file in files:
        root = root.replace("\\", "/")
        full_file_path = os.path.join(root, file).replace("\\", "/")
        stat = os.stat(full_file_path)
        # sha_obj_0 = hashlib.sha256()
        # with open(full_file_path, 'rb') as f:
        # while True:
        #  ba_len_0 = f.readinto(ba_0)
        #  if not ba_len_0:
        #   break
        #  sha_obj_0.update(mv_0[:ba_len_0])
        # Create info dictionary for current file
        d = {
            "f_short_file_name": file,
            "f_file_name_extension": file.rsplit(".", 1)[-1],
            "f_created": dt.datetime.fromtimestamp(stat.st_ctime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "f_accessed": dt.datetime.fromtimestamp(stat.st_atime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "f_modified": dt.datetime.fromtimestamp(stat.st_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "f_is_deleted": 0,
            "b_size": stat.st_size,
            "b_is_deleted": 0,
            "b_record_error_code": 0,
            "d_legacy_path": root,
            "d_is_deleted": 0,
            "d_record_error_code": 0,
        }
        line = json.dumps(d).encode("utf-8")
        sys.stdout.buffer.write(line + b"\n")
