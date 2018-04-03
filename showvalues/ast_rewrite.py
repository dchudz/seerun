import logging
from ast import *  #TODO


def node_pos_str(node):
    return str(node.first_token.startpos) + 'to' + str(
        node.last_token.endpos)


SAVE_FUNCTION_NAME = '_show_values_internal_save'


class SaveTransformer(NodeTransformer):
    """Replace some nodes with a function call."""

    def generic_visit(self, node):
        """A version of generic_visit which never visits the "target" field.

        This avoids messing with the left side of an assignment.
        """
        for field, old_value in iter_fields(node):
            # 'target' and 'targets' are both fieldswe don't want to mess with
            # these two lines are the only change from ast.generic_visit
            if field.startswith('target'):
                logging.debug('not descending into the left side of an assign')
            elif isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, AST):
                        value = self.visit(value)
                        if value is None:
                            continue
                        elif not isinstance(value, AST):
                            new_values.extend(value)
                            continue
                    new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, AST):
                new_node = self.visit(old_value)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node

    def visit(self, node):
        self.generic_visit(node)
        if isinstance(node, expr):
            return Call(func=Name(id=SAVE_FUNCTION_NAME, ctx=Load()),
                        args=[node, Str(node_pos_str(node))], keywords=[])
        else:
            return node