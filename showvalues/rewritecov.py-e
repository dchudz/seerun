import ast
import logging
import traceback
from collections import namedtuple

DELETE = 'delete'
NONIFY = 'nonify'


def exec_tree(tree):
    exec(compile(tree, filename="<ast>", mode="exec"), {})

Rewrite = namedtuple('Rewrite', ['lineno', 'type'])


def is_test_node(node):
    return isinstance(node, ast.FunctionDef) and node.name.startswith(
        'test_')


class Deleter(ast.NodeTransformer):
    """Tries Rewrites (but not those in skip_these_rewrites).

    Only considers the first AST node we see for each line number.

    Stops rewriting once any function called "test_<anything>" is found.
    """

    def __init__(self, skip_these_rewrites):
        self.stop_modifying = False
        self.skip_these_mods = skip_these_rewrites
        self.current_rewrite = None  # tuple: lineno, modification type

    def ok_delete(self, node):
        return (
            hasattr(node, 'lineno') and  # Top-level Module node has no lineno
            (node.lineno, DELETE) not in self.skip_these_mods and
            not self.stop_modifying
        )

    def ok_sub_none(self, node):
        return (
            hasattr(node, 'lineno') and  # Top-level Module node has no lineno
            (node.lineno, NONIFY) not in self.skip_these_mods and
            isinstance(node, ast.Call) and
            not self.stop_modifying
        )

    def visit(self, node):
        if is_test_node(node):
            # Once we see a test definition, stop messing with things.
            # (Assumes NodeTransformer searches depth-first, which I think
            # is true.)
            self.stop_modifying = True
            return node
        elif self.ok_delete(node):
            self.current_rewrite = Rewrite(node.lineno, DELETE)
            self.stop_modifying = True
            return None
        elif self.ok_sub_none(node):
            self.current_rewrite = Rewrite(node.lineno, NONIFY)
            self.stop_modifying = True
            return ast.NameConstant(value=None, lineno=node.lineno,
                                    col_offset=node.col_offset)
        else:
            if not self.stop_modifying:
                self.generic_visit(node)
            return node


def find_uncovered(code):
    """Return a set of Rewrites that can be made with no error.

    Once we see a function definition starting with 'test_', we're in the
    'testing' section of the code and we stop trying to delete anything.
    """
    try:
        exec_tree(ast.parse(code))  # Unmodified tree shouldn't have errors.
    except Exception as e:

        raise ValueError('%s\n\n You gave me a file that already has errors!' %
                         traceback.format_exc())

    rewrites_no_fail = set()
    rewrites_tried = set()

    while True:
        tree = ast.parse(code)
        deleter = Deleter(skip_these_rewrites=rewrites_tried)
        deleter.visit(tree)
        if not deleter.current_rewrite:
            break
        rewrites_tried.add(deleter.current_rewrite)
        try:
            exec_tree(tree)
        except Exception:
            logging.info('Got an error from %s:\n%s' %
                         (str(deleter.current_rewrite), traceback.format_exc()))
        else:
            logging.info('No error from %s' % str(deleter.current_rewrite))
            rewrites_no_fail.add(deleter.current_rewrite)

    return rewrites_no_fail
