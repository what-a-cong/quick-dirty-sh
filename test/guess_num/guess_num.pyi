import sys

answer = 0

if len(sys.argv) == 3:
    print(answer)
    sys.exit(0)

assert len(sys.argv) == 2

input = int(sys.argv[1])

if input == answer:
    sys.exit(0)
elif input > answer:
    sys.exit(1)
else:
    sys.exit(2)
