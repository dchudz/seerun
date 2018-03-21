from click.testing import CliRunner
import pytest

from rewritecov import find_uncovered, DELETE, NONIFY, Rewrite
from rewritecov import cli

code1 = """a = 1
b = 2
    
def f():
    x = 1
    y = 2
    z = x + 3


def test_hi():
    y = 3
    f()
    return a

test_hi()
"""

code2 = """import re

a = 1

def replace(s):
    return re.sub(r'\s+', '_', s)

def test_hi():
    replace('hi there')

test_hi()
"""

code3 = """import re


def munge_some_text(text):
    replacements = [
        (r'[\s+]', r'_'),
        (r'[^a-zA-Z0-9_]', r'')
    ]
    for old, new in replacements:
        text = re.sub(old, new, text)
    return text


def test_hi():
    munge_some_text('hi there!')


test_hi()
"""


@pytest.mark.parametrize('code,expected', [
    (code1, {Rewrite(lineno, DELETE) for lineno in [2, 6, 7]}),
    (code2, {Rewrite(3, DELETE), Rewrite(6, NONIFY)}),
    (code3, {Rewrite(6, DELETE),
             Rewrite(7, DELETE),
             Rewrite(9, DELETE),
             Rewrite(11, DELETE),
             Rewrite(10, NONIFY)})

])
def test_find_uncovered(code, expected):
    assert find_uncovered(code) == expected


def test_fails_on_bad_input():
    with pytest.raises(ValueError):
        find_uncovered('assert False')


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, args=['tests/example.py'])
    print(result.output)
    assert result.exit_code == 0
