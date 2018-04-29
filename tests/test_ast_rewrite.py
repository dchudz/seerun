import ast
import asttokens

from seerun.ast_rewrite import SaveTransformer


def get_targets(tree):
    """`Assign` nodes have a targets field that's a list."""
    [assign_node] = tree.body
    [target] = assign_node.targets
    return target


def get_target(tree):
    """`For` nodes have a  """
    [assign_node] = tree.body
    return assign_node.target


def test_dont_rewrite_left_of_equals():
    tree = asttokens.ASTTokens('a = 1', parse=True).tree
    old_target = get_targets(tree)
    SaveTransformer().visit(tree)
    assert old_target == get_targets(tree)


def test_dont_rewrite_assignee_of_for():
    tree = asttokens.ASTTokens('for i in [1,2]: print(i)', parse=True).tree
    old_target = get_target(tree)
    SaveTransformer().visit(tree)
    assert old_target == get_target(tree)
