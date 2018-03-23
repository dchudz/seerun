import ast
import imp
import sys

import os
import types

import asttokens
from execute import SaveTransformer, SAVE_FUNCTION_NAME

class MyHook(object):
    """PEP302 Import hook which rewrites asserts."""
    def __init__(self, function_to_insert):
        self.modules = {}
        self.function_to_insert = function_to_insert

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

        # hypothesis.internal.conjecture.engine /Users/davidchudzicki/hypothesis-python/src/hypothesis/internal/conjecture/engine.py
        if name not in ['hi', 'hypothesis.internal.conjecture.engine']:
            return None
        print(name, fn)
        with open(fn) as file:
            source = file.read()

        tree = asttokens.ASTTokens(source, parse=True).tree
        SaveTransformer().visit(tree)
        ast.fix_missing_locations(tree)
        co = compile(tree, fn, "exec", dont_inherit=True)
        self.modules[name] = co
        return self

    def _should_rewrite(self, name, fn_pypath, state):
        return False

    def load_module(self, name):
        co = self.modules.pop(name)
        mod = sys.modules[name] = types.ModuleType(name)
        mod.__dict__[SAVE_FUNCTION_NAME] = self.function_to_insert
        print(mod.__dict__)
        try:
            mod.__file__ = co.co_filename
            mod.__loader__ = self
            exec(co, mod.__dict__)
        except:  # noqa
            if name in sys.modules:
                del sys.modules[name]
            raise
        return sys.modules[name]


_values = {}


def save_and_return(value, location):
    _values[location] = repr(value)
    # print(value)
    # print(location)
    return value





def install():
    """Inserts the finder into the import machinery"""
    sys.meta_path.insert(0, MyHook(save_and_return))

install()


# source = 'showvalues/hi.py'
# import hi
# print(hi.aaa)
# hi.f()

source = '/Users/davidchudzicki/hypothesis-python/src/hypothesis/internal/conjecture/engine.py'

from hypothesis import given, strategies as st

@given(st.integers())
def f(x):
    pass

f()


print(_values)

from htmlize import write_html

# write_html('showvalues/hi.py', 'hi.html')

write_html(source,
           'hi.html',
           values=_values)