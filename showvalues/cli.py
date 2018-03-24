# -*- coding: utf-8 -*-

"""Console script for showvalues."""
import logging
import sys
import click

from showvalues import moduletracker
from showvalues.htmlize import write_html


# seerun?

@click.group()
def main():
    return 11


@main.command()
@click.argument('script')
@click.argument('html_out')
def trackscript(script, html_out):
    """TODO"""
    write_html(script_path=script, html_path=html_out)


@main.command()
@click.argument('modulepath')
@click.argument('html_out')
@click.option('--runscript',
              default=None,
              help="Path to the script you want to run")
@click.option('--runmodule',
              default=None,
              help="???")
def trackmodule(modulepath, html_out, runscript, runmodule):
    """TODO"""
    click.echo("runscei: " + runscript)
    if runscript and runmodule:
        raise click.ClickException(
            'You provided --runscript and --runmodule. Instead, '
            'provide exactly one.')
    if runmodule:
        raise click.ClickException(
            'Sorry, --runmodule is not implemented yet. I lied.')
    if runscript:
        print("if runscript:")
        values = moduletracker.get_values_from_execution(modulepath, runscript)
        print("values: %r" % values)

        write_html(script_path=modulepath, html_path=html_out, values=values)

        click.echo("something good should happen now")


#
# if __name__ == "__main__":
#     sys.exit(main())  # pragma: no cover
