import coverage
import os
import subprocess

from showvalues.moduletracker import get_values_from_module_execution
from showvalues import scripttracker
from showvalues.htmlize import write_html

cov = coverage.Coverage()
cov.start()

# subprocess.call(
#     ['viewrun', 'trackscript',
#      '/tmp/hi',
#      'tests/scripts/add_received_args.py',
#      '33333', '44444'],
#     env=dict(os.environ, COVERAGE_PROCESS_START='.coveragerc'))

trackpath = 'tests/add.py'

args = ['tests.scripts.receive_args_call_add', '33333', '44444']

module_to_run = args[0]
values = get_values_from_module_execution(trackpath, module_to_run, args)


cov.stop()
cov.save()

cov.html_report()