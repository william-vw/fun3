# TODO
from ast import *
from n3.terms import *


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
        # code = [ self.__gen_imports() ] # TODO
        code = self.__terms()
        code += [fn for (head, _, body)
                 in rules for fn in self.__gen_rule(head, body)]

        return Module(body=code, type_ignores=[])

    def __gen_imports(self):
        imprt = ImportFrom(module='n3.terms',
                           names=[alias(name='Iri'), alias(name='Var'), alias(name='Literal')], level=0)
        fix_missing_locations(imprt)

        return imprt

    def __gen_rule(self, head, body):
        self.__cur_params = self.__vars_graph(head)

        return [self.__gen_clause(head, body, i) for i, _ in enumerate(body.model.triples())]

    def __gen_clause(self, head, body, index):
        clause = body.model.triple_at(index)

        own_params = self.__cur_params + ['model', 'state', 'ctu']
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
        #   if variable, refer to the function argument (provided as argument)
        #   else, use resource from clause
        call_args = [self.__builder.ref(r.name) if isinstance(
            r, Var) else self.__construct_call(r) for r in clause]
        call_args += [self.__builder.ref('state'), lmbda]
        model_call = self.__builder.fn_call(
            self.__builder.attr_ref('model', 'find'), call_args)

        # add model call to the function's body
        self.__builder.fn_body_stmt(
            clause_fn, self.__builder.to_stmt(model_call))

        fix_missing_locations(clause_fn)

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

    def __construct_call(self, r):
        match r.type():
            case term_types.IRI:
                cls = "Iri"
                val = r.iri
            case term_types.VAR:
                cls = "Var"
                val = r.name
            case term_types.LITERAL:
                cls = "Literal"
                val = r.value
            case _: print("inconceivable")

        return self.__builder.fn_call(fn=self.__builder.ref(cls), args=[self.__builder.cnst(val)])
    
    # TODO
    def __terms(self):
        terms = [
            ClassDef(
                name='Iri',
                bases=[],
                keywords=[],
                body=[
                    FunctionDef(
                        name='__init__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self'),
                                arg(arg='iri'),
                                arg(arg='label')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[
                                Constant(value=False)]),
                        body=[
                            Assign(
                                targets=[
                                    Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='iri',
                                        ctx=Store())],
                                value=Name(id='iri', ctx=Load())),
                            Assign(
                                targets=[
                                    Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='label',
                                        ctx=Store())],
                                value=Name(id='label', ctx=Load()))],
                        decorator_list=[]),
                    FunctionDef(
                        name='type',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Return(
                                value=Attribute(
                                    value=Name(id='term_types', ctx=Load()),
                                    attr='IRI',
                                    ctx=Load()))],
                        decorator_list=[]),
                    FunctionDef(
                        name='__str__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Return(
                                value=IfExp(
                                    test=UnaryOp(
                                        op=Not(),
                                        operand=Attribute(
                                            value=Name(id='self', ctx=Load()),
                                            attr='label',
                                            ctx=Load())),
                                    body=JoinedStr(
                                        values=[
                                            Constant(value='<'),
                                            FormattedValue(
                                                value=Attribute(
                                                    value=Name(
                                                        id='self', ctx=Load()),
                                                    attr='iri',
                                                    ctx=Load()),
                                                conversion=-1),
                                            Constant(value='>')]),
                                    orelse=Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='iri',
                                        ctx=Load())))],
                        decorator_list=[]),
                    FunctionDef(
                        name='__repr__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Return(
                                value=Call(
                                    func=Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='__str__',
                                        ctx=Load()),
                                    args=[],
                                    keywords=[]))],
                        decorator_list=[])],
                decorator_list=[]),
            ClassDef(
                name='Literal',
                bases=[],
                keywords=[],
                body=[
                    FunctionDef(
                        name='__init__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self'),
                                arg(arg='value')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Assign(
                                targets=[
                                    Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='value',
                                        ctx=Store())],
                                value=Name(id='value', ctx=Load()))],
                        decorator_list=[]),
                    FunctionDef(
                        name='type',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Return(
                                value=Attribute(
                                    value=Name(id='term_types', ctx=Load()),
                                    attr='LITERAL',
                                    ctx=Load()))],
                        decorator_list=[]),
                    FunctionDef(
                        name='__str__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Return(
                                value=Attribute(
                                    value=Name(id='self', ctx=Load()),
                                    attr='value',
                                    ctx=Load()))],
                        decorator_list=[]),
                    FunctionDef(
                        name='__repr__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Return(
                                value=Call(
                                    func=Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='__str__',
                                        ctx=Load()),
                                    args=[],
                                    keywords=[]))],
                        decorator_list=[])],
                decorator_list=[]),
            ClassDef(
                name='var_types',
                bases=[
                    Name(id='Enum', ctx=Load())],
                keywords=[],
                body=[
                    Assign(
                        targets=[
                            Name(id='UNIVERSAL', ctx=Store())],
                        value=Constant(value=0)),
                    Assign(
                        targets=[
                            Name(id='EXISTENTIAL', ctx=Store())],
                        value=Constant(value=1))],
                decorator_list=[]),
            ClassDef(
                name='Var',
                bases=[],
                keywords=[],
                body=[
                    FunctionDef(
                        name='__init__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self'),
                                arg(arg='type'),
                                arg(arg='name')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Assign(
                                targets=[
                                    Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='type',
                                        ctx=Store())],
                                value=Name(id='type', ctx=Load())),
                            Assign(
                                targets=[
                                    Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='name',
                                        ctx=Store())],
                                value=Name(id='name', ctx=Load()))],
                        decorator_list=[]),
                    FunctionDef(
                        name='type',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Return(
                                value=Attribute(
                                    value=Name(id='term_types', ctx=Load()),
                                    attr='VAR',
                                    ctx=Load()))],
                        decorator_list=[]),
                    FunctionDef(
                        name='__str__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Match(
                                subject=Attribute(
                                    value=Name(id='self', ctx=Load()),
                                    attr='type',
                                    ctx=Load()),
                                cases=[
                                    match_case(
                                        pattern=MatchValue(
                                            value=Attribute(
                                                value=Name(
                                                    id='var_types', ctx=Load()),
                                                attr='UNIVERSAL',
                                                ctx=Load())),
                                        body=[
                                            Return(
                                                value=JoinedStr(
                                                    values=[
                                                        Constant(value='?'),
                                                        FormattedValue(
                                                            value=Attribute(
                                                                value=Name(
                                                                    id='self', ctx=Load()),
                                                                attr='name',
                                                                ctx=Load()),
                                                            conversion=-1)]))]),
                                    match_case(
                                        pattern=MatchAs(),
                                        body=[
                                            Return(
                                                value=JoinedStr(
                                                    values=[
                                                        Constant(value='_:'),
                                                        FormattedValue(
                                                            value=Attribute(
                                                                value=Name(
                                                                    id='self', ctx=Load()),
                                                                attr='name',
                                                                ctx=Load()),
                                                            conversion=-1)]))])])],
                        decorator_list=[]),
                    FunctionDef(
                        name='__repr__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self')],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]),
                        body=[
                            Return(
                                value=Call(
                                    func=Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='__str__',
                                        ctx=Load()),
                                    args=[],
                                    keywords=[]))],
                        decorator_list=[])],
                decorator_list=[])
        ]
        
        # TODO
        return [ fix_missing_locations(term) for term in terms ]


