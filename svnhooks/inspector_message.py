import sys

msg = sys.argv[1]
if msg is None or len(msg) == 0:
    echo "Empty log messages are not allowed." >&2
    sys.exit(1)
elif len(msg) < 6:
    echo "Least log messages is 6 charactors." >&2
    sys.exit(1)

sys.exit(0)
