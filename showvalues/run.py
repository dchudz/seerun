import logging
import sys
import types


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
    except Exception:
        logging.exception('got exception executing tranformed tree')
    finally:
        sys.argv = old_sys_argv
        sys.modules['__main__'] = old_main_mod