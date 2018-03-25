import logging
import sys
import types


def run_script(script_to_run, args, environment):
    with open(script_to_run) as script_file:
        script_source = script_file.read()

    # thanks coverage.py!
    old_main_mod = sys.modules['__main__']
    main_mod = types.ModuleType('__main__')
    sys.modules['__main__'] = main_mod
    main_mod.__file__ = script_to_run
    main_mod.__builtins__ = sys.modules['builtins']
    old_sys_argv = sys.argv
    sys.argv = args

    try:
        exec(script_source,
             {**main_mod.__dict__,
              **environment
              }
             )
    except Exception:
        logging.exception('got exception executing tranformed tree')
    finally:
        sys.argv = old_sys_argv
        sys.modules['__main__'] = old_main_mod