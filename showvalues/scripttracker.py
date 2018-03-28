from asttokens import asttokens

import ast
from .ast_rewrite import SaveTransformer

from .run import run, get_execution_environment


def get_values_from_execution(source, args):
    """Execute the source and return a dictionary mapping source code
    character ranges to values (for nodes whose values we saved)."""

    tree = asttokens.ASTTokens(source, parse=True).tree
    SaveTransformer().visit(tree)
    ast.fix_missing_locations(tree)

    environment = get_execution_environment()
    run(compile(tree, filename="<ast>", mode="exec"), args,
        environment=environment)
    # For simplicity, turn the defaultdict into a dict.
    return dict(environment['_seerun_saved_values'])
