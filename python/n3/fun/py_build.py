import ast

class PyBuilder:

    def __init__(self):
        pass
    
    def module(self, body):
        return ast.Module(body=body, type_ignores=[])

    def imports(self, module, names):
        imprt = ast.ImportFrom(module=module, names=[ast.alias(name=n) for n in names], level=0)
        ast.fix_missing_locations(imprt)
        
        return imprt

    def fn(self, name, params=[]):
        args = [ast.arg(arg=p) for p in params]

        ret = ast.FunctionDef(
            name=name,
            args=ast.arguments(
                args=args,
                posonlyargs=[], vararg=None, kwarg=None, defaults=[], kwonlyargs=[], kw_defaults=[]
            ),
            body=[],
            decorator_list=[]
        )
        ast.fix_missing_locations(ret)
        
        return ret

    def fn_body_stmt(self, fn, stmt):
        fn.body.append(stmt)

    def fn_body_stmts(self, fn, stmts):
        fn.body.extend(stmts)

    def ref(self, name):
        ret = ast.Name(id=name, ctx=ast.Load())
        ast.fix_missing_locations(ret)
        
        return ret

    def cnst(self, value):
        ret = ast.Constant(value=value)
        ast.fix_missing_locations(ret)
        
        return ret

    def attr_ref(self, var, attr):
        return self.attr_ref_expr(self.ref(var), attr)
    
    def attr_ref_expr(self, expr, attr):
        ret = ast.Attribute(value=expr, attr=attr, ctx=ast.Load())
        ast.fix_missing_locations(ret)
        
        return ret

    def fn_call(self, fn, args=[]):
        ret = ast.Call(func=fn, args=args, keywords=[])
        ast.fix_missing_locations(ret)
        
        return ret

    def lmbda(self, params, expr):
        args = [ast.arg(arg=p) for p in params]

        ret = ast.Lambda(
            args=ast.arguments(
                args=args,
                posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=expr
        )
        ast.fix_missing_locations(ret)
        
        return ret

    def stmt(self, expr):
        ret = ast.Expr(expr)
        ast.fix_missing_locations(ret)
        
        return ret

    def comp(self, op1, cmp, op2):
        match cmp:
            case 'eq': cmp = ast.Eq()
            case 'neq': cmp = ast.NotEq()
            case 'is': cmp = ast.Is()
            case 'is not': cmp = ast.IsNot()
            case _: print("inconceivable"); return

        ret = ast.Compare(left=op1, ops=[cmp], comparators=[op2])
        ast.fix_missing_locations(ret)
        
        return ret

    def noot(self, cond):
        ret = ast.BoolOp(op=ast.Not(), values=cond)
        ast.fix_missing_locations(ret)
        
        return ret

    def conj(self, conds):
        ret = ast.BoolOp(op=ast.And(), values=conds)
        ast.fix_missing_locations(ret)
        
        return ret

    def disj(self, conds):
        ret = ast.BoolOp(op=ast.Or(), values=conds)
        ast.fix_missing_locations(ret)
        
        return ret

    def iif(self, cond, body, ellse=[]):
        ret = ast.If(
            test=cond,
            body=body,
            orelse=ellse)
        ast.fix_missing_locations(ret)
        
        return ret
    
    def pss(self):
        ret = ast.Pass()
        ast.fix_missing_locations(ret)
        
        return ret