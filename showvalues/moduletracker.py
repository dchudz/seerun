import ast
import imp
import os
import sys
import types

import asttokens

from .run import run, run_python_module, get_execution_environment
from .ast_rewrite import SaveTransformer, SAVE_FUNCTION_NAME


class RewriteHook(object):
    """Shamelessly copies pytest."""

    # Lots of `# pragma: no cover` here because I haven't tested cases that
    # need all of this, but I suspect it's better to keep than delete some of
    # this stuff I copied from pytest.
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
            if len(path) == 1:  # pragma: no cover
                pth = path[0]
        if pth is None:
            try:
                found = imp.find_module(lastname, path)
                fd, fn, desc = found
            except ImportError:  # pragma: no cover
                return None  # pragma: no cover
            if fd is not None:  # pragma: no cover
                fd.close()  # pragma: no cover
            tp = desc[2]
            if tp == imp.PY_COMPILED:  # pragma: no cover
                if hasattr(imp, "source_from_cache"):  # pragma: no cover
                    try:  # pragma: no cover
                        fn = imp.source_from_cache(fn)  # pragma: no cover
                    except ValueError:  # pragma: no cover
                        # Python 3 doesn't like orphaned but still-importable
                        # .pyc files.
                        fn = fn[:-1]  # pragma: no cover
                else:
                    fn = fn[:-1]  # pragma: no cover
            elif tp != imp.PY_SOURCE:  # pragma: no cover
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
        except:  # noqa  # pragma: no cover
            if name in sys.modules:  # pragma: no cover
                del sys.modules[name]  # pragma: no cover
            raise  # pragma: no cover
        return sys.modules[name]


def install_import_hook(function_to_add, path_to_hook):
    """Inserts the finder into the import machinery"""
    sys.meta_path.insert(0, RewriteHook(function_to_add, path_to_hook))


def get_values_from_script_execution(path_to_watch, script_to_run, args):
    environment = get_execution_environment()
    install_import_hook(environment[SAVE_FUNCTION_NAME], path_to_watch)
    with open(script_to_run) as script_file:
        script_source = script_file.read()

    run(script_source, args, environment=environment)
    return environment['_seerun_saved_values']



def get_values_from_module_execution(path_to_watch, module_to_run, args):
    environment = get_execution_environment()
    install_import_hook(environment[SAVE_FUNCTION_NAME], path_to_watch)
    run_python_module(module_to_run, args, environment=environment)
    return environment['_seerun_saved_values']
