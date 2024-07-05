import os

for i in range(8):
    try:
        os.mkdir(f"D:/ts_cam{i}")
    except FileExistsError:
        pass
    f2 = open(f"D:/ts_cam{i}_touch.txt", "w")
    f2.write("")
    f2.close()
