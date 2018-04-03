import pytest

from showvalues.scripttracker import get_values_from_execution


@pytest.mark.parametrize('code,expected', [
    ('111 + 222 < 555', {'0to9': ['333'], '0to15': ['True']}),
    ('a = 1; b = 2 + 3', {'11to16': ['5']}),
    ('for i in range(3): print(i + 100)', {'25to32': ['100', '101', '102']})


])
def test_get_values(code, expected):
    actual = get_values_from_execution(code, ['<ast>'])
    # Extra values are OK, since we won't necessarily bother writing down in
    # the test everything that we expect.
    assert expected.items() <= actual   .items()
