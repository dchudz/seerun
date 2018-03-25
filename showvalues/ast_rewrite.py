from ast import *


def node_pos_str(node):
    return str(node.first_token.startpos) + 'to' + str(
        node.last_token.endpos)


SAVE_FUNCTION_NAME = '_show_values_internal_save'


class SaveTransformer(NodeTransformer):
    """Replace some nodes with a function call."""
    def visit(self, node):
        self.generic_visit(node)
        # messing with the left side of an assign is bad
        # restrict to certain types helps avoid that
        # better would probably be: just don't explore the left side of
        # an assign
        # TODO: be more liberal!
        ok_types = (BinOp, Call, Compare)
        if isinstance(node, ok_types):
            return Call(func=Name(id=SAVE_FUNCTION_NAME, ctx=Load()),
                        args=[node, Str(node_pos_str(node))], keywords=[])
        else:
            return node