##### Notes on arch
# 1) Maybe we can ditch the parent id column in directories
# We are not storing dirs independently (normal form) including those
# which have no containing file. So can reconstruct this column later.
# Further it may be a relic of the past because with parsing and a
# datetime, this can also be found without  this only parent ID/tree
# structure.  But for the times where we may have double paths where we
# run forced_new_records, we should have the correct upstream dir ID then.
# 2) Here we will create the root dir without a parent and due to the
# order that we walk the reading directory, we will have parents already
# cached so we can add it via lookup_by_legacy_path without root
# traversal, and given the assumption of order, reach the same output.
import datetime as dt
import glob
import hashlib
import json
import mimetypes
import os
import shutil
import sys
from typing import Protocol, cast

if len(sys.argv) != 4:
    print(
        "Usage: python matchfiledirblob.py <clobber|forced-new-records> <destination_dir/s1_local_path>",
        file=sys.stderr,
    )
    sys.exit(1)

forced_new_records = False if sys.argv[1] != "forced-new-records" else True
s1_local_path = sys.argv[2]
s2_local_path = sys.argv[3]
# next file is copy and compress
# The we follow the standard pipeline

fheaders = [
    "f_id",
    "f_created_at",
    "f_updated_at",
    "f_short_file_name",
    "f_file_name_extension",
    "f_accessed",
    "f_modified",
    "f_created",
    "f_is_deleted",
    "f_blob_id",
    "f_directory_id",
    "f_record_error_code",
    "fo_uuid",
    "fo_blob_id",
    "fo_directory_id",
]
bheaders = [
    "b_id",
    "b_created_at",
    "b_updated_at",
    "b_path",
    "b_mime_type",
    "b_size",
    "b_sha256",
    "b_is_deleted",
    "b_record_error_code",
]
dheaders = [
    "d_id",
    "d_created_at",
    "d_updated_at",
    "d_legacy_path",
    "d_accessed",
    "d_modified",
    "d_created",
    "d_is_deleted",
    "d_record_error_code",
    "d_parent_directory_id",
]
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
s1headers = [
    "s1_id",
    "s1_created_at",
    "s1_updated_at",
    "s1_name",
    "s1_local_path",
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
s2headers = [
    "s2_id",
    "s2_created_at",
    "s2_updated_at",
    "s2_name",
    "s2_local_path",
]

glob_argument_pattern = "E:/new_file_storage/data/part*"  # sys.argv[1]

unsorted_files_to_cat_to_cat = [
    x.replace("\\", "/") for x in glob.glob(glob_argument_pattern)
]

sorted_files_to_cat = sorted(unsorted_files_to_cat_to_cat)

# Ascertain whether this is a better algo to move to the cat program
db_file_records = []
for filename in sorted_files_to_cat:
    try:
        with open(filename, "rb") as buffer:
            while True:
                acc = []
                while True:
                    chunk = buffer.readline()
                    if not chunk:  # If no more lines, break the inner loop
                        break
                    acc.append(chunk)
                    if chunk.rstrip() == b"}":  # End of JSON record
                        break
                # If acc is empty, end of file reached, break the outer loop
                if not acc:
                    break
                # Process accumulated lines
                d = json.loads(b"".join(acc).decode("utf-8"))
                db_file_records.append(d)
    except Exception as e:
        print(f"Error reading file {filename}: {e}")

directories_indexed = {}
files_indexed = {}
blobs_indexed = {}
s_indexed = {}

for db_file_record in db_file_records:
    if db_file_record["d_legacy_path"] not in directories_indexed:
        directories_indexed.update(
            {
                db_file_record["d_legacy_path"]: {
                    header: db_file_record[header] for header in dheaders
                }
            }
        )
    if db_file_record["b_sha256"] not in blobs_indexed:
        blobs_indexed.update(
            {
                db_file_record["b_sha256"]: {
                    header: db_file_record[header]
                    for hg in [bheaders, bs1headers, s1headers, bs2headers, s2headers]
                    for header in hg
                }
            }
        )
    files_indexed.update(
        {
            (
                db_file_record["d_legacy_path"],
                db_file_record["f_short_file_name"],
                db_file_record["b_sha256"],
            ): {header: db_file_record[header] for header in fheaders}
        }
    )
    s_indexed.update({db_file_record["s1_local_path"]: None})
    s_indexed.update({db_file_record["s2_local_path"]: None})

next_dir_id = max([int(x["d_id"]) for x in directories_indexed.values()]) + 1
next_file_id = max([int(x["f_id"]) for x in files_indexed.values()]) + 1
next_blob_id = max([int(x["b_id"]) for x in blobs_indexed.values()]) + 1
next_s_id = (
    max(
        [int(x["s1_id"]) for x in blobs_indexed.values()]
        + [int(x["s2_id"]) for x in blobs_indexed.values()]
    )
    + 1
)
next_bs_id = (
    max(
        [int(x["bs1_id"]) for x in blobs_indexed.values()]
        + [int(x["bs2_id"]) for x in blobs_indexed.values()]
    )
    + 1
)

directories_created_ids = {}
files_created_ids = {}

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    record = json.loads(line.decode("utf-8"))
    try:
        # Existing dir match
        maybe_dir_match = directories_indexed.get(record["d_legacy_path"])
        # new dir match
        maybe_new_dir_match = directories_created_ids.get(record["d_legacy_path"])
        if maybe_new_dir_match:
            record.update(maybe_dir_match)
        elif maybe_dir_match and not forced_new_records:
            record.update(maybe_dir_match)
        else:
            # Assert
            if (maybe_new_dir_match or maybe_dir_match) and not forced_new_records:
                print(
                    f"[FATAL ERROR] dir should be in directories_indexed",
                    file=sys.stderr,
                )

            # Decision to make a new record
            # stage: set the file record with the new directory info
            record["d_id"] = next_dir_id
            now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record["d_created_at"] = now_str
            record["d_updated_at"] = now_str
            dir_stat = os.stat(record["d_legacy_path"])
            record["d_accessed"] = dt.datetime.fromtimestamp(
                dir_stat.st_atime
            ).strftime("%Y-%m-%d %H:%M:%S")
            record["d_modified"] = dt.datetime.fromtimestamp(
                dir_stat.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S")
            record["d_created"] = dt.datetime.fromtimestamp(dir_stat.st_ctime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if forced_new_records:
                # Only check new IDs
                record["d_parent_directory_id"] = directories_created_ids.get(
                    os.path.dirname(record["d_legacy_path"]), 0
                )
            else:
                # Check existing IDs first, then new IDs
                record["d_parent_directory_id"] = directories_indexed.get(
                    os.path.dirname(record["d_legacy_path"])
                ) or directories_created_ids.get(
                    os.path.dirname(record["d_legacy_path"]), 0
                )

            # stage: cleanup
            directories_indexed.update(
                {
                    record["d_legacy_path"]: {
                        header: record[header] for header in dheaders
                    }
                }
            )
            directories_created_ids[record["d_legacy_path"]] = next_dir_id
            next_dir_id += 1

        # Existing
        maybe_blob_match = blobs_indexed.get(record["b_sha256"])
        if maybe_blob_match and not forced_new_records:
            if maybe_blob_match["bs1_sha256_error"] != "0":
                print(
                    "[FATAL ERROR] We have a bad sha and an identical file importing to recover it. Manual intervention required",
                    file=sys.stderr,
                )
                sys.exit(1)
            # Dedup if allowed
            record.update(maybe_blob_match)
        else:
            if s1_local_path not in s_indexed:
                record["s1_id"] = str(next_s_id)
                next_s_id += 1
                now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                record["s1_created_at"] = now_str
                record["s1_updated_at"] = now_str
                record["s1_name"] = s1_local_path
                record["s1_local_path"] = s1_local_path
                s_indexed.update(
                    {s1_local_path: {header: record[header] for header in s1headers}}
                )
            else:
                record.update(s_indexed[s1_local_path])

            if s2_local_path not in s_indexed:
                record["s2_id"] = str(next_s_id)
                next_s_id += 1
                now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                record["s2_created_at"] = now_str
                record["s2_updated_at"] = now_str
                record["s2_name"] = s2_local_path
                record["s2_local_path"] = s2_local_path
                s_indexed.update(
                    {s2_local_path: {header: record[header] for header in s2headers}}
                )
            else:
                record.update(s_indexed[s2_local_path])

            # Make a new record
            record["b_id"] = str(next_blob_id)
            next_blob_id += 1
            now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record["b_created_at"] = now_str
            record["b_updated_at"] = now_str
            # record["b_path",
            full_file_path = record["d_legacy_path"] + "/" + record["f_short_file_name"]
            record["b_mime_type"] = mimetypes.guess_type(full_file_path)[0]
            # record["b_size",
            # record["b_sha256",
            # record["b_is_deleted",
            # record["b_record_error_code",

            # "bs1_id",
            record["bs1_id"] = str(next_bs_id)
            next_bs_id += 1
            record["bs1_created_at"] = "1970-01-01 01:01:01"
            record["bs1_updated_at"] = "1970-01-01 01:01:01"
            record["bs1_blob_id"] = record["b_id"]
            record["bs1_storage_location_id"] = record["s1_id"]
            record["bs1_comp_iter_error"] = "0"
            record["bs1_comp_iterations"] = "0"
            record["bs1_comp_last_checked"] = "1970-01-01 01:01:01"
            record["bs1_comp_sha256"] = ""
            record["bs1_comp_sha256_error"] = "0"
            record["bs1_comp_sha256_last_checked"] = "1970-01-01 01:01:01"
            record["bs1_compression_type"] = ""
            record["bs1_is_compressed"] = "0"
            record["bs1_par2_error"] = "0"
            record["bs1_par2_exists"] = "0"
            record["bs1_par2_last_checked"] = "1970-01-01 01:01:01"
            record["bs1_par2_redundancy_pct"] = "0"
            record["bs1_sha256_error"] = "0"
            record["bs1_sha256_last_checked"] = "1970-01-01 01:01:01"

            # "bs2_id",
            record["bs2_id"] = str(next_bs_id)
            next_bs_id += 1
            record["bs2_created_at"] = "1970-01-01 01:01:01"
            record["bs2_updated_at"] = "1970-01-01 01:01:01"
            record["bs2_blob_id"] = record["b_id"]
            record["bs2_storage_location_id"] = record["s2_id"]
            record["bs2_comp_iter_error"] = "0"
            record["bs2_comp_iterations"] = "0"
            record["bs2_comp_last_checked"] = "1970-01-01 01:01:01"
            record["bs2_comp_sha256"] = ""
            record["bs2_comp_sha256_error"] = "0"
            record["bs2_comp_sha256_last_checked"] = "1970-01-01 01:01:01"
            record["bs2_compression_type"] = ""
            record["bs2_is_compressed"] = "0"
            record["bs2_par2_error"] = "0"
            record["bs2_par2_exists"] = "0"
            record["bs2_par2_last_checked"] = "1970-01-01 01:01:01"
            record["bs2_par2_redundancy_pct"] = "0"
            record["bs2_sha256_error"] = "0"
            record["bs2_sha256_last_checked"] = "1970-01-01 01:01:01"

            # Cleanup
            blobs_indexed.update(
                {
                    record["b_sha256"]: {
                        header: record[header]
                        for hg in [
                            bheaders,
                            bs1headers,
                            s1headers,
                            bs2headers,
                            s2headers,
                        ]
                        for header in hg
                    }
                }
            )

        # Existing
        maybe_file_match = files_indexed.get(
            (record["d_legacy_path"], record["f_short_file_name"], record["b_sha256"])
        )
        # New
        maybe_new_files_match = files_created_ids.get(
            (record["d_legacy_path"], record["f_short_file_name"], record["b_sha256"])
        )
        if maybe_new_dir_match:
            record.update(maybe_file_match)
        elif maybe_file_match and not forced_new_records:
            record.update(maybe_file_match)
        else:
            # Make a new record
            record["f_id"] = next_file_id
            next_file_id += 1
            now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record["f_created_at"] = now_str
            record["f_updated_at"] = now_str
            record["f_blob_id"] = record["b_id"]
            record["f_directory_id"] = record["d_id"]
            record["f_record_error_code"] = "0"
            record["fo_uuid"] = ""
            record["fo_blob_id"] = ""
            record["fo_directory_id"] = ""

            # Cleanup
            files_indexed.update(
                {
                    (
                        record["d_legacy_path"],
                        record["f_short_file_name"],
                        record["b_sha256"],
                    ): {header: record[header] for header in fheaders}
                }
            )
            files_created_ids[
                (
                    record["d_legacy_path"],
                    record["f_short_file_name"],
                    record["b_sha256"],
                )
            ] = next_dir_id

    except Exception as e:
        print("[FATAL ERROR] matchfiledirblob.py:", e, file=sys.stderr)
        record["bs1_comp_sha256"] = ""
        sys.exit(1)
    line = json.dumps(record).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
