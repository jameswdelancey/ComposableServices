import sys

part_number = 0
line_count = 0
max_lines_per_file = 10000
output_file_name = f"E:/new_file_storage/data/part{part_number:03}.tsv"
output_file = open(output_file_name, "wb")

while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break

    output_file.write(line)
    line_count += 1

    if line_count == max_lines_per_file:
        output_file.close()
        part_number += 1
        output_file_name = f"E:/new_file_storage/data/part{part_number:03}.tsv"
        output_file = open(output_file_name, "wb")
        line_count = 0

output_file.close()
