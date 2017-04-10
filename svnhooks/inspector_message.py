import sys

msg = sys.argv[1]
if msg is None or len(msg) == 0:
    print("Empty log messages are not allowed.")
    sys.exit(1)
elif len(msg.decode('utf-8')) < 6:
    print("Least log messages is 6 charactors.")
    sys.exit(1)

sys.exit(0)
