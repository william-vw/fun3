import ast
from n3.terms import Var, term_types
from multidict import MultiDict


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
        self.__process_rules(rules)
        # print("pred_idx:", self.__pred_idx)

        return self.__gen_rule_mod(rules)

    def __gen_rule_mod(self, rules):
        code = [self.__gen_imports()]
        code += [fn for i, (head, _, body) in enumerate(rules)
                 for fn in self.__gen_rule(i, head, body)]

        return ast.Module(body=code, type_ignores=[])

    def __gen_imports(self):
        imprt = ast.ImportFrom(module='n3.terms',
                               names=[ast.alias(name='Iri'), ast.alias(name='Var'), ast.alias(name='Literal')], level=0)
        ast.fix_missing_locations(imprt)

        return imprt

    def __gen_rule(self, rule_no, head, body):
        self.__cur_params = self.__vars_graph(head)

        return [self.__gen_clause(rule_no, head, body, i) for i, _ in enumerate(body.model.triples())]

    def __gen_clause(self, rule_no, head, body, clause_no):
        clause = body.model.triple_at(clause_no)

        in_params = self.__cur_params  # incoming parameters representing variables
        # all incoming parameters
        own_params = in_params + ['model', 'state', 'ctu']
        clause_fn = self.__builder.fn(rule_no, clause_no, own_params)

        # running example: clause = ?p :address ?a ; cur_vars = [ p, r ] ; head = ?p a :Person

        # e.g., [ p, a ]
        own_vars = [v for _, v in self.__vars_triple(clause)]

        if clause_no < body.model.len() - 1:
            # e.g., p, r, a
            # (unique but keep ordering)
            ctu_params = list(dict.fromkeys(self.__cur_params + own_vars))
            rest_args = [self.__builder.ref(v)
                         for v in ['model', 'state', 'ctu']]
            self.__cur_params = ctu_params
            # call next clause fn
            ctu_fn = self.__builder.fn_name(rule_no, clause_no+1)
        else:
            # e.g., p
            ctu_params = self.__vars_graph(head)
            rest_args = [self.__builder.ref('state')]
            # at the last clause, so call the original ctu
            ctu_fn = 'ctu'

        # e.g., { 'p' : 's', 'a': 'o' }
        clause_vars = {v: i for i, v in self.__vars_triple(clause)}

        # arguments to be passed to ctu
        # if next is clause: e.g., att_ref(t.s), ref(r), att_ref(t.o)
        # if next is head: e.g., att_ref(t.s)
        pass_args = [self.__builder.attr_ref('t', clause_vars[p]) if p in clause_vars else self.__builder.ref(p)
                     for p in ctu_params]

        # - find matching triples

        # model.find will call a lambda
        # this lambda will itself call a ctu

        # first, build the ctu call
        call_args = pass_args + rest_args
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
                call_args.append(self.__cnstr_call(r))

        call_args += [self.__builder.ref('state'), lmbda]
        search_call = self.__builder.fn_call(
            self.__builder.attr_ref('model', 'find'), call_args)

        # add search call to the function's body
        self.__builder.fn_body_stmt(
            clause_fn, self.__builder.to_stmt(search_call))

        # - call matching rule fns
        matches = self.__matching_rules(clause)
        print("match", clause.p, matches)

        # TODO blank nodes vs. universals

        match_conds = []; match_args = []; lmbda_params = [], ok = True
        for match in matches:
            match_clause = match.rule.head.triples()[0]
            
            for pos in range(3):
                match_r = match_clause[pos]; clause_r = clause[pos]
                if match_r.is_concrete():
                    if clause_r.is_concrete():
                        if clause_r != match_r:  # compile-time check
                            ok = False
                            break
                    else:  # add runtime check, if variable is incoming param
                        if clause_r.name in in_params:
                            cmp1 = self.__builder.comp(self.__builder.ref(
                                clause_r.name), 'is', self.__builder.cnst(None))
                            cmp2 = self.__builder.comp(self.__builder.ref(
                                clause_r.name)), 'eq', self.__cnstr_call(match_r)
                            match_conds.append(self.__builder.disj([cmp1, cmp2]))
                
                else: # values will be passed as lambda parameters
                    if clause_r.is_concrete():
                        lmbda_params.append('_') # don't care about value (will be same)
                        match_args.append(self.__cnstr_call(clause_r))
                    else:
                        lmbda_params.append(clause_r.name) # (same as ctu_param)
                        if clause_r.name in in_params:
                            match_args.append(
                                self.__builder.ref(clause_r.name))
                        else:
                            match_args.append(self.__builder.cnst(None))

            if ok:
                call_args = [self.__builder.ref(p) for p in ctu_params] + rest_args
                ctu_call = self.__builder.fn_call(
                    self.__builder.ref(ctu_fn), call_args)

                lmbda_params.append('state')
                lmbda = self.__builder.lmbda(lmbda_params, ctu_call)

                match_args += [self.__builder.ref('model'),
                               self.__builder.ref('state'), lmbda]
                match_call = self.__builder.to_stmt(self.__builder.fn_call(
                    self.__builder.ref(match.fn_name), match_args))

                if len(match_conds) > 0:
                    match_call = self.__builder.ifc(
                        self.__builder.conj(match_conds), match_call)

                self.__builder.fn_body_stmt(
                    clause_fn, self.__builder.to_stmt(match_call))

        ast.fix_missing_locations(clause_fn)

        return clause_fn

    def __matching_rules(self, clause):
        if clause.p.type() == term_types.VAR:
            return self.__pred_idx.getall('all')

        ret = []
        if clause.p.idx_val() in self.__pred_idx:
            ret.append(self.__pred_idx.getall(clause.p.idx_val()))
        if 'var' in self.__pred_idx:
            ret += self.__pred_idx.getall('var')
        return ret

    def __process_rules(self, rules):
        self.__pred_idx = MultiDict()

        i = 0
        while i < len(rules):
            r = rules[i]
            if r.s.model.len() != 1:
                print(f"warning: cannot use rule, length of head > 1 ({r})")
                del rules[i]
                continue

            entry = FnEntry(r, self.__builder.fn_name(i, 0))
            for t in r.s.model.triples():
                if t.p.type() == term_types.VAR:
                    self.__pred_idx.add('var', entry)
                else:
                    self.__pred_idx.add(t.p.idx_val(), entry)
                self.__pred_idx.add('all', entry)

            i += 1

    def __vars_graph(self, graph):
        return [v for t in graph.model.triples() for _, v in self.__vars_triple(t)]

    def __vars_triple(self, t):
        spo = ['s', 'p', 'o']
        for i, r in enumerate(t):
            if isinstance(r, Var):
                yield spo[i], r.name

    def __cnstr_call(self, r):
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


