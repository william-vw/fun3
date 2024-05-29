from ast import *
from types import *

function_ast = FunctionDef(
    name='f',
    args=arguments(
        args=[], vararg=None, kwarg=None, defaults=[],
        kwonlyargs=[], kw_defaults=[], posonlyargs=[]
    ),
    body=[Return(value=Constant(n=42, lineno=1, col_offset=0), lineno=1, col_offset=0)],
    decorator_list=[],
    lineno=1,
    col_offset=0
)
module_ast = Module(body=[function_ast], type_ignores=[])

module_code = compile(module_ast, "<not_a_file>", "exec")
function_code = [c for c in module_code.co_consts if isinstance(c, CodeType)][0]

f = FunctionType(function_code, {})

print(f())