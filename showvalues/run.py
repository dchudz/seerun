"""Functions for running a specified Python script or module.

A lot of the was taken from coverage.py:
https://bitbucket.org/ned/coveragepy/src
/a31983fd62940d4f039de21dc3ce84c8c659b831/coverage/execfile.py

Probably we're missing some stuff I should have taken, and has some stuff
that wasn't necessary to take.

Lots of "# pragma: no cover" b/c I don't have tetss using all of this, but
I suspect some of it is better to keep than not to.
"""
import logging
import sys
import traceback
import types
import importlib
import importlib.util

import os
from collections import defaultdict

from .ast_rewrite import SAVE_FUNCTION_NAME


def find_module(modulename):
    """Find the module named `modulename`.

    Returns the file path of the module, and the name of the enclosing
    package.
    """
    try:
        spec = importlib.util.find_spec(modulename)
    except ImportError as err:  # pragma: no cover
        raise Exception(str(err))  # pragma: no cover
    if not spec:  # pragma: no cover
        raise Exception("No module named %r" % (modulename,))  # pragma: no cover
    pathname = spec.origin
    packagename = spec.name
    if pathname.endswith("__init__.py") and not modulename.endswith(  # pragma: no cover
            "__init__"):
        mod_main = modulename + ".__main__"  # pragma: no cover
        spec = importlib.util.find_spec(mod_main)  # pragma: no cover
        if not spec:  # pragma: no cover
            raise Exception(  # pragma: no cover
                "No module named %s; "
                "%r is a package and cannot be directly executed"
                % (mod_main, modulename)
            )
        pathname = spec.origin  # pragma: no cover
        packagename = spec.name  # pragma: no cover
    packagename = packagename.rpartition(".")[0]
    return pathname, packagename


def run_python_module(modulename, args, environment):
    """Run a Python module, as though with ``python -m name args...``.

    `modulename` is the name of the module, possibly a dot-separated name.
    `args` is the argument array to present as sys.argv, including the first
    element naming the module being executed.

    """

    pathname, packagename = find_module(modulename)

    pathname = os.path.abspath(pathname)
    args = list(args)
    args[0] = pathname
    run_python_file(pathname, args, environment)


def run_python_file(path, args, environment):
    with open(path) as file:
        source = file.read()
    run(source, args, environment, path=path)


def run(script_source_or_compiled, args, environment, path=None,
        raise_exceptions=False):
    """

    Args:
        script_source_or_compiled:
        args:
        environment:
        path:
        raise_exceptions: usually we want to run the code and report results even
                       if it fails. But disallowing failue is helpful for
                       tests.

    Returns:

    """
    # thanks coverage.py!
    old_main_mod = sys.modules['__main__']
    main_mod = types.ModuleType('__main__')
    sys.modules['__main__'] = main_mod
    if path:
        main_mod.__file__ = path
    main_mod.__builtins__ = sys.modules['builtins']
    old_sys_argv = sys.argv
    sys.argv = args

    try:
        exec(script_source_or_compiled,
             {**main_mod.__dict__,
              **environment
              }
             )
    except SystemExit as e:
        if e.code != 0:
            # Don't make noise about SystemExit(0) - that's normal.
            logging.exception('got exception executing tranformed tree')
    except (Exception, SystemExit):
        if raise_exceptions:  # pragma: no cover
            raise  # pragma: no cover
        else:
            logging.exception('`got exception executing tranformed tree')
    finally:
        sys.argv = old_sys_argv
        sys.modules['__main__'] = old_main_mod


def get_execution_environment():
    _seerun_saved_values = defaultdict(list)

    def _show_values_internal_save(value, location):
        """Nodes are replaced by calls to this, with original node as arg.

        The original node is evaluated as usual (as the argument, now). Then
        we save the value, and return it so it can play the same role further
        up the call stack that it did originally.
        """
        frames = traceback.extract_stack(sys._getframe().f_back)
        # Unless we skip instrumenting calls we generated, examples where the
        # repr refers to itself lead to infinite recursion, e.g.:
        #   def __repr__(self): return 'HoldsX(%r)' % (self.x,)
        # Also we really only want to instrument the user's calls anyway.
        # (Not ours.)
        if '_show_values_internal_save' not in [frame.name for frame in frames]:
            _seerun_saved_values[location].append(repr(value))
        return value

    return {SAVE_FUNCTION_NAME: _show_values_internal_save,
            '_seerun_saved_values': _seerun_saved_values}
