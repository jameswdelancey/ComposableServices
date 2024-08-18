import datetime as dt
import json
import os
import subprocess
import sys

while True:
    line = sys.stdin.buffer.readline()
    if not line.strip():
        break
    d = json.loads(line.decode("utf-8"))
    for k in list(d):
        if k.startswith("ts2jpg"):
            path = k.rsplit("|", 2)[-2]
            out_path = k.rsplit("|", 2)[-1]

            ts_files = [f"{path}/{f}" for f in os.listdir(path) if f.endswith(".ts")]
            ts_files.sort(key=lambda x: x, reverse=False)  # os.path.getmtime(x))

            if len(ts_files) < 2:
                print(
                    "There are not enough .ts files in the directory.", file=sys.stderr
                )
            else:
                second_latest_ts_file = ts_files[-2]

                ffmpeg_command = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    second_latest_ts_file,
                    "-vf",
                    "fps=fps=1/60",  # Get one frame every 60 seconds (you can adjust this)
                    "-vframes",
                    "1",  # Get only one frame (the last one)
                    "-q:v",
                    "2",  # Set the quality of the output image
                    out_path,  # Output file name
                ]

                # Run the ffmpeg command
                try:
                    subprocess.run(ffmpeg_command, check=True)
                    print(
                        f"Latest still image from {second_latest_ts_file} saved to {out_path}.",
                        file=sys.stderr,
                    )
                except subprocess.CalledProcessError as e:
                    print(
                        f"An error occurred while running ffmpeg: {e}", file=sys.stderr
                    )

            d["time"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = json.dumps(d).encode("utf-8")
    sys.stdout.buffer.write(line + b"\n")
    sys.stdout.flush()
