import pytest

from showvalues.scripttracker import get_values_from_execution


# The important feature of this code is that its repr refers to an attribute of
# itself.
code_with_repr = """class HoldsX(object):
    def __init__(self, x): self.x = x
    def __repr__(self): return 'HoldsX(%r)' % (self.x,)

s = HoldsX(1)
"""


@pytest.mark.parametrize('code,expected', [
    ('111 + 222 < 555', {'0to9': ['333'], '0to15': ['True']}),
    ('a = 1; b = 2 + 3', {'11to16': ['5']}),
    ('for i in range(3): print(i + 100)', {'25to32': ['100', '101', '102']}),
    (code_with_repr, {}),
])
def test_get_values(code, expected):
    actual = get_values_from_execution(code, ['<ast>'], raise_exceptions=True)
    # Extra values are OK, since we won't necessarily bother writing down in
    # the test everything that we expect.
    assert expected.items() <= actual.items()
    print(actual)
