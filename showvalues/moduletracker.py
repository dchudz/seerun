import ast
import imp
import os
import sys
import types

import asttokens

from .run import run_script
from showvalues.scripttracker import SAVE_FUNCTION_NAME
from .ast_rewrite import SaveTransformer


class RewriteHook(object):
    """Shamelessly copies pytest."""

    def __init__(self, function_to_insert, path_to_hook):
        self.modules = {}
        self.function_to_insert = function_to_insert
        self.path_to_hook = path_to_hook

    def find_module(self, name, path=None):
        names = name.rsplit(".", 1)
        lastname = names[-1]
        pth = None
        if path is not None:
            # Starting with Python 3.3, path is a _NamespacePath(), which
            # causes problems if not converted to list.
            path = list(path)
            if len(path) == 1:
                pth = path[0]
        if pth is None:
            try:
                found = imp.find_module(lastname, path)
                fd, fn, desc = found
            except ImportError:
                return None
            if fd is not None:
                fd.close()
            tp = desc[2]
            if tp == imp.PY_COMPILED:
                if hasattr(imp, "source_from_cache"):
                    try:
                        fn = imp.source_from_cache(fn)
                    except ValueError:
                        # Python 3 doesn't like orphaned but still-importable
                        # .pyc files.
                        fn = fn[:-1]
                else:
                    fn = fn[:-1]
            elif tp != imp.PY_SOURCE:
                # Don't know what this is.
                return None
        else:
            fn = os.path.join(pth, name.rpartition(".")[2] + ".py")

        if fn == self.path_to_hook:
            with open(fn) as file:
                source = file.read()

            tree = asttokens.ASTTokens(source, parse=True).tree
            SaveTransformer().visit(tree)
            ast.fix_missing_locations(tree)
            co = compile(tree, fn, "exec", dont_inherit=True)
            self.modules[name] = co
            return self

    def load_module(self, name):
        co = self.modules.pop(name)
        mod = sys.modules[name] = types.ModuleType(name)
        mod.__dict__[SAVE_FUNCTION_NAME] = self.function_to_insert
        try:
            mod.__file__ = co.co_filename
            mod.__loader__ = self
            exec(co, mod.__dict__)
        except:  # noqa
            if name in sys.modules:
                del sys.modules[name]
            raise
        return sys.modules[name]


def install_import_hook(function_to_add, path_to_hook):
    """Inserts the finder into the import machinery"""
    sys.meta_path.insert(0, RewriteHook(function_to_add, path_to_hook))


def get_values_from_execution(module_path_to_watch, script_to_run, args):
    _values = {}

    def save_and_return(value, location):
        _values[location] = repr(value)
        return value

    install_import_hook(save_and_return, module_path_to_watch)
    run_script(script_to_run, args,
               environment={SAVE_FUNCTION_NAME: save_and_return,
                            '_values': _values})

    return _values
