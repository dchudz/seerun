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
    assert expected == get_values_from_execution(code)



def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    with NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        result = runner.invoke(cli.main,
                               args=['tests/example.py', temp_html.name])
    assert result.exit_code == 0
