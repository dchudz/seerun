# -*- coding: utf-8 -*-

"""Console script for showvalues."""
import importlib
import logging
import sys
import click

from showvalues.htmlize import write_html


def format_uncovereds(uncovereds, description):
    if uncovereds:
        collection_str = ', '.join(str(u.lineno) for u in sorted(uncovereds))
        return 'Lines with %s: %s' % (description, collection_str)
    else:
        return ''



class WarnOnImport(object):
    def __init__(self, *args):
        self.module_names = args

    def find_module(self, fullname, path=None):
        if fullname in self.module_names:
            self.path = path
            return self
        return None

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]
        module_info = importlib.find_module(name, self.path)
        module = importlib.load_module(name, *module_info)
        sys.modules[name] = module

        logging.warning("Imported deprecated module %s", name)
        return module

class ImportFindPrint(object):
    def __init__(self, *args):
        self.module_names = args

    def find_module(self, fullname, path=None):
        print("%s: %s" % (fullname, path))
        return None


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.argument('python_source')
@click.argument('html_out')
def main(verbose, python_source, html_out):
    """Console script for showvalues."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    write_html(python_source, html_out)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
