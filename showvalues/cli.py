# -*- coding: utf-8 -*-

"""Console script for showvalues."""
import logging
import sys
import click

from showvalues.html import write_html


def format_uncovereds(uncovereds, description):
    if uncovereds:
        collection_str = ', '.join(str(u.lineno) for u in sorted(uncovereds))
        return 'Lines with %s: %s' % (description, collection_str)
    else:
        return ''


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.argument('python_source')
@click.argument('html_out')
def main(verbose, python_source, html_out):
    """Console script for showvalues."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    write_html(python_source, python_source)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