class FnEntry:

    # rule (triple)
    # fn_name

    def __init__(self, rule, fn_name):
        self.rule = rule
        self.fn_name = fn_name

    def __str__(self):
        return f"<{self.fn_name} - {str(self.rule)}>"

    def __repr__(self):
        return self.__str__()


class FnBuilder:

    # fn_prefix

    def __init__(self, fn_prefix):
        self.__fn_prefix = fn_prefix

    def fn(self, rule_no, clause_no, params=[]):
        name = self.fn_name(rule_no, clause_no)
        args = [ast.arg(arg=p) for p in params]

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

    def comp(self, op1, cmp, op2):
        match cmp:
            case 'eq': cmp = ast.Eq()
            case 'neq': cmp = ast.NotEq()
            case 'is': cmp = ast.Is()
            case _: print("inconceivable")
            return

        return ast.Compare(left=op1, ops=[cmp], comparators=[op2]),

    def conj(self, conds):
        return ast.BoolOp(op=ast.And(), values=conds)

    def disj(self, conds):
        return ast.BoolOp(op=ast.Or(), values=conds)

    def ifc(self, cond, body):
        return ast.If(
            test=cond,
            body=body,
            orelse=[])

    def fn_name(self, rule_no, clause_no):
        if clause_no == 0:
            return f"{self.__fn_prefix}_{rule_no}"
        else:
            return f"{self.__fn_prefix}_{rule_no}_{clause_no}"
