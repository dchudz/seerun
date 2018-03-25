import subprocess
from tempfile import NamedTemporaryFile

import pytest


@pytest.yield_fixture(scope='function')
def temp_html():
    with NamedTemporaryFile(suffix='.html') as file:
        yield file


def test_command_script_tracker(temp_html):
    """Test the CLI."""
    subprocess.call(
        ['viewrun', 'trackscript',
         temp_html.name,
         'tests/scripts/add_received_args.py',
         '33333', '44444'])
    assert b'77777' in temp_html.read()


@pytest.mark.parametrize('script', [
    'tests/scripts/no_args_call_add.py',
    'tests/scripts/call_add_in_main.py',
])
def test_module_tracker_script_no_args(script, temp_html):
    """Test the CLI."""
    subprocess.call(
        ['viewrun', 'trackmodule',
         'showvalues/just_for_a_test.py',
         temp_html.name,
         '--runscript', script])
    assert b'77777' in temp_html.read()


def test_module_tracker_script_with_args(temp_html):
    """Test the CLI."""
    subprocess.call(
        ['viewrun', 'trackmodule',
         'showvalues/just_for_a_test.py',
         temp_html.name,
         '--runscript',
         'tests/scripts/receive_args_call_add.py',
         '33333', '44444'])
    assert b'77777' in temp_html.read()


def test_module_tracker_module(temp_html):
    subprocess.call(
        ['viewrun', 'trackmodule',
         'showvalues/just_for_a_test.py',
         temp_html.name,
         '--runmodule',
         'tests.scripts.receive_args_call_add',
         '33333', '44444'])
    assert b'77777' in temp_html.read()
