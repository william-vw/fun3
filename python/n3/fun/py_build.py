import ast

class PyBuilder:
    
    def module(self, body):
        return self.__fix(ast.Module(body=body, type_ignores=[]))        

    def imports(self, module, names):
        return self.__fix(ast.ImportFrom(module=module, names=[self.__fix(ast.alias(name=n)) for n in names], level=0))

    def fn(self, name, params=[]):
        args = [self.__fix(ast.arg(arg=p)) for p in params]

        return self.__fix(ast.FunctionDef(
            name=name,
            args=self.__fix(ast.arguments(
                args=args,
                posonlyargs=[], vararg=None, kwarg=None, defaults=[], kwonlyargs=[], kw_defaults=[]
            )),
            body=[],
            decorator_list=[]
        ))        

    def fn_body_stmt(self, fn, stmt):
        fn.body.append(stmt)

    def fn_body_stmts(self, fn, stmts):
        fn.body.extend(stmts)

    def ref(self, name):
        return self.__fix(ast.Name(id=name, ctx=ast.Load()))

    def cnst(self, value):
        return self.__fix(ast.Constant(value=value))
        
    def lst(self, elts):
        return self.__fix(ast.List(elts = elts, ctx = ast.Load()))
    
    def tple(self, elts):
        return self.__fix(ast.Tuple(elts = elts, ctx = ast.Load()))
    
    def attr_ref(self, var, attr):
        return self.attr_ref_expr(self.ref(var), attr)
    
    def attr_ref_expr(self, expr, attr):
        return self.__fix(ast.Attribute(value=expr, attr=attr, ctx=ast.Load()))
        
    def index(self, expr, nr):
        return self.__fix(ast.Subscript(expr, slice=self.cnst(nr), ctx=ast.Load()))

    def fn_call(self, fn, args=None):
        return self.__fix(ast.Call(func=fn, args=(args if args is not None else []), keywords=[]))
        
    def lmbda(self, params, expr):
        args = [self.__fix(ast.arg(arg=p)) for p in params]

        return self.__fix(ast.Lambda(
            args=self.__fix(ast.arguments(
                args=args,
                posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            )),
            body=expr
        ))

    def stmt(self, expr):
        return self.__fix(ast.Expr(expr))
        
    def comp(self, op1, cmp, op2):
        return self.comps(cmp, [op1, op2])
    
    def comps(self, cmp, ops):
        match cmp:
            case 'eq': cmp = ast.Eq()
            case 'neq': cmp = ast.NotEq()
            case 'gt': cmp = ast.Gt()
            case 'gte': cmp = ast.GtE()
            case 'lt': cmp = ast.Lt()
            case 'lte': cmp = ast.LtE()
            case 'is': cmp = ast.Is()
            case 'is not': cmp = ast.IsNot()
            case _: print("inconceivable"); return
        self.__fix(cmp)
        
        return self.__fix(ast.Compare(left=ops[0], ops=[cmp], comparators=ops[1:]))
        
    def assn(self, var, expr):
        return self.__fix(ast.Assign(targets=[self.__fix(ast.Name(id=var, ctx=ast.Store()))],
                   value=expr))

    def noot(self, cond):
        return self.__fix(ast.BoolOp(op=ast.Not(), values=cond))

    def conj(self, conds):
        if len(conds) > 1:
            return self.__fix(ast.BoolOp(op=ast.And(), values=conds))
        else: 
            return self.__fix(conds[0])

    def disj(self, conds):
        return self.__fix(ast.BoolOp(op=ast.Or(), values=conds))

    def iif(self, cond, body, ellse=None):
        return self.__fix(ast.If(
            test=cond,
            body=body,
            orelse=ellse if ellse is not None else []))
    
    def pss(self):
        return self.__fix(ast.Pass())
    
    # shamelessly adapted from ast.py
    # (got too frustrated to keep using the original version)
    
    def __fix(self, node, lineno=1, col_offset=0, end_lineno=1, end_col_offset=0):
        if 'lineno' in node._attributes:
            node.lineno = lineno
        if 'end_lineno' in node._attributes:
            node.end_lineno = end_lineno
        if 'col_offset' in node._attributes:
            node.col_offset = col_offset
        if 'end_col_offset' in node._attributes:
            node.end_col_offset = end_col_offset
        return node