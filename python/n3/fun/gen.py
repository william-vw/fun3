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
    # __cur_vars
    # __inner_fn_params (+ __inner_fn_args)
    # __rule_fn_params (+ __rule_fn_args)

    def __init__(self):
        self.__builder = PyBuilder()
        self.__fn_prefix = "rule"
        
        self.__inner_fn_params = [ 'data', 'state', 'ctu' ]
        self.__rule_fn_params = [ 'state' ]
        self.__inner_fn_args = [self.__builder.ref(v) for v in self.__inner_fn_params]
        self.__rule_fn_args = [self.__builder.ref(v) for v in self.__rule_fn_params]

    def gen_python(self, rules):
        self.__process_rules(rules)
        # print("pred_idx:", self.__pred_idx)

        return self.__gen_rule_mod(rules)

    def __gen_rule_mod(self, rules):
        self.__code = [self.__gen_imports()]
        
        # will add corresponding functions to 'code'
        for i, (head, _, body) in enumerate(rules):
            self.__gen_rule(i, head, body)

        return self.__builder.module(self.__code)

    def __gen_imports(self):
        return self.__builder.imports('n3.terms', ['Iri', 'Var', 'Literal', 'Collection', 'term_types'])

    def __gen_rule(self, rule_no, head, body):
        self.__setup_rule_vars(head, body)
        
        if head.type() == term_types.GRAPH:
            self.__cur_vars = self.__vars_graph(head)

            if body.type() == term_types.GRAPH:
                for i, _ in enumerate(body.model.triples()):
                    self.__gen_clause(rule_no, head, body, i)

            elif body.type() == term_types.LITERAL and body.value == True:
                self.__gen_clause(rule_no, head, None, 0)

    def __setup_rule_vars(self, head, body):
        self.__all_rule_vars = { v: True for v in head._vars() }
        
        if body is not None and body.type() == term_types.GRAPH:
            self.__all_rule_vars.update({ v: True for v in body._vars() })

    def __gen_clause(self, rule_no, head, body, clause_no):        
        # in case unification is taking place in rule head
        # (may modify self.__cur_vars)
        do_unify_head = clause_no == 0 and len(self.__cur_vars) != len(set(self.__cur_vars))
        unify_stmts = self.__unify_head() if do_unify_head else None
        
        # incoming parameters representing variables
        in_vars = self.__cur_vars

        # function representing this clause
        clause_fn = self.__rule_fn_def(self.__fn_name(rule_no, clause_no), in_vars)

        # running example: clause = ?p :address ?a ; cur_vars = [ p, r ] ; head = ?p a :Person

        # e.g., boolean as body
        if body is None:
            if unify_stmts is not None:
                self.__builder.fn_body_stmts(clause_fn, unify_stmts)
            else:
                self.__builder.fn_body_stmt(clause_fn, self.__builder.pss())
            self.__code.append(clause_fn); 
            return

        clause = body.model.triple_at(clause_no)

        # ex: [ p, a ]
        own_vars = [v for v in self.__vars_triple(clause)]

        if clause_no < body.model.len() - 1:
            # parameters for the ctu function; unique(prior + own vars) ; ex: p, r, a
            ctu_vars = list(dict.fromkeys(self.__cur_vars + own_vars)) # (keep order)
            self.__cur_vars = ctu_vars
            # call next clause fn
            ctu_fn_name = self.__fn_name(rule_no, clause_no+1)
        else:
            # only pass var needed by original ctu fn (head vars!) ; ex: p
            ctu_vars = self.__vars_graph(head)
            # at the last clause, so call the original ctu
            ctu_fn_name = 'ctu'

        clause_fn = RuleFn(clause_fn.name, in_vars, clause_fn)
        ctu_fn = RuleFn(ctu_fn_name, ctu_vars, None)

        # if self.__is_builtin(clause):
        #     self.__run_builtin(clause_fn, clause, in_vars, ctu_fn, ctu_vars)
        # else:
        self.__find_triple_call(clause, clause_fn, ctu_fn)
        self.__match_rule_calls(clause, clause_fn, ctu_fn)

        self.__code.append(clause_fn.fn)
        
    # 1/ ok if all _provided_ (de-)duplicated vars are same
    # 2/ pass provided var values for non-provided vars
    def __unify_head(self):
        dupl_vars = self.__deduplicate_vars()
        # print("dupl_vars:", dupl_vars)

        body = []
        self.__unify_vars(dupl_vars, 0, [], [], body)

        return body

    # 1/ returns duplicate vars in head
    # 2/ sets __cur_vars to renamed vars w/o duplicates 
    #  e.g., (p, p, s) -> duplicates=(p0, p1), cur_vars=(p0, p1, s)
    def __deduplicate_vars(self):
        counts = Counter(self.__cur_vars)
        ren_vars = []; dupl_vars = []
        for p in self.__cur_vars:
            if counts[p] > 1:
                np = f"{p}{len(dupl_vars)}"
                ren_vars.append(np); dupl_vars.append(np)
            else:
                ren_vars.append(p)
        self.__cur_vars = ren_vars
        
        return dupl_vars
    
    # bound: vars that are bound at this point; unbound: idem for unbound vars
    def __unify_vars(self, vars, idx, bound, unbound, body):
        bld = self.__builder; var = vars[idx]
        
        if_body = []; else_body = []
        
        # IF: var is not None
        
        body.append(bld.iif(bld.comp(bld.ref(var), 'is not', bld.cnst(None)), if_body, else_body))
        # add stuff to if's body from here
        
        # compare the last two bound vars
        if len(bound) > 0:
            if_body2 = []
            if_body.append(bld.iif(bld.comp(bld.ref(bound[-1]), 'eq', bld.ref(var)), if_body2))
            if_body = if_body2 # add the rest to this if's body!
            
        # (var is not None, so add to bound)
        bound.append(var)
        if idx+1 < len(vars):
            # for case where this var is bound, process next var
            self.__unify_vars(vars, idx+1, bound[:], unbound[:], if_body)
        else:
            # if last var, then we made it! call ctu
            if_body.append(bld.stmt(bld.fn_call(bld.ref('ctu'), self.__unify_ctu_args(bld, vars, bound))))
        
        # ELSE: (so, var is None)
        
        bound.pop() # remove from bound
        unbound.append(var) # add to unbound
        
        if idx+1 < len(vars):
            # for case where this var is _not_ bound, process next var
            self.__unify_vars(vars, idx+1, bound[:], unbound[:], else_body)
        elif len(bound) > 0:
            # if last var, then we made it! call ctu
            else_body.append(bld.stmt(bld.fn_call(bld.ref('ctu'), self.__unify_ctu_args(bld, vars, bound))))

    def __unify_ctu_args(self, bld, vars, bound):
        # (if a var was not provided, pass one of the bound vars instead)
        return [ bld.ref(var) if var in bound else bld.ref(bound[0]) for var in vars ] + [ bld.ref('state') ]
    
    def __find_triple_call(self, clause, clause_fn, ctu_fn):
        # first, build the ctu call
        ctu_call = self.__gen_find_ctu(clause, clause_fn, ctu_fn)
        
        # then, create lambda with as body the ctu call
        lmbda = self.__builder.lmbda(['t', 'state'], ctu_call)

        # finally, create model.find call

        # s, p, o from clause will be search terms
        #   if variable: if provided as argument, refer to the function argument, else None
        #   (ungrounded-collections) if coll with variables: provide None (requires separate unification) 
        #   else, use resource from clause
        call_args = []
        for r in clause:
            match r.type():
                
                case term_types.VAR:
                    varname = self.__safe_int_var(r.name)
                    if varname in clause_fn.in_vars: # given as var, so can pass it
                        call_args.append(self.__var_ref(varname))
                    else:
                        call_args.append(self.__builder.cnst(None))
                
                # TODO if possible, unify collection and pass in search
                case term_types.COLLECTION: # (ungrounded-collections)
                    if not r.is_grounded():
                        call_args.append(self.__builder.cnst(None))
                    else:
                        call_args.append(self.__val(r))
                
                case _: call_args.append(self.__val(r))

        call_args += [self.__builder.ref('state'), lmbda]
        search_call = self.__builder.fn_call(
            self.__builder.attr_ref('data', 'find'), call_args)

        self.__builder.fn_body_stmt(
            clause_fn.fn, self.__builder.stmt(search_call))
        
        
    def __gen_find_ctu(self, clause, clause_fn, ctu_fn):
        # (ungrounded-collections)
        colls_with_vars = [ (coll, spo) for (coll, spo) in self.__coll_with_vars_spo(clause) ]
        # coll with vars need to be unified separately
        # returned ctu will point to the unification function
        if len(colls_with_vars) > 0:
            ctu_fn.in_args = [self.__builder.ref(v) for v in ctu_fn.in_vars]
            return self.__unifycoll_find_ctu(colls_with_vars, clause, clause_fn, ctu_fn)
        else:
            return self.__default_find_ctu(clause, ctu_fn)
    
    # (ungrounded-collections)
    def __unifycoll_find_ctu(self, colls_with_vars, clause, clause_fn, ctu_fn):
        unify_fn_params = []; unify_fn_args = []
        
        if_test = []; if_body = []
        # for each rule's coll with vars, attempt to unify with data coll
        #   if_test = comparisons between rule coll's constants and data coll's elements
        #   if_body = assignments of data coll's elements to rule coll's variables 
        for i, (coll, spo) in enumerate(colls_with_vars):
            coll_param = self.__builder.ref(f'coll_{i}')
            
            # add param for coll
            unify_fn_params.append(coll_param.id)
            # get arg for coll param from triple
            unify_fn_args.append(self.__builder.attr_ref('t', spo))
            
            self.__unify_coll(coll, [], coll_param, clause_fn, if_test, if_body)
        
        if_test = self.__builder.conj(if_test) if len(if_test) > 1 else if_test[0]
        
        # all individual (non-nested) vars in clause, with spo position
        clause_vars = {v: i for i, v in self.__vars_triple_spo(clause)}
        
        # also fn params: distinct incoming & indiv clause vars
        unify_vars = list(dict.fromkeys(clause_fn.in_vars + [v for v in clause_vars])) # (keep order)
        unify_fn_params += unify_vars
        
        # get args for these extra vars
        unify_fn_args += [self.__triple_val('t', clause_vars[v]) if v in clause_vars else self.__builder.ref(v) for v in unify_vars]
        
        # print("params/args", unify_fn_params, unify_fn_args)
        
        # create our unification function
        unify_fn = self.__rule_fn_def(clause_fn.name + "_unify_coll", unify_fn_params)
        self.__code.append(unify_fn)
                
        # add call to original continuation to if_body
        # (use ctu_vars/call_args; these include vars that were unified here)
        if_body.append(self.__builder.stmt(self.__rule_fn_call(ctu_fn.name, ctu_fn.in_args)))
        
        # create if stmt based on if_test & if_body
        self.__builder.fn_body_stmt(unify_fn, self.__builder.iif(if_test, if_body))
        
        # call our unify_fn as ctu from original rule fn
        return self.__rule_fn_call(unify_fn.name, unify_fn_args)
    
    # (ungrounded-collections)
    def __unify_coll(self, clause_coll_val, pos, match_coll_expr, clause_fn, conds, assns):
        bld = self.__builder
        
        conds.append(
            bld.comp(
                bld.fn_call(bld.attr_ref_expr(match_coll_expr, 'type')),
                'eq', bld.attr_ref('term_types', 'COLLECTION'))
        )        
        conds.append(
            bld.comp(bld.fn_call(bld.ref('len'), [ match_coll_expr ]),
                                'eq', bld.cnst(len(clause_coll_val)))
        )
        
        for i, clause_el_val in enumerate(clause_coll_val):
            cur_pos = pos + [ i ]
            match_el_expr = bld.index(match_coll_expr, i)
            
            match clause_el_val.type():
                case term_types.COLLECTION:
                    self.__unify_coll(clause_el_val, cur_pos, match_el_expr, clause_fn, conds, assns)
                
                case term_types.VAR:
                    # TODO only need assignment is var is None
                    if clause_el_val.idx_val() in clause_fn.in_vars:
                        conds.append(bld.disj([
                            bld.comp(bld.ref(clause_el_val.name), 'is', bld.cnst(None)),
                            bld.comp(bld.ref(clause_el_val.name), 'eq', self.__term_val(match_el_expr))
                        ]))
                    assns.append(
                        bld.assn(clause_el_val.name, self.__term_val(match_el_expr)))
                    
                case _:
                    conds.append(
                        bld.comp(self.__term_val(match_el_expr), 'eq', bld.cnst(clause_el_val.idx_val())))

    
    def __default_find_ctu(self, clause, ctu_fn):
        # ex: { 'p' : 's', 'a': 'o' }
        clause_vars = {v: i for i, v in self.__vars_triple_spo(clause)}

        # arguments to be passed to ctu
        ctu_fn.in_args = [self.__triple_val('t', clause_vars[v]) if v in clause_vars else self.__builder.ref(v)
                     for v in ctu_fn.in_vars]

        # model.find will call a lambda
        # this lambda will itself call a ctu

        # ex: ctu_fn = rule0_1 or ctu (original parameter)
        return self.__rule_fn_call(ctu_fn.name, ctu_fn.in_args)
        
    
    def __match_rule_calls(self, clause, clause_fn, ctu_fn):
        # print("matching:", clause)
        matches = self.__matching_rules(clause)

        # TODO blank nodes vs. universals

        for match in matches:
            
            # TODO deal with recursion
            if match.fn_name == clause_fn.name:
                #print(f"warning: avoiding recursion in {match.fn_name}")
                continue;
            
            # arguments to be passed to ctu
            # (may be updated by code below)
            ctu_fn.in_args = [ self.__builder.ref(p) for p in ctu_fn.in_vars ]
            
            match_fn = MatchRuleFn()
            
            head = match.rule.s
            match_clause = head.model.triples()[0]
            
            for pos in range(3):
                match_r = match_clause[pos]; clause_r = clause[pos]
                # print(f"{match_r} <> {clause_r}")
                
                # (ungrounded-collections)
                if match_r.type() == term_types.COLLECTION and not match_r.is_grounded() or \
                    clause_r.type() == term_types.COLLECTION and not clause_r.is_grounded():
                    # check consistency between match_r's coll & clause_r
                    
                    # returns false if match_r coll is not consistent with clause_r
                    # else; note that rule fns will have separate params for each of its coll var
                    # so, fn passes appropriate arguments for these params based on clause_r
                    if not self.__match_call_coll(match_r, clause_r, clause_fn, ctu_fn, match_fn):
                        return False
                else:
                    if not self.__match_call_terms(match_r, clause_r, clause_fn, ctu_fn, match_fn):
                        return False

            ctu_call = self.__rule_fn_call(ctu_fn.name, ctu_fn.in_args)

            # lambda params: vars we want from match rule fn (+ extra params)
            lmbda_params = match_fn.get_vars + ['state' ]
            lmbda = self.__builder.lmbda(lmbda_params, ctu_call)

            # match args: args we pass to match fn call
            match_args = match_fn.in_args + \
                    [self.__builder.ref('data'), self.__builder.ref('state'), lmbda]
            match_call = self.__builder.stmt(self.__builder.fn_call(
                self.__builder.ref(match.fn_name), match_args))

            # if needed, wrap in runtime conditional
            if len(match_fn.conds) > 0:
                match_call = self.__builder.iif(
                    self.__builder.conj(match_fn.conds), match_call)

            self.__builder.fn_body_stmt(clause_fn.fn, match_call)
        #     print()
        
        return True
        
    def __match_call_terms(self, match_r, clause_r, clause_fn, ctu_fn, match_fn):
        if match_r.is_concrete():
            if clause_r.is_concrete():
                # (ungrounded-collections)
                if clause_r.is_grounded() and match_r.is_grounded() and clause_r != match_r:  # compile-time check
                    print("compile-time check: nok")
                    return False
            else:
                clause_varname = self.__safe_int_var(clause_r.name)
                # add runtime check, if possible
                if clause_varname in clause_fn.in_vars:
                    cmp1 = self.__builder.comp(self.__var_ref(clause_varname), 
                                                'is', self.__builder.cnst(None))
                    cmp2 = self.__builder.comp(self.__var_ref(clause_varname), 'eq', self.__val(match_r))
                    match_fn.conds.append(self.__builder.disj([cmp1, cmp2]))

                # clause has variable; match rule has concrete value
                # if successful, pass concrete value to ctu, if needed
                if clause_varname in ctu_fn.in_vars:
                    ctu_fn.in_args[ctu_fn.in_vars.index(clause_varname)] = self.__val(match_r)
        
        else: # pass data as arguments; get results as lambda parameters
            if clause_r.is_concrete():
                match_varname = self.__safe_ext_var(match_r.name)
                match_fn.get_vars.append(match_varname)
                match_fn.in_args.append(self.__val(clause_r))
            else:
                clause_varname = self.__safe_int_var(clause_r.name)
                # always get value from match clause / find call; 
                # either we gave None, or it is the same as what we gave
                match_fn.get_vars.append(clause_varname)
                if clause_varname in clause_fn.in_vars:
                    # pass var to rule fn call, if given as input
                    match_fn.in_args.append(self.__var_ref(clause_varname))
                else: # else, pass None
                    match_fn.in_args.append(self.__builder.cnst(None))
                    
        return True
        
    # (ungrounded-collections)
    def __match_call_coll(self, match_r, clause_r, clause_fn, ctu_fn, match_fn):
        # (clause_r is none if there was nothing left to check consistency with)
        if clause_r is not None:
            # if both are collections, require same length as match_r
            if (match_r.type() == term_types.COLLECTION and clause_r.type() == term_types.COLLECTION and len(match_r) != len(clause_r)):
                return False
            
            # if clause_r is var, match_r was ungrounded coll: 
            # need to unify with _grounded collection_ from match fn
            if not clause_r.is_concrete():
                # we'll do this based on var values passed by match fn
                clause_varname = self.__safe_int_var(clause_r.name)
                if clause_varname in ctu_fn.in_vars: # only if this var is actually used, lol
                    ctu_fn.in_args[ctu_fn.in_vars.index(clause_varname)] = self.__reconstr(match_r, ext_vars=True)
                    
                # (after, still need to process match_r (i.e., pass None's, collect its vars))
        
            # if match_r is var, clause_r was ungrounded coll: 
            # need to pass _grounded collection_ to match fn
            # TODO ensure full grounding by skolemization or whatever
            elif not match_r.is_concrete():
                match_varname = self.__safe_ext_var(match_r.name)
                match_fn.get_vars.append(match_varname)
                match_fn.in_args.append(self.__reconstr(clause_r))
                return True # nothing left to do
        
        for i, match_r2 in enumerate(match_r):
            clause_r2 = clause_r[i] if (clause_r is not None and clause_r.type() == term_types.COLLECTION) else None
            
            # nested collection-with-vars; call fn recursively
            if (match_r2.type() == term_types.COLLECTION and not match_r2.is_grounded()) or \
                (clause_r2 is not None and clause_r2.type() == term_types.COLLECTION and not clause_r2.is_grounded()):
                if not self.__match_call_coll(match_r2, clause_r2, clause_fn, ctu_fn, match_fn):
                    return False
            
            # if no consistency to be checked, add empty arguments (None) for coll var param
            elif clause_r2 is None:
                if not match_r2.is_concrete():
                    match_varname = self.__safe_ext_var(match_r2.name)
                    match_fn.get_vars.append(match_varname)
                    match_fn.in_args.append(self.__builder.cnst(None))
            else:
                if not self.__match_call_terms(match_r2, clause_r2, clause_fn, ctu_fn, match_fn):
                    return False           
        
        return True


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

            entry = FnIdxEntry(r, self.__fn_name(i, 0))
            for t in r.s.model.triples():
                if t.p.type() == term_types.VAR:
                    self.__pred_idx.add('var', entry)
                else:
                    self.__pred_idx.add(t.p.idx_val(), entry)
                self.__pred_idx.add('all', entry)

            i += 1
            
    # def __is_builtin(self, clause):
    #     return clause.p.type() == term_types.IRI and clause.p.ns.startswith(swapNs.iri)
    
    # def __run_builtin(self, clause_fn, clause, in_vars, ctu_fn, ctu_vars, rest_args):
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
                        ret.append(self.__safe_int_var(r.name))
                    case term_types.COLLECTION: 
                        ret.extend(self.__safe_int_var(v) for v in r._vars())
        return ret

    def __vars_triple_spo(self, t):
        spo = ['s', 'p', 'o']
        for i, r in enumerate(t):
            match r.type():
                case term_types.VAR:
                    yield spo[i], self.__safe_int_var(r.name)

    def __vars_triple(self, t):
        for i, r in enumerate(t):
            match r.type():
                case term_types.VAR:
                    yield self.__safe_int_var(r.name)
                
                case term_types.COLLECTION:
                    for coll_var in r._vars():
                        yield self.__safe_int_var(coll_var)
                        
    def __coll_with_vars_spo(self, t):
        spo = ['s', 'p', 'o']
        for i, r in enumerate(t):
            match r.type():
                case term_types.COLLECTION:
                    if not r.is_grounded():
                        yield r, spo[i]
    
    # NOTE code below assumes this does not occur often
    # (else, possibility for optimizing this)
    
    def __safe_var(self, n, ext_vars=False):
        return self.__safe_ext_var(n) if ext_vars else self.__safe_int_var(n)
    
    def __safe_int_var(self, n):
        n2 = None
        match n:
            case 't': n2 = 'tt'
            case 'data': n2 = 'dataa'
            case 'state': n2 = 'statee'
            case 'ctu': n2 = 'ctuu'
            case _: return n
        
        # ensure that new var does not occur in this rule
        return self.__safe_ext_var(n2)
        
    def __safe_ext_var(self, n):
        if n not in self.__all_rule_vars:
            return n
        
        return self.__safe_ext_var(n + "2")

    def __val(self, r):
        return self.__builder.cnst(r.idx_val())
    
    def __var_ref(self, name):
        return self.__builder.ref(name)
    
    def __triple_val(self, t, spo):
        return self.__builder.fn_call(self.__builder.attr_ref_expr(self.__builder.attr_ref(t, spo), 'idx_val'))

    def __term_val(self, expr):
        return self.__builder.fn_call(self.__builder.attr_ref_expr(expr, 'idx_val'))

    def __fn_name(self, rule_no, clause_no):
        if clause_no == 0:
            return f"{self.__fn_prefix}_{rule_no}"
        else:
            return f"{self.__fn_prefix}_{rule_no}_{clause_no}"
        
    def __rule_fn_def(self, fn_name, params):
        my_params = params + self.__inner_fn_params
        return self.__builder.fn(fn_name, my_params)
        
    def __rule_fn_call(self, fn_name, args):
        my_args = args + (self.__rule_fn_args if fn_name == 'ctu' else self.__inner_fn_args)
        return self.__builder.fn_call(self.__builder.ref(fn_name), my_args)
            
    def __reconstr(self, r, ext_vars=False):
        match r.type():
            case term_types.IRI: 
                cls = "Iri"; arg = r.iri
            case term_types.LITERAL: 
                cls = "Literal"; arg = r.value
            case term_types.COLLECTION: 
                cls = "Collection"
                arg = self.__builder.lst([ self.__reconstr(e, ext_vars) for e in r ])
            case term_types.VAR: 
                return self.__var_ref(self.__safe_var(r.name, ext_vars))
            case _: print("inconceivable")

        return self.__builder.fn_call(fn=self.__builder.ref(cls), args=[arg])


class RuleFn:
    
    # name (string)
    # in_vars (strings)
    # in_args (ast)
    # fn (ast)
    
    def __init__(self, name, in_vars, fn):
        self.name = name
        self.in_vars = in_vars
        self.fn = fn
        
class MatchRuleFn:
    
    # conds (runtime conditions before calling match rule fn)
    # in_args (args to provide to match fn's vars)
    # get_vars (vars to get from match rule fn; will serve as lambda params)

    def __init__(self):
        self.conds = []
        self.in_args = []
        self.get_vars = []

class FnIdxEntry:

    # rule (triple)
    # fn_name

    def __init__(self, rule, fn_name):
        self.rule = rule
        self.fn_name = fn_name

    def __str__(self):
        return f"<{self.fn_name} - {str(self.rule)}>"

    def __repr__(self):
        return self.__str__()