import json
import sys

headers = [
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
    "b_id",
    "b_created_at",
    "b_updated_at",
    "b_path",
    "b_mime_type",
    "b_size",
    "b_sha256",
    "b_is_deleted",
    "b_record_error_code",
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
    "s1_id",
    "s1_created_at",
    "s1_updated_at",
    "s1_name",
    "s1_local_path",
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
    "s2_id",
    "s2_created_at",
    "s2_updated_at",
    "s2_name",
    "s2_local_path",
    "fo_uuid",
    "fo_blob_id",
    "fo_directory_id",
]
part_number = 0
line_count = 0
max_lines_per_file = 10000
output_file_name = f"D:/t/partnew{part_number:03}.ppjson"
output_file = open(output_file_name, "wb")

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    d = json.loads(line.decode("utf-8"))
    rd = {k: d[k] for k in headers}

    line = json.dumps(rd, indent=0, separators=(",", ":")).encode("utf-8")
    output_file.write(line + b"\n")
    line_count += 1

    if line_count == max_lines_per_file:
        # No try here because let's fail hard if we can't copy.
        output_file.close()
        part_number += 1
        output_file_name = f"D:/t/part{part_number:03}.ppjson"
        output_file = open(output_file_name, "wb")
        line_count = 0

output_file.close()
