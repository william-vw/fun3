import ast
from n3.terms import Var, term_types


def gen_py(rules):
    gen = GenPython()
    return gen.gen_python(rules)


class GenPython:

    # __builder
    # __pred_idx
    # __cur_params

    def __init__(self):
        self.__builder = FnBuilder("rule")

    def gen_python(self, rules):
        # self.__pred_idx = self.__build_pred_idx(rules)

        return self.__gen_rule_mod(rules)

    def __gen_rule_mod(self, rules):
        code = [self.__gen_imports()]
        code += [fn for (head, _, body)
                 in rules for fn in self.__gen_rule(head, body)]

        return ast.Module(body=code, type_ignores=[])

    def __gen_imports(self):
        imprt = ast.ImportFrom(module='n3.terms',
                               names=[ast.alias(name='Iri'), ast.alias(name='Var'), ast.alias(name='Literal')], level=0)
        ast.fix_missing_locations(imprt)

        return imprt

    def __gen_rule(self, head, body):
        self.__cur_params = self.__vars_graph(head)

        return [self.__gen_clause(head, body, i) for i, _ in enumerate(body.model.triples())]

    def __gen_clause(self, head, body, index):
        clause = body.model.triple_at(index)

        in_params = self.__cur_params
        own_params = in_params + ['model', 'state', 'ctu']
        clause_fn = self.__builder.fn(own_params)

        # running example: clause = ?p :address ?a ; cur_vars = [ p, r ] ; head = ?p a :Person

        # e.g., [ p, a ]
        own_vars = [v for _, v in self.__vars_triple(clause)]

        if index < body.model.len() - 1:
            # e.g., p, r, a
            # unique but keep ordering
            ctu_params = list(dict.fromkeys(self.__cur_params + own_vars))
            self.__cur_params = ctu_params
            # call next clause fn
            ctu_fn = self.__builder.next_fn_name()
        else:
            # e.g., p
            ctu_params = self.__vars_graph(head)
            # at the last clause, so call the original ctu
            ctu_fn = 'ctu'

        # e.g., { 'p' : 's', 'a': 'o' }
        clause_vars = {v: i for i, v in self.__vars_triple(clause)}

        # if next is clause: e.g., att_ref(t.s), ref(r), att_ref(t.o)
        # if next is head: e.g., att_ref(t.s)
        pass_args = [self.__builder.attr_ref('t', clause_vars[p]) if p in clause_vars else self.__builder.ref(p)
                     for p in ctu_params]

        # model.find will call a lambda
        # this lambda will itself call a ctu

        # first, build the ctu call
        call_args = pass_args + [self.__builder.ref(v)
                                 for v in (['model', 'state', 'ctu'] if index < body.model.len() - 1 else ['state'])]
        ctu_call = self.__builder.fn_call(
            self.__builder.ref(ctu_fn), call_args)

        # then, create lambda with as body the ctu call
        lmbda = self.__builder.lmbda(['t', 'state'], ctu_call)

        # finally, create model.find call

        # s, p, o from clause will be search terms
        #   if variable: if provided as argument, refer to the function argument, else None
        #   else, use resource from clause
        call_args = []
        for r in clause:
            if isinstance(r, Var):
                if r.name in in_params:
                    call_args.append(self.__builder.ref(r.name))
                else:
                    call_args.append(self.__builder.cnst(None))
            else:
                call_args.append(self.__cnstor_call(r))

        call_args += [self.__builder.ref('state'), lmbda]
        model_call = self.__builder.fn_call(
            self.__builder.attr_ref('model', 'find'), call_args)

        # add model call to the function's body
        self.__builder.fn_body_stmt(
            clause_fn, self.__builder.to_stmt(model_call))

        ast.fix_missing_locations(clause_fn)

        return clause_fn

    # def __build_pred_idx(self, rules):
    #     pred_idx = {}
    #     for r in rules:
    #         if r.p == "<=":
    #             for t in r.s:
    #                 pred_idx[t.p] = r
    #     return pred_idx

    def __vars_graph(self, graph):
        return [v for t in graph.model.triples() for _, v in self.__vars_triple(t)]

    def __vars_triple(self, t):
        spo = ['s', 'p', 'o']
        for i, r in enumerate(t):
            if isinstance(r, Var):
                yield spo[i], r.name

    def __cnstor_call(self, r):
        match r.type():
            case term_types.IRI:
                cls = "Iri"
                args = [r.iri, r.label]
            case term_types.VAR:
                cls = "Var"
                args = [r.name]
            case term_types.LITERAL:
                cls = "Literal"
                args = [r.value]
            case _: print("inconceivable")

        return self.__builder.fn_call(fn=self.__builder.ref(cls), args=[self.__builder.cnst(a) for a in args])


class FnBuilder:

    # fn_prefix
    # fn_cnt

    def __init__(self, fn_prefix):
        self.__fn_prefix = fn_prefix
        self.__fn_cnt = 0

    def fn(self, params=[]):
        args = [ast.arg(arg=p) for p in params]

        name = self.__fn_name(self.__fn_cnt)
        self.__fn_cnt += 1

        return ast.FunctionDef(
            name=name,
            args=ast.arguments(
                args=args,
                posonlyargs=[], vararg=None, kwarg=None, defaults=[], kwonlyargs=[], kw_defaults=[]
            ),
            body=[],
            decorator_list=[]
        )

    def fn_body_stmt(self, fn, stmt):
        fn.body.append(stmt)

    def ref(self, name):
        return ast.Name(id=name, ctx=ast.Load())

    def cnst(self, value):
        # TODO escape strings
        return ast.Constant(value=value)

    def attr_ref(self, var, attr):
        return ast.Attribute(value=self.ref(var), attr=attr, ctx=ast.Load())

    def fn_call(self, fn, args=[]):
        return ast.Call(func=fn, args=args, keywords=[])

    def lmbda(self, params, expr):
        args = [ast.arg(arg=p) for p in params]

        return ast.Lambda(
            args=ast.arguments(
                args=args,
                posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=expr
        )

    def to_stmt(self, expr):
        return ast.Expr(expr)

    def next_fn_name(self):
        return self.__fn_name(self.__fn_cnt)

    def __fn_name(self, cnt):
        return f"{self.__fn_prefix}_{cnt}"
