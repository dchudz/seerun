"""Thanks coverage.py"""
import logging
import sys
import types
import importlib
import importlib.util


import os

NoSource = Exception

def find_module(modulename):
    """Find the module named `modulename`.

    Returns the file path of the module, and the name of the enclosing
    package.
    """
    try:
        spec = importlib.util.find_spec(modulename)
    except ImportError as err:
        raise NoSource(str(err))
    if not spec:
        raise NoSource("No module named %r" % (modulename,))
    pathname = spec.origin
    packagename = spec.name
    if pathname.endswith("__init__.py") and not modulename.endswith("__init__"):
        mod_main = modulename + ".__main__"
        spec = importlib.util.find_spec(mod_main)
        if not spec:
            raise NoSource(
                "No module named %s; "
                "%r is a package and cannot be directly executed"
                % (mod_main, modulename)
            )
        pathname = spec.origin
        packagename = spec.name
    packagename = packagename.rpartition(".")[0]
    return pathname, packagename


def run_python_module(modulename, args, environment):
    """Run a Python module, as though with ``python -m name args...``.

    `modulename` is the name of the module, possibly a dot-separated name.
    `args` is the argument array to present as sys.argv, including the first
    element naming the module being executed.

    """
    args = list(args)
    pathname, packagename = find_module(modulename)

    pathname = os.path.abspath(pathname)
    print(pathname)
    print(args)
    args[0] = pathname
    print(pathname)
    run_python_file(pathname, args, environment, package=packagename,
                    modulename=modulename, path0="")


def run_python_file(path, args, environment, package=None, modulename=None,
                    path0=None):
    with open(path) as file:
        source = file.read()
    run(source, args, environment, path=path)


def run(script_source_or_compiled, args, environment, path=None):
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
    except (Exception, SystemExit):  # don't want pytest exiting on us!!
        logging.exception('got exception executing tranformed tree')
    # TODO: no message for SystemExit(1)
    finally:
        sys.argv = old_sys_argv
        sys.modules['__main__'] = old_main_mod
