import pytest

from showvalues.scripttracker import get_values_from_execution


@pytest.mark.parametrize('code,expected', [
    ('111 + 222 < 555', {'0to9': '333', '0to15': 'True'}),
    ('a = 1; b = 2 + 3', {'11to16': '5'})

])
def test_get_values(code, expected):
    print(code)
    assert expected == get_values_from_execution(code, ['<ast>'])

