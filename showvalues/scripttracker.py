import logging

from asttokens import asttokens

import ast
from .ast_rewrite import SAVE_FUNCTION_NAME, SaveTransformer, node_pos_str


def get_values_from_execution(source):
    """Execute the source and return a dictionary mapping source code
    character ranges to values (for nodes whose values we saved)."""
    _values = {}

    def save_and_return(value, location):
        """Nodes are replaced by calls to this, with original node as arg.

        The original node is evaluated as usual (as the argument, now). Then
        we save the value, and return it so it can play the same role further
        up the call stack that it did originally.
        """
        _values[location] = repr(value)
        return value

    def exec_tree(tree):
        exec(compile(tree, filename="<ast>", mode="exec"),
             {SAVE_FUNCTION_NAME: save_and_return,
              '_values': _values}
             )

    tree = asttokens.ASTTokens(source, parse=True).tree
    SaveTransformer().visit(tree)
    ast.fix_missing_locations(tree)
    try:
        exec_tree(tree)
    except Exception:
        logging.exception('got exception executing tranformed tree')

    return _values
