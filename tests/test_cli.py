from tempfile import NamedTemporaryFile

from click.testing import CliRunner
import pytest

from showvalues import cli


def test_command_script_tracker():
    """Test the CLI."""
    runner = CliRunner()
    with NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        result = runner.invoke(cli.trackscript,
                               args=['tests/example.py', temp_html.name])
    assert result.exit_code == 0


@pytest.mark.parametrize('script', [
    'tests/scripts/no_args_call_add.py',
    'tests/scripts/call_add_in_main.py',
])
def test_module_tracker_script_no_args(script):
    """Test the CLI."""
    # had some trouble with the Click test runner, so subprocess.call it is.
    with NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        import subprocess
        subprocess.call(['viewrun', 'trackmodule',
                         '/Users/davidchudzicki/showvalues/showvalues'
                         '/just_for_a_test.py',
                         temp_html.name,
                         '--runscript', script])
        print(temp_html.name)
        assert b'77777' in temp_html.read()


def test_module_tracker_with_args():
    """Test the CLI."""
    # had some trouble with the Click test runner, so subprocess.call it is.
    with NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        import subprocess
        subprocess.call(['viewrun', 'trackmodule',
                         '/Users/davidchudzicki/showvalues/showvalues'
                         '/just_for_a_test.py',
                         temp_html.name,
                         '--runscript',
                         'tests/scripts/receive_args_call_add.py',
                         '33333', '44444'])
        print(temp_html.name)
        assert b'77777' in temp_html.read()