class FnBuilder:

    # fn_prefix
    # fn_cnt

    def __init__(self, fn_prefix):
        self.__fn_prefix = fn_prefix
        self.__fn_cnt = 0

    def fn(self, params=[]):
        args = [arg(arg=p) for p in params]

        name = self.__fn_name(self.__fn_cnt)
        self.__fn_cnt += 1

        return FunctionDef(
            name=name,
            args=arguments(
                args=args,
                posonlyargs=[], vararg=None, kwarg=None, defaults=[], kwonlyargs=[], kw_defaults=[]
            ),
            body=[],
            decorator_list=[]
        )

    def fn_body_stmt(self, fn, stmt):
        fn.body.append(stmt)

    def ref(self, name):
        return Name(id=name, ctx=Load())

    def cnst(self, value):
        # TODO escape strings
        return Constant(value=value)

    def attr_ref(self, var, attr):
        return Attribute(value=self.ref(var), attr=attr, ctx=Load())

    def fn_call(self, fn, args):
        return Call(func=fn, args=args, keywords=[])

    def fn_call_arg(self, fn_call, arg):
        fn_call.args.append(arg)

    def lmbda(self, params, expr):
        args = [arg(arg=p) for p in params]

        return Lambda(
            args=arguments(
                args=args,
                posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=expr
        )

    def to_stmt(self, expr):
        return Expr(expr)

    def next_fn_name(self):
        return self.__fn_name(self.__fn_cnt)

    def __fn_name(self, cnt):
        return f"{self.__fn_prefix}_{cnt}"
