import coverage
import os
import subprocess

from seerun.moduletracker import get_values_from_module_execution
from seerun import scripttracker
from seerun.htmlize import write_html

cov = coverage.Coverage()
cov.start()

trackpath = 'tests/add.py'

args = ['tests.scripts.receive_args_call_add', '33333', '44444']

module_to_run = args[0]
values = get_values_from_module_execution(trackpath, module_to_run, args)


cov.stop()
cov.save()

cov.html_report()