import datetime as dt
import json
import sys
import time

PAYLOAD_TMPL_INTERVAL_A = []  # 5 min
PAYLOAD_TMPL_INTERVAL_B = [  # 30 min
    {"latestfile_D:/ts_cam0": "", "pid_file": "D:/ts_cam0_touch.txt"},
    {"latestfile_D:/ts_cam1": "", "pid_file": "D:/ts_cam1_touch.txt"},
    {"latestfile_D:/ts_cam2": "", "pid_file": "D:/ts_cam2_touch.txt"},
    {"latestfile_D:/ts_cam3": "", "pid_file": "D:/ts_cam3_touch.txt"},
    {"latestfile_D:/ts_cam4": "", "pid_file": "D:/ts_cam4_touch.txt"},
    {"latestfile_D:/ts_cam5": "", "pid_file": "D:/ts_cam5_touch.txt"},
    {"latestfile_D:/ts_cam6": "", "pid_file": "D:/ts_cam6_touch.txt"},
    {"latestfile_D:/ts_cam7": "", "pid_file": "D:/ts_cam7_touch.txt"},
]
next_interval_a = dt.datetime.now() - dt.timedelta(minutes=1)
next_interval_b = dt.datetime.now() - dt.timedelta(minutes=1)

while True:
    if dt.datetime.now() > next_interval_a:
        for x in PAYLOAD_TMPL_INTERVAL_A:
            sys.stdout.buffer.write(json.dumps(x).encode("utf-8") + b"\n")
        current_time = dt.datetime.now()
        next_interval_a = current_time + dt.timedelta(minutes=15)
        sys.stdout.flush()
    if dt.datetime.now() > next_interval_b:
        for x in PAYLOAD_TMPL_INTERVAL_B:
            sys.stdout.buffer.write(json.dumps(x).encode("utf-8") + b"\n")
        current_time = dt.datetime.now()
        next_interval_b = current_time + dt.timedelta(minutes=30)
        sys.stdout.flush()
    time.sleep(30)
