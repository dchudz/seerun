from tempfile import NamedTemporaryFile

from click.testing import CliRunner
import pytest

from showvalues import cli
from showvalues.execute import get_values_from_execution


@pytest.mark.parametrize('code,expected', [
    ('111 + 222 < 555', {'0to9': '333', '0to15': 'True'}),
    ('a = 1; b = 2 + 3', {'11to16': '5'})

])
def test_get_values(code, expected):
    print(code)
    assert expected == get_values_from_execution(code)



def test_command_script_tracker():
    """Test the CLI."""
    runner = CliRunner()
    with NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        result = runner.invoke(cli.trackscript,
                               args=['tests/example.py', temp_html.name])
    assert result.exit_code == 0


def test_command_module_tracker():
    """Test the CLI."""
    runner = CliRunner()
    print(cli.trackmodule)
    with NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        result = runner.invoke(cli.trackmodule,
                               args=['/Users/davidchudzicki/showvalues/showvalues/just_for_a_test.py',
                                     temp_html.name,
                                     '--runscript', 'tests/call_add.py'])
        # how to add option? tests/b.py
        print(temp_html.name)
        # assert b'77777' in temp_html.read()
    assert result.exit_code == 0
