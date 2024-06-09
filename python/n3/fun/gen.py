from collections import Counter
from multidict import MultiDict
from n3.fun.py_build import PyBuilder
from n3.terms import Var, term_types
from n3.ns import n3Log, swapNs


def gen_py(rules):
    gen = GenPython()
    return gen.gen_python(rules)


class GenError(Exception):
    pass


class GenPython:

    # __builder
    # __fn_prefix
    # __pred_idx
    # __cur_params
    # __extra_params

    def __init__(self):
        self.__builder = PyBuilder()
        self.__fn_prefix = "rule"
        self.__extra_params = [ 'data', 'state', 'ctu' ]

    def gen_python(self, rules):
        self.__process_rules(rules)
        # print("pred_idx:", self.__pred_idx)

        return self.__gen_rule_mod(rules)

    def __gen_rule_mod(self, rules):
        code = [self.__gen_imports()]
        code += [fn for i, (head, _, body) in enumerate(rules)
                 for fn in self.__gen_rule(i, head, body)]

        return self.__builder.module(code)

    def __gen_imports(self):
        return self.__builder.imports('n3.terms', ['Iri', 'Var', 'Literal'])

    def __gen_rule(self, rule_no, head, body):
        if head.type() == term_types.GRAPH:
            self.__cur_params = self.__vars_graph(head)

            if body.type() == term_types.GRAPH:
                return [self.__gen_clause(rule_no, head, body, i) for i, _ in enumerate(body.model.triples())]

            elif body.type() == term_types.LITERAL and body.value == True:
                return [self.__gen_clause(rule_no, head, None, 0)]

    def __gen_clause(self, rule_no, head, body, clause_no):
        # unification taking place in rule head
        # (may modify cur_params)
        unify_stmts = self.__unify_head() if clause_no == 0 and len(
            self.__cur_params) != len(set(self.__cur_params)) else None

        # incoming parameters representing variables
        in_params = self.__cur_params
        # all incoming parameters
        own_params = in_params + self.__extra_params

        # function representing this clause
        clause_fn = self.__builder.fn(
            self.__fn_name(rule_no, clause_no), own_params)

        # running example: clause = ?p :address ?a ; cur_vars = [ p, r ] ; head = ?p a :Person

        # e.g., boolean as body
        if body is None:
            if unify_stmts is not None:
                self.__builder.fn_body_stmts(clause_fn, unify_stmts)
            else:
                self.__builder.fn_body_stmt(clause_fn, self.__builder.pss())
            return clause_fn

        clause = body.model.triple_at(clause_no)

        # ex: [ p, a ]
        own_vars = [v for _, v in self.__vars_triple(clause)]

        if clause_no < body.model.len() - 1:
            # parameters for the ctu function; unique(prior + own vars)
            # ex: p, r, a
            ctu_params = list(dict.fromkeys(
                self.__cur_params + own_vars))  # keep order
            # rest of ctu args (unrelated to vars)
            rest_args = [self.__builder.ref(v) for v in self.__extra_params]
            self.__cur_params = ctu_params
            # call next clause fn
            ctu_fn = self.__fn_name(rule_no, clause_no+1)
        else:
            # only pass var needed by original ctu fn (head vars!)
            # ex: p
            ctu_params = self.__vars_graph(head)
            # rest of ctu args (unrelated to vars)
            rest_args = [self.__builder.ref('state')]
            # at the last clause, so call the original ctu
            ctu_fn = 'ctu'

        # if self.__is_builtin(clause):
        #     self.__run_builtin(clause_fn, clause, in_params, ctu_fn, ctu_params, rest_args)
        # else:
        self.__find_triple_call(
            clause_fn, clause, in_params, ctu_fn, ctu_params, rest_args)
        self.__match_rule_calls(
            clause_fn, clause, in_params, ctu_fn, ctu_params, rest_args)

        return clause_fn

    def __unify_head(self):
        dupl_params = self.__deduplicate_params()
        # print("dupl_params:", dupl_params)

        body = []
        self.__unify_vars(dupl_params, 0, [], [], body)

        return body

    def __deduplicate_params(self):
        counts = Counter(self.__cur_params)
        ren_params = []; dupl_params = []
        for p in self.__cur_params:
            if counts[p] > 1:
                np = f"{p}{len(dupl_params)}"
                ren_params.append(np); dupl_params.append(np)
            else:
                ren_params.append(p)
        self.__cur_params = ren_params
        
        return dupl_params
    
    def __unify_vars(self, vars, idx, bound, unbound, body):
        bld = self.__builder; var = vars[idx]
        
        if_body = []; else_body = []
        body.append(bld.iif(bld.comp(bld.ref(var), 'is not', bld.cnst(None)), if_body, else_body))
        
        if len(bound) > 0:
            if_body2 = []
            if_body.append(bld.iif(bld.comp(bld.ref(bound[-1]), 'eq', bld.ref(var)), if_body2))
            if_body = if_body2
            
        bound.append(var)
        if idx+1 < len(vars):
            self.__unify_vars(vars, idx+1, bound[:], unbound[:], if_body)
        else:
            if_body.append(bld.stmt(bld.fn_call(bld.ref('ctu'), self.__unify_ctu_args(bld, vars, bound))))
        
        bound.pop()
        unbound.append(var)
        
        if idx+1 < len(vars):
            self.__unify_vars(vars, idx+1, bound[:], unbound[:], else_body)
        elif len(bound) > 0:
            else_body.append(bld.stmt(bld.fn_call(bld.ref('ctu'), self.__unify_ctu_args(bld, vars, bound))))

    def __unify_ctu_args(self, bld, vars, bound):
        return [ bld.ref(var) if var in bound else bld.ref(bound[0]) for var in vars ] + [ bld.ref('state') ]
    
    def __find_triple_call(self, clause_fn, clause, in_params, ctu_fn, ctu_params, rest_args):
        # ex: { 'p' : 's', 'a': 'o' }
        clause_vars = {v: i for i, v in self.__vars_triple(clause)}

        # arguments to be passed to ctu
        # if next is clause: ex: att_ref(t.s), ref(r), att_ref(t.o)
        # if next is head: ex: att_ref(t.s)
        var_args = [self.__triple_val('t', clause_vars[p]) if p in clause_vars else self.__builder.ref(p)
                     for p in ctu_params]

        # model.find will call a lambda
        # this lambda will itself call a ctu

        # first, build the ctu call
        call_args = var_args + rest_args
        ctu_call = self.__builder.fn_call(self.__builder.ref(ctu_fn), call_args)

        # then, create lambda with as body the ctu call
        lmbda = self.__builder.lmbda(['t', 'state'], ctu_call)

        # finally, create model.find call

        # s, p, o from clause will be search terms
        #   if variable: if provided as argument, refer to the function argument, else None
        #   else, use resource from clause
        call_args = []
        for r in clause:
            if isinstance(r, Var):
                varname = self.__safe_var(r.name)
                if varname in in_params:
                    call_args.append(self.__var_ref(varname))
                else:
                    call_args.append(self.__builder.cnst(None))
            else:
                call_args.append(self.__val(r))

        call_args += [self.__builder.ref('state'), lmbda]
        search_call = self.__builder.fn_call(
            self.__builder.attr_ref('data', 'find'), call_args)

        self.__builder.fn_body_stmt(
            clause_fn, self.__builder.stmt(search_call))
    
    def __match_rule_calls(self, clause_fn, clause, in_params, ctu_fn, ctu_params, rest_args):
        #print("matching:", clause)
        matches = self.__matching_rules(clause)

        # TODO blank nodes vs. universals

        for match in matches:
            
            # TODO deal with recursion
            if match.fn_name == clause_fn.name:
                #print(f"warning: avoiding recursion in {match.fn_name}")
                continue;
            
            # arguments to be passed to ctu
            # (can be updated by code below)
            call_args = [ self.__builder.ref(p) for p in ctu_params ]
            
            match_conds = []; match_args = []; lmbda_params = []; ok = True
            #print("match:", match.rule.s)
            
            head = match.rule.s
            match_clause = head.model.triples()[0]
            
            for pos in range(3):
                match_r = match_clause[pos]; clause_r = clause[pos]
                #print(f"{match_r} <> {clause_r}")
                
                if match_r.is_concrete():
                    if clause_r.is_concrete():
                        if clause_r != match_r:  # compile-time check
                            #print("compile-time check: nok")
                            ok = False; break
                    else:
                        clause_varname = self.__safe_var(clause_r.name)
                        # add runtime check, if possible
                        if clause_varname in in_params:
                            cmp1 = self.__builder.comp(self.__var_ref(clause_varname), 
                                                       'is', self.__builder.cnst(None))
                            cmp2 = self.__builder.comp(self.__var_ref(clause_varname), 'eq', self.__val(match_r))
                            match_conds.append(self.__builder.disj([cmp1, cmp2]))

                        # clause has variable; match rule has concrete value
                        # if successful, pass concrete value to ctu (ex 3), if needed
                        # (get arg index from ctu_params)
                        if clause_varname in ctu_params:
                            call_args[ctu_params.index(clause_varname)] = self.__val(match_r)
                
                else: # values will be passed as lambda parameters
                    if clause_r.is_concrete():
                        # not a variable so is not needed in ctu
                        lmbda_params.append('_')
                        match_args.append(self.__val(clause_r))
                    else:
                        clause_varname = self.__safe_var(clause_r.name)
                        # ex 1-4 (p<>p, p<>pe, t<>ty)
                        # always get value from match clause / find call; 
                        # either we gave None, or it is the same as what we gave
                        # (use our var's name, as it is same as ctu_param)
                        lmbda_params.append(clause_varname)
                        if clause_varname in in_params:
                            match_args.append(self.__var_ref(clause_varname))
                        else: # ex 4
                            match_args.append(self.__builder.cnst(None))

            # print(f"ok? {ok}")
            if ok:
                # print("match_conds:", match_conds, "match_args:", match_args, "lmbda_params:", lmbda_params)
                call_args += rest_args
                ctu_call = self.__builder.fn_call(
                    self.__builder.ref(ctu_fn), call_args)

                # lambda params: useful vars from matching clause
                lmbda_params.append('state') # (add rest param)
                lmbda = self.__builder.lmbda(lmbda_params, ctu_call)

                # match args: args we pass to match fn call
                match_args += [self.__builder.ref('data'),
                               self.__builder.ref('state'), lmbda]
                match_call = self.__builder.stmt(self.__builder.fn_call(
                    self.__builder.ref(match.fn_name), match_args))

                # if needed, wrap in runtime conditional
                if len(match_conds) > 0:
                    match_call = self.__builder.iif(
                        self.__builder.conj(match_conds), match_call)

                self.__builder.fn_body_stmt(clause_fn, match_call)
        #     print()
        # print()

    def __matching_rules(self, clause):
        if clause.p.type() == term_types.VAR:
            return self.__pred_idx.getall('all')

        ret = []
        if clause.p.idx_val() in self.__pred_idx:
            ret.extend(self.__pred_idx.getall(clause.p.idx_val()))
        if 'var' in self.__pred_idx:
            ret.extend(self.__pred_idx.getall('var'))
        return ret

    def __process_rules(self, rules):
        self.__pred_idx = MultiDict()

        i = 0
        while i < len(rules):
            r = rules[i]
            if r.s.model.len() != 1:
                print(f"warning: cannot use rule, length of head > 1 ({r})")
                del rules[i]; continue
            if r.p.iri == n3Log['implies']:
                print(f"warning: cannot use bottom-up rule ({r})")
                del rules[i]; continue

            entry = FnEntry(r, self.__fn_name(i, 0))
            for t in r.s.model.triples():
                if t.p.type() == term_types.VAR:
                    self.__pred_idx.add('var', entry)
                else:
                    self.__pred_idx.add(t.p.idx_val(), entry)
                self.__pred_idx.add('all', entry)

            i += 1
            
    # def __is_builtin(self, clause):
    #     return clause.p.type() == term_types.IRI and clause.p.ns.startswith(swapNs.iri)
    
    # def __run_builtin(self, clause_fn, clause, in_params, ctu_fn, ctu_params, rest_args):
    #     match clause.p.ln:
    #         case 'notEqualTo': ...
    #         case _: raise GenError(f"unsupported builtin: '{clause.p.ln}'")
            
    # helper functions

    def __vars_graph(self, graph):
        ret = []
        for t in graph.model.triples():
            for r in t:
                match (r.type()):
                    case term_types.VAR: 
                        ret.append(self.__safe_var(r.name))
                    case term_types.COLLECTION: 
                        ret.extend(self.__safe_var(v.name) for v in r._vars())
        return ret

    def __vars_triple(self, t):
        spo = ['s', 'p', 'o']
        for i, r in enumerate(t):
            if isinstance(r, Var):
                yield spo[i], self.__safe_var(r.name)
                
    def __safe_var(self, n):
        match n:
            case 't': return 'tt'
            case 'data': return 'ddata'
            case 'state': return 'sstate'
            case 'ctu': return 'cctu'
            case _: return n

    # def __cnstr_call(self, r):
    #     match r.type():
    #         case term_types.IRI: cls = "Iri"
    #         case term_types.VAR: cls = "Var"
    #         case term_types.LITERAL: cls = "Literal"
    #         case _: print("inconceivable")
    #     arg = r.idx_val()

    #     return self.__builder.fn_call(fn=self.__builder.ref(cls), args=[self.__builder.cnst(arg)])

    def __val(self, r):
        return self.__builder.cnst(r.idx_val())
    
    def __var_ref(self, name):
        return self.__builder.ref(name)
    
    def __triple_val(self, t, spo):
        return self.__builder.fn_call(self.__builder.attr_ref_expr(self.__builder.attr_ref(t, spo), 'idx_val'))

    def __fn_name(self, rule_no, clause_no):
        if clause_no == 0:
            return f"{self.__fn_prefix}_{rule_no}"
        else:
            return f"{self.__fn_prefix}_{rule_no}_{clause_no}"

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