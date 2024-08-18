import shlex
import subprocess
import sys
import time

if len(sys.argv) != 3:
    print("Usage: python script.py '<command>' <filepath_to_save_pid>", file=sys.stderr)
    sys.exit(1)

command_string = sys.argv[1]
pid_file_path = sys.argv[2]
parsed_command = shlex.split(command_string)
binary_name = parsed_command[0].encode("utf-8")

# If the command by the current pid is running, await it.
try:
    with open(pid_file_path, "rb") as pid_file:
        pid = pid_file.read().strip().decode("utf-8")
except Exception:
    pid = b"0"

is_running = True
while is_running:
    try:
        # Run tasklist and find the process with the given PID
        tasklist_output = subprocess.check_output(["tasklist", "/fi", f"PID eq {pid}"])
        # Check if the binary name is in the output
        is_running = binary_name.lower() in tasklist_output.lower()
    except subprocess.CalledProcessError:
        is_running = False
    time.sleep(15)

process = subprocess.Popen(parsed_command)
pid = str(process.pid).encode("utf-8")

print(f"[INFO] Process starting at pid: {pid.decode('utf-8')}", file=sys.stderr)

with open(pid_file_path, "wb") as pid_file:
    pid_file.write(pid)

process.wait()

print(f"[INFO] Process at pid: {pid.decode('utf-8')} is closed", file=sys.stderr)
