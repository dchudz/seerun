import sys

from tests import add

print(sys.argv)
a, b = sys.argv[1:]
a, b = int(a), int(b)
print("executing call add")
print(add.add(a, b))
print("executed call add")