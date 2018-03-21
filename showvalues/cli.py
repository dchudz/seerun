# -*- coding: utf-8 -*-

"""Console script for rewritecov."""
import logging
import sys
import click

from rewritecov import find_uncovered, DELETE, NONIFY


def format_uncovereds(uncovereds, description):
    if uncovereds:
        collection_str = ', '.join(str(u.lineno) for u in sorted(uncovereds))
        return 'Lines with %s: %s' % (description, collection_str)
    else:
        return ''


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.argument('path')
def main(verbose, path):
    """Console script for rewritecov."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    with open(path) as code_file:
        code = code_file.read()
    uncovereds = find_uncovered(code)
    if uncovereds:
        deleted = {u for u in uncovereds if u.type == DELETE}
        nonified = {u for u in uncovereds if u.type == NONIFY}

        click.echo(format_uncovereds(
            deleted,
            'stuff we could delete'))
        click.echo(format_uncovereds(
            nonified,
            'function calls we could replace with None'))
    else:
        click.echo('Yay, every change we tried made it fail!')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
