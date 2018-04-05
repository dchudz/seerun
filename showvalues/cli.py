import click
import os

from .moduletracker import get_values_from_module_execution
from . import moduletracker, scripttracker
from showvalues.htmlize import write_html


# new name: seerun?

@click.group()
def main():
    pass


@main.command()
@click.argument('html_out')
@click.argument('args',
                default=None,
                nargs=-1,
                type=click.UNPROCESSED,
                # help="Path to the script you want to run"
                )
def trackscript(html_out, args):
    """TODO"""
    script_to_run = args[0]
    with open(script_to_run) as script_file:
        source = script_file.read()
    values = scripttracker.get_values_from_execution(source, args)
    write_html(script_path=script_to_run, html_path=html_out, values=values)


@main.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('trackpath')
@click.argument('htmlout')
@click.option('--runscript', default=False, flag_value=True,
              help='Run a script or a module?')
@click.option('--runmodule', default=False, flag_value=True,
              help='Run a script or a module?')
@click.argument('args',
                default=None,
                nargs=-1,
                type=click.UNPROCESSED,
                # help="Path to the script you want to run"
                )
def trackmodule(trackpath, htmlout, runscript, runmodule, args):
    """TODO"""
    #TODO: relative to absolute paths
    #TODO: nice error when len(args) == 0
    trackpath = os.path.abspath(trackpath)
    # TODO: add test for providing both args erroneously & remove these "no cover"s
    if runscript + runmodule != 1:  # pragma: no cover
        raise click.ClickException(  # pragma: no cover
            'Provide exactly one of  --runscript and --runmodule.')
    if runmodule:
        module_to_run = args[0]
        values = get_values_from_module_execution(trackpath, module_to_run, args)
    if runscript:
        script_to_run = args[0]
        values = moduletracker.get_values_from_script_execution(
            trackpath, script_to_run, args)
    write_html(script_path=trackpath, html_path=htmlout, values=values)
