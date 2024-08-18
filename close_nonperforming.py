import datetime as dt
import json
import subprocess
import sys

while True:
    line = sys.stdin.buffer.readline()
    if not line.strip():
        break
    d = json.loads(line.decode("utf-8"))
    for k in list(d):
        if k.startswith("latestfile"):
            path = k.split("_", 1)[-1]
            now = dt.datetime.now()
            date_time = dt.datetime.strptime(d[k], "%Y-%m-%d %H:%M:%S")
            if now - date_time > dt.timedelta(minutes=30):
                try:
                    with open(d["pid_file"], "rb") as f:
                        pid = f.read().strip().decode("utf-8")
                except Exception:
                    print(f"[WARN] Process has no PID file found.", file=sys.stderr)
                    pid = b""
                if pid:
                    try:
                        subprocess.check_output(["taskkill", "/F", "/PID", pid])
                        print(
                            f"[INFO] Process with PID {pid} has been killed.",
                            file=sys.stderr,
                        )
                    except Exception:
                        print(
                            f"[INFO] Process with PID {pid} is not active but was decided closed.",
                            file=sys.stderr,
                        )
            else:
                if "-d" in sys.argv:
                    print(
                        f"[DEBUG] File {d} is {now - date_time} old, skipping.",
                        file=sys.stderr,
                    )
            d["time"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # line = json.dumps(d).encode("utf-8")
    # sys.stdout.buffer.write(line + b"\n")
    # sys.stdout.flush()
