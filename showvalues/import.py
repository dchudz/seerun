import ast
import imp
import importlib

import types

import sys

mod = sys.modules['hi'] = types.ModuleType("hi")


tree = ast.parse('aaa = 111')
co = compile(tree, 'hiiii', "exec", dont_inherit=True)
print(mod.__dict__)
exec(co, mod.__dict__)



print(mod)

print(mod.aaa)