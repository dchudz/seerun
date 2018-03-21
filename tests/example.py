import re

a = 1


def replace(s):
    return re.sub(r'\s+', '_', s)


def test_hi():
    assert ' ' not in replace('hi there')


test_hi()
