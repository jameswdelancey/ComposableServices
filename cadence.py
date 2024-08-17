import datetime as dt
import json
import sys
import time

PAYLOAD_TMPL_INTERVAL_A = [  # 5 min
    {"ping_10.0.0.242": ""},
    {"ping_10.0.0.243": ""},
    {"ping_10.0.0.244": ""},
    {"ping_10.0.0.245": ""},
    {"ping_10.0.0.246": ""},
    {"ping_10.0.0.240": ""},
    {"ping_10.0.0.241": ""},
    {"ping_10.0.0.247": ""},
    {"tcpping_10.0.0.242": ""},
    {"tcpping_10.0.0.243": ""},
    {"tcpping_10.0.0.244": ""},
    {"tcpping_10.0.0.245": ""},
    {"tcpping_10.0.0.246": ""},
    {"tcpping_10.0.0.240": ""},
    {"tcpping_10.0.0.241": ""},
    {"tcpping_10.0.0.247": ""},
    {"rtspping_10.0.0.242": ""},
    {"rtspping_10.0.0.243": ""},
    {"rtspping_10.0.0.244": ""},
    {"rtspping_10.0.0.245": ""},
    {"rtspping_10.0.0.246": ""},
    {"rtspping_10.0.0.240": ""},
    {"rtspping_10.0.0.241": ""},
    {"rtspping_10.0.0.247": ""},
]
PAYLOAD_TMPL_INTERVAL_B = [  # 60 min
    {"ftpbytes_D:/ftproot": ""},
    {"latestfile_D:/ts_cam0": ""},
    {"latestfile_D:/ts_cam1": ""},
    {"latestfile_D:/ts_cam2": ""},
    {"latestfile_D:/ts_cam3": ""},
    {"latestfile_D:/ts_cam4": ""},
    {"latestfile_D:/ts_cam5": ""},
    {"latestfile_D:/ts_cam6": ""},
    {"latestfile_D:/ts_cam7": ""},
    {"earliestfile_D:/ts_cam0": ""},
    {"earliestfile_D:/ts_cam1": ""},
    {"earliestfile_D:/ts_cam2": ""},
    {"earliestfile_D:/ts_cam3": ""},
    {"earliestfile_D:/ts_cam4": ""},
    {"earliestfile_D:/ts_cam5": ""},
    {"earliestfile_D:/ts_cam6": ""},
    {"earliestfile_D:/ts_cam7": ""},
    {"numfiles_D:/ts_cam0": ""},
    {"numfiles_D:/ts_cam1": ""},
    {"numfiles_D:/ts_cam2": ""},
    {"numfiles_D:/ts_cam3": ""},
    {"numfiles_D:/ts_cam4": ""},
    {"numfiles_D:/ts_cam5": ""},
    {"numfiles_D:/ts_cam6": ""},
    {"numfiles_D:/ts_cam7": ""},
    {"numbytes_D:/ts_cam0": ""},
    {"numbytes_D:/ts_cam1": ""},
    {"numbytes_D:/ts_cam2": ""},
    {"numbytes_D:/ts_cam3": ""},
    {"numbytes_D:/ts_cam4": ""},
    {"numbytes_D:/ts_cam5": ""},
    {"numbytes_D:/ts_cam6": ""},
    {"numbytes_D:/ts_cam7": ""},
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
        next_interval_b = current_time + dt.timedelta(minutes=60)
        sys.stdout.flush()
    time.sleep(30)
