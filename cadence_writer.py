import sys
import datetime as dt

date_str = dt.datetime.now().strftime("%Y-%m-%d")
filename = f"D:/log/{date_str}.txt"
f = open(filename, "ab")

while True:
    line = sys.stdin.buffer.readline()
    if not line.strip():
        break
    if dt.datetime.now().strftime("%Y-%m-%d") != date_str:
        date_str = dt.datetime.now().strftime("%Y-%m-%d")
        f.close()
        filename = f"D:/log/{date_str}.txt"
        f = open(filename, "ab")
    f.write(line)
    f.flush()
