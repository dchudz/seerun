import click

from showvalues import moduletracker
from showvalues.htmlize import write_html


# new name: seerun?

@click.group()
def main():
    pass


@main.command()
@click.argument('script')
@click.argument('html_out')
def trackscript(script, html_out):
    """TODO"""
    write_html(script_path=script, html_path=html_out)


@main.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('trackpath')
@click.argument('htmlout')
@click.option('--runscript', default=False, flag_value=True, help='Run a script or a module?')
@click.option('--runmodule', default=False, flag_value=True, help='Run a script or a module?')
@click.argument('args',
                default=None,
                nargs=-1,
                type=click.UNPROCESSED,
                # help="Path to the script you want to run"
                )
def trackmodule(trackpath, htmlout, runscript, runmodule, args):
    """TODO"""
    click.echo(args)
    click.echo(runscript)
    click.echo(runmodule)
    if runscript + runmodule != 1:
        raise click.ClickException(
            'Provide exactly one of  --runscript and --runmodule.')
    if runmodule:
        raise click.ClickException(
            'Sorry, --runmodule is not implemented yet. I lied.')
    if runscript:
        print("hi")
        script_to_run = args[0]
        values = moduletracker.get_values_from_execution(
            trackpath, script_to_run, args)
        print(values)
        write_html(script_path=trackpath, html_path=htmlout, values=values)
