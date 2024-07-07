import sys


while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    line = line.replace(sys.argv[1].encode('utf-8'), sys.argv[2].encode('utf-8'))
    sys.stdout.buffer.write(line)
