import ast
import logging
from ast import *

from asttokens import asttokens

SAVE_FUNCTION_NAME = '_show_values_internal_save'


def node_pos_str(node):
    return str(node.first_token.startpos) + 'to' + str(
        node.last_token.endpos)


class SaveTransformer(ast.NodeTransformer):
    """Replace some nodes with a function call."""
    def visit(self, node):
        self.generic_visit(node)
        # messing with the left side of an assign is bad
        # restrict to certain types helps avoid that
        # better would probably be: just don't explore the left side of
        # an assign
        ok_types = (BinOp, Call, Compare)
        if isinstance(node, ok_types):
            return Call(func=Name(id=SAVE_FUNCTION_NAME, ctx=Load()),
                        args=[node, Str(node_pos_str(node))], keywords=[])
        else:
            return node


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
