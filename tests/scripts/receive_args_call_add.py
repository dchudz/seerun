import sys

from showvalues import just_for_a_test
print(sys.argv)
a, b = sys.argv[1:]
a, b = int(a), int(b)
print("executing call add")
print(just_for_a_test.add(a, b))
print("executed call add")