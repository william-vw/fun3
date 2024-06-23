from collections import Counter
from multidict import MultiDict
from n3.fun.py_build import PyBuilder
from n3.terms import Var, term_types, Triple
from n3.ns import n3Log, swapNs
from itertools import chain

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
    # __var_cnt
    
    # __unify_head
    # __unify_body
    # __unify_data_coll
    
    # __inner_fn_params (+ __inner_fn_args)
    # __rule_fn_params (+ __rule_fn_args)

    def __init__(self):
        self.bld = PyBuilder()
        self.__fn_prefix = "rule"
        self.__var_cnt = 0
        
        self.__inner_fn_params = [ 'data', 'state', 'ctu' ]
        self.__rule_fn_params = [ 'state' ]
        self.__inner_fn_args = [self.bld.ref(v) for v in self.__inner_fn_params]
        self.__rule_fn_args = [self.bld.ref(v) for v in self.__rule_fn_params]

    def gen_python(self, rules):
        self.__process_rules(rules)

        return self.__gen_rule_mod(rules)

    def __gen_rule_mod(self, rules):
        self._code = [self.__gen_imports()]
        
        # will add corresponding functions to 'code'
        for i, (head, _, body) in enumerate(rules):
            self.__gen_rule(i, head, body)

        return self.bld.module(self._code)

    def __gen_imports(self):
        return self.bld.imports('n3.terms', ['Iri', 'Var', 'Literal', 'Collection', 'term_types'])

    def __gen_rule(self, rule_no, head, body):                
        in_vars = head._recur_vars()
        first_fn = RuleFn(in_vars=in_vars)
        
        # if needed, unify coref vars in head
        # (will update clause_fn & its in_vars)
        # self.__unify_head.unify(head, body, first_fn)
        
        # keeps track of vars in subsequent clauses
        self.__cur_vars = first_fn.in_vars

        if body.type() == term_types.GRAPH:
            for i, _ in enumerate(body.model.triples()):
                self.__gen_clause(rule_no, head, body, i, (first_fn if i==0 else None))

        elif body.type() == term_types.LITERAL and body.value == True:
            self.__gen_clause(rule_no, head, None, 0, first_fn)

    def __gen_clause(self, rule_no, head, body, clause_no, clause_fn):
        # incoming params representing vars
        in_vars = self.__cur_vars
        
        # ADT representing clause fn
        clause_fn = clause_fn if clause_fn is not None else RuleFn(in_vars=in_vars)
        clause_fn.name = self._fn_name(rule_no, clause_no)

        # fn AST representing this clause
        clause_fn.fn = self._rule_fn_def(clause_fn.name, in_vars)
        self._code.append(clause_fn.fn) # add to generated code
        
        # e.g., boolean as body
        if body is None:
            self.bld.fn_body_stmts(clause_fn.fn, clause_fn.body if len(clause_fn.body) > 0 
                                                                    else [ self.bld.pss() ])
            return
                
        # current clause
        clause = body.model.triple_at(clause_no)
        
        # ADT representing ctu fn (i.e., fn to be called after clause fn)
        # (either fn for the next clause, or original 'ctu' fn for this rule)
        is_last = (clause_no == body.model.len() - 1)
        ctu_fn = RuleFn(name=(self._fn_name(rule_no, clause_no+1) if not is_last else 'ctu'), is_last=is_last)
        
        # vars occurring in clause
        own_vars = clause._recur_vars()
        
        if not ctu_fn.is_last:
            # params to pass to next clause fn; unique(prior vars + own vars)
            ctu_fn.in_vars = list(dict.fromkeys(self.__cur_vars + own_vars)) # (keep order)
        else:
            # only pass var needed by original ctu fn (head vars!)
            ctu_fn.in_vars = head._recur_vars()
         
        # keep track of vars in subsequent clauses
        if not ctu_fn.is_last:
            self.__cur_vars = list(dict.fromkeys(self.__cur_vars + clause._recur_vars())) # (keep order)

        # if self.__is_builtin(clause):
        #     self.__run_builtin(clause_fn, clause, in_vars, ctu_fn, ctu_vars)
        # else:
        # try finding matching data
        self.__find_data_call(head, clause, clause_fn, ctu_fn)
        # try finding matching rules
        self.__match_rule_calls(head, clause, clause_fn, ctu_fn)
    
    # START find data
    
    def __find_data_call(self, head, clause, clause_fn, ctu_fn):
        unify = Unify(self, self.bld, find_data=True)
        
        # if needed, unify co-ref vars in clause
        unify.unify_coref(clause)
        
        # if needed, unify ungrounded collections in clause with data
        # clause = self.__unify_coll.unify_find_data(clause, clause_fn, ctu_fn)
                 
        #  arguments for data.find call

        # s, p, o from clause will be search terms
        #   if variable: if provided as argument, refer to the function argument, else None
        #   (ungrounded-collections) if coll with variables: provide None (requires separate unification) 
        #   else, use resource from clause
        call_args = []
        for r in clause:
            
            match r.type():
                case term_types.VAR:
                    # when given as var, can pass it
                    call_args.append(self._var_ref(r.name) if r.name in clause_fn.avail_vars else self.bld.cnst(None))
                
                # TODO (long-term) if possible, unify collection and provide as search param
                case term_types.COLLECTION: # (ungrounded-collections)
                    call_args.append(self.bld.cnst(None) if not r.is_grounded() else self._val(r))
                
                case _: call_args.append(self._val(r))
        
        # ctu vars ; ex: { 'p' : [ 's ', Var('p') ], 'a': [ 'o', Var('a') ] }
        clause_vars = { v.name: (['s', 'p', 'o'][i], v) for i, v in clause._vars(get_name=False) }
        ctu_fn.in_args.extend([self._triple_val('t', *clause_vars[v]) if v in clause_vars else self.bld.ref(v)
                     for v in ctu_fn.in_vars])
        
        # let unif do its thing, if needed
        ctu_fn = unify.finalize(clause_fn, ctu_fn)
        
        # build the ctu call
        ctu_call = self._rule_fn_call(ctu_fn.name, ctu_fn.in_args)
        
        # then, create lambda with as body the ctu call
        lmbda = self.bld.lmbda(['t', 'state'], ctu_call)

        # finally, create data.find call
        call_args += [self.bld.ref('state'), lmbda]
        search_call = self.bld.fn_call(
            self.bld.attr_ref('data', 'find'), call_args)

        self.bld.fn_body_stmt(
            clause_fn.fn, self.bld.stmt(search_call))
        
    # END find triple    
    
    # START match call
    
    def __match_rule_calls(self, head, clause, clause_fn, ctu_fn):
        # print("matching:", clause)
        matches = self.__matching_rules(clause)

        # TODO blank nodes vs. universals

        # print("matches:", matches)
        for match in matches:
            
            # TODO deal with recursion
            # if clause_fn.name.startswith(match.fn_name): # (calling first rule fn again)
            #     print(f"\nwarning: avoiding recursion in {match.fn_name}\n")
            #     continue;
            
            # arguments to be passed to ctu (may be updated below)
            ctu_fn.in_args = [ self.bld.ref(p) for p in ctu_fn.in_vars ]
            
            match_fn = MatchRuleFn()
            
            head = match.rule.s
            match_clause = head.model.triples()[0]
            
            if not self.__match_clauses(clause, match_clause, clause_fn, ctu_fn, match_fn):
                continue
            
            unify = Unify(self, self.bld, find_data=False, id=match.fn_name)
        
            # if needed, unify co-ref vars in clause
            unify.unify_coref(clause)
            
            # if needed, unify coll vars (see __match_call_coll)
            # self.__unify_coll.unify_coll_vars(clause_fn, ctu_fn)
            
            # let unif do its thing, if needed
            ctu_fn = unify.finalize(clause_fn, ctu_fn, match_fn)

            # build the ctu call

            ctu_call = self._rule_fn_call(ctu_fn.name, ctu_fn.in_args)

            # lambda params: vars we want from match rule fn (+ extra params)
            lmbda_params = match_fn.get_vars + ['state' ]
            lmbda = self.bld.lmbda(lmbda_params, ctu_call)

            # match args: args we pass to match fn call
            match_args = match_fn.in_args + \
                    [self.bld.ref('data'), self.bld.ref('state'), lmbda]
            match_call = self.bld.stmt(self.bld.fn_call(
                self.bld.ref(match.fn_name), match_args))

            # if needed, wrap in runtime conditional
            if len(match_fn.cond) > 0:
                match_call = self.bld.iif(
                    self.bld.conj(match_fn.cond), match_call)

            self.bld.fn_body_stmt(clause_fn.fn, match_call)
        #     print()
    
    def __match_clauses(self, clause, match_clause, clause_fn, ctu_fn, match_fn):
        for pos in range(3):
            match_r = match_clause[pos]; clause_r = clause[pos]
            # print(f"{match_r} <> {clause_r}")
            
            # (ungrounded-collections)
            if match_r.type() == term_types.COLLECTION and not match_r.is_grounded() or \
                clause_r.type() == term_types.COLLECTION and not clause_r.is_grounded():
                # check consistency between match_r's coll & clause_r
                
                # check consistency between match_r and clause_r
                # (also, pass appropriate arguments to match rule fn)
                if not self.__match_call_coll(match_r, clause_r, clause_fn, ctu_fn, match_fn):
                    return False
            else:
                if not self.__match_call_terms(match_r, clause_r, clause_fn, ctu_fn, match_fn):
                    return False

        return True
    
    # unify clause term with match clause term
    def __match_call_terms(self, match_r, clause_r, clause_fn, ctu_fn, match_fn):
        if match_r.is_concrete():
            if clause_r.is_concrete():
                if clause_r.is_grounded() and match_r.is_grounded() and clause_r != match_r:  # compile-time check
                    print("compile-time check: nok")
                    return False
            else:
                # add runtime check, if possible
                if clause_r.name in clause_fn.avail_vars:
                    cmp1 = self.bld.comp(self._var_ref(clause_r.name), 
                                                'is', self.bld.cnst(None))
                    cmp2 = self.bld.comp(self._var_ref(clause_r.name), 'eq', self._val(match_r))
                    match_fn.cond.append(self.bld.disj([cmp1, cmp2]))

                # clause has variable; match rule has concrete value
                # if successful, pass concrete value to ctu, if needed
                if clause_r.name in ctu_fn.in_vars:
                    ctu_fn.in_args[ctu_fn.in_vars.index(clause_r.name)] = self._val(match_r)
        
        else: # pass data as arguments; get results as lambda parameters
            if clause_r.is_concrete():
                match_fn.get_vars.append(match_r.name)
                match_fn.in_args.append(self._val(clause_r))
            else:
                # always get value from match clause / find call; 
                # either we gave None, or it is the same as what we gave
                match_fn.get_vars.append(clause_r.name)
                # when given as var, can pass it
                match_fn.in_args.append(self._var_ref(clause_r.name) if clause_r.name in clause_fn.avail_vars else self.bld.cnst(None))
                    
        return True
    
    # (ungrounded-collections)
    # returns false if match_r coll is not consistent with clause_r
    # also, will pass appropriate arguments for params based on clause_r
    # (note that rule fns will have separate params for each of its coll var)
    def __match_call_coll(self, match_r, clause_r, clause_fn, ctu_fn, match_fn):
        # (clause_r is none if there was nothing left to check consistency with)
        if clause_r is not None:
            # if both are collections, require same length as match_r
            if (match_r.type() == term_types.COLLECTION and clause_r.type() == term_types.COLLECTION and len(match_r) != len(clause_r)):
                return False
            
            # if clause_r is var, match_r was ungrounded coll: unify with _grounded collection_ from match fn
            if not clause_r.is_concrete():
                # we'll do this based on var values passed by match fn
                if clause_r.name in ctu_fn.in_vars: # only if this var is actually used, lol
                    ctu_fn.in_args[ctu_fn.in_vars.index(clause_r.name)] = self._reconstr(match_r)
                    
                # (after, will still process match_r (i.e., pass None's, collect its vars))
        
            # if match_r is var, clause_r was ungrounded coll: pass _grounded collection_ to match fn
            # TODO (long-term) if possible, unify collection and provide as search param
            elif not match_r.is_concrete():
                # self.__unify_coll.coll_to_unify(clause_r, match_r, clause_fn, ctu_fn, match_fn)
                return True
        
        # compare element-by-element
        for i, match_r2 in enumerate(match_r):
            clause_r2 = clause_r[i] if (clause_r is not None and clause_r.type() == term_types.COLLECTION) else None
            
            # nested ungrounded collections; call fn recursively
            if (match_r2.type() == term_types.COLLECTION and not match_r2.is_grounded()) or \
                (clause_r2 is not None and clause_r2.type() == term_types.COLLECTION and not clause_r2.is_grounded()):
                if not self.__match_call_coll(match_r2, clause_r2, clause_fn, ctu_fn, match_fn):
                    return False
            
            # if no consistency to be checked, add empty arguments (None) for coll var param
            elif clause_r2 is None:
                if not match_r2.is_concrete():
                    match_fn.get_vars.append(match_r2.name)
                    match_fn.in_args.append(self.bld.cnst(None))
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
            
            # giving up & just giving all vars unique names
            self.__rename_vars_unique(r.s, r.o)
            
            if r.s.model.len() != 1:
                print(f"warning: cannot use rule, length of head > 1 ({r})")
                del rules[i]; continue
            if r.p.iri == n3Log['implies']:
                print(f"warning: cannot use bottom-up rule ({r})")
                del rules[i]; continue

            entry = FnIdxEntry(r, self._fn_name(i, 0))
            for t in r.s.model.triples():
                if t.p.type() == term_types.VAR:
                    self.__pred_idx.add('var', entry)
                else:
                    self.__pred_idx.add(t.p.idx_val(), entry)
                self.__pred_idx.add('all', entry)

            i += 1
            
        # print("pred_idx:")
        # for k, v in self.__pred_idx.items(): print(k, ":\n", v, "\n")
            
    # END match call

    # def __is_builtin(self, clause):
    #     return clause.p.type() == term_types.IRI and clause.p.ns.startswith(swapNs.iri)
    
    # def __run_builtin(self, clause_fn, clause, in_vars, ctu_fn, ctu_vars, rest_args):
    #     match clause.p.ln:
    #         case 'notEqualTo': ...
    #         case _: raise GenError(f"unsupported builtin: '{clause.p.ln}'")
         
    # helper functions
    
    def _fn_name(self, rule_no, clause_no):
        if clause_no == 0:
            return f"{self.__fn_prefix}_{rule_no}"
        else:
            return f"{self.__fn_prefix}_{rule_no}_{clause_no}"

    def _val(self, r):
        return self.bld.cnst(r.idx_val())
    
    def _var_ref(self, name):
        return self.bld.ref(name)
    
    def _triple_val(self, t, spo, var=None):
        triple_ref = self.bld.attr_ref(t, spo)
        # unification code requires original ADT to work with
        if var is None or var._get_raw:
            return self.bld.fn_call(self.bld.attr_ref_expr(triple_ref, 'idx_val'))
        else:
            return triple_ref

    def _term_val(self, expr):
        return self.bld.fn_call(self.bld.attr_ref_expr(expr, 'idx_val'))
        
    def _rule_fn_def(self, fn_name, params):
        my_params = params + self.__inner_fn_params
        return self.bld.fn(fn_name, my_params)
        
    def _rule_fn_call(self, fn_name, args):
        my_args = args + (self.__rule_fn_args if fn_name == 'ctu' else self.__inner_fn_args)
        return self.bld.fn_call(self.bld.ref(fn_name), my_args)
            
    def _reconstr(self, r):
        match r.type():
            case term_types.IRI: 
                return self.bld.cnst(r.iri)
            case term_types.LITERAL: 
                return self.bld.cnst(r.value)
            case term_types.COLLECTION: 
                return self.bld.tple([ self._reconstr(e) for e in r ])
            case term_types.VAR: 
                return self.bld.ref(r.name)
            case _: print("inconceivable")
    
    # def _raw_type_check(self, ref, adt_type):
    #     raw_type = None
    #     match adt_type:    
    #         case term_types.COLLECTION:
    #             raw_type = 'tuple'
    #         case _: print("inconceivable!")

    #     return self.bld.comp(
    #         self.bld.fn_call(self.bld.ref('type'), [ ref ]), 'eq',
    #         self.bld.ref(raw_type)
    #     )
    
    def __rename_vars_unique(self, head, body):
        triple_it = chain(head._recur_vars(), body._recur_vars()) \
            if body.type() == term_types.GRAPH else head._recur_vars()
        unique_vars = { v:0 for v in triple_it }
        unique_vars = { v:f"{v}_{i}" for v,i in zip(unique_vars, range(self.__var_cnt, len(unique_vars)+self.__var_cnt)) }
        
        head._rename_recur_vars(unique_vars)
        if body.type() == term_types.GRAPH:
            body._rename_recur_vars(unique_vars)
        
        self.__var_cnt += len(unique_vars)
        

class RuleFn:
    
    # name (string)
    # in_vars (strings; incoming params representing vars)
    # in_args (ast; arguments for in_vars)
    # fn (ast)
    # is_last (bool)
    
    # cond, body
    
    def __init__(self, name=None, in_vars=None, in_args=None, fn=None, is_last=False):
        self.name = name
        self.in_vars = in_vars if in_vars is not None else []
        self.in_args = in_args if in_args is not None else []
        self.fn = fn
        self.is_last = is_last
        
    def extra_avail(self, vars):
        self.__extra_avail.extend(vars)
    
    def __getattr__(self, name):
        match name:
            case 'avail_vars': return self.in_vars
            case _: raise AttributeError(f"unknown attribute: {name}")
    
    # (shallow copy)
    def clone(self):
        copy = RuleFn(self.name, self.in_vars[:], self.in_args[:], self.fn)
        copy.is_last = self.is_last
        return copy
    
    
class MatchRuleFn:
    
    # conds (runtime conditions before calling match rule fn)
    # in_args (args to provide to match fn's vars)
    # get_vars (vars to get from match rule fn; will serve as lambda params)

    def __init__(self):
        self.cond = []
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
    

# unify hooks

class UnifyOp:
    
    # in_args
    # in_var
    # lmbda_vars
    
    # conds
    # assns
    
    def __init__(self):
        self.in_args = []
        self.in_vars = []
        self.lmbda_vars = MultiDict()
        
        self.conds = []
        self.assns = []
        
    def entry(self, arg, var):
        self.in_args.append(arg)
        self.in_vars.append(var)
        
    def is_empty(self):
        return len(self.in_args) == 0


class Unify:
    
    # gen, bld
    # find_data
    # cur_op
        
    def __init__(self, gen, bld, find_data, id=None):
        self.gen = gen
        self.bld = bld
        self.find_data = find_data
        self.id = id if id is not None else 'data'
        
        self._cur_op = UnifyOp()
        
    def finalize(self, clause_fn, ctu_fn, match_fn=None):
        if self._cur_op.is_empty():
            return ctu_fn

        # create separ unif fn
        unif_fn = ctu_fn.clone()
        unif_fn.name = f"{clause_fn.name}_unify_{self.id}"
        unif_fn.in_args.extend(self._cur_op.in_args)
        unif_fn.in_vars.extend(self._cur_op.in_vars)
        
        new_fn = self.gen._rule_fn_def(unif_fn.name, unif_fn.in_vars)
        self.gen._code.append(new_fn)
        
        fn_body = self._cur_op.assns
        # add call to orig ctu to our unif fn body
        fn_body.append(self.bld.stmt(self.gen._rule_fn_call(ctu_fn.name, [ self.bld.ref(v) for v in ctu_fn.in_vars ])))
        
        # wrap fn body in if-stmt w/ unif conds
        if len(self._cur_op.conds) > 0:
            fn_body = [ self.bld.iif(
                self.bld.conj(self._cur_op.conds), fn_body) ]
        
        self.bld.fn_body_stmts(new_fn, fn_body)
        
        # ugh, have to update lambda params
        if not self.find_data:
            match_fn.get_vars = list(dict.fromkeys(match_fn.get_vars)) # may have duplicates
            get_vars = []
            # expand each dupl var with unique occ names
            for v in match_fn.get_vars:
                if v in self._cur_op.lmbda_vars:
                    get_vars.extend(self._cur_op.lmbda_vars.getall(v))
                else:
                    get_vars.append(v)
            match_fn.get_vars = get_vars
        
        return unif_fn

    def unify_coref(self, clause):
        orig_vars_pos = clause._recur_vars_pos()
        orig_vars = [ v for _, v in orig_vars_pos ]
        
        # whew, no need to unify!
        if len(orig_vars) == len(set(orig_vars)): 
            return
        
        # darn :-(
        dupls = { v for v,c in Counter(orig_vars).items() if c > 1 }
        # print("dupls", dupls)
        
        # per triple spo, get unique names for dupl var occ (if needed, also for coll w/ dupl)
        # ex: { ?x :p ?x } = 0 -> ( x, x_s ), 2 -> ( x, x_o ) ; ex: { :a :p ( ?x ?x ) } = 2 -> ( None, coll_o )
        spo_var_occ = { self.__get_spo_pos(pos): (var, self.__get_spo_varname(pos, var)) for pos, var in orig_vars_pos if var in dupls }
        # print("spo_var_occ", spo_var_occ)
        
        # per dupl var occ, need extra in_arg and in_var for unif fn
        # (so we can manually unify them in unif fn)
        for spo, (orig_var, occ) in spo_var_occ.items():
            arg = self.gen._triple_val('t', Triple.spo[spo]) if self.find_data else self.bld.ref(occ)
            self._cur_op.entry(arg, occ)
            # print(arg, "->", occ)
        
        if not self.find_data:
            # if needed, update lambda params as well
            lmbda_vars = MultiDict()
            for spo, (orig_var, occ) in spo_var_occ.items():
                # map orig_var to its occ's (will be replaced by latter)
                lmbda_vars.add(orig_var, occ)
            self._cur_op.lmbda_vars.extend(lmbda_vars)

        # now, let's setup the unify conds

        # per orig (dupl) var, get positions of its occ's
        # ex: { ?x :p ?x } = x -> ((0, <triple>)), ((2, <triple>))
        # ex: { :a :p ( ?x ?x ) } = x -> ((2, <triple>), (0, <coll>)), ((2, <triple>), (1, <coll>))
        origvar_pos = MultiDict((orig_var, pos) for pos, orig_var in orig_vars_pos)
        
        for orig_var in set(origvar_pos.keys()):
            # per orig (dupl) var, for each occ, get in_var & pos
            # ex: { ?x :p ?x } = [ ( x_s, () ), ( x_o, () ) ]
            # ex: { :a :p ( ?x ?x ) } = [ ( coll_o, (0, <coll>) ), ( coll_o, (1, <coll>) ) ]
            entries = []
            for pos in origvar_pos.getall(orig_var):
                ( _, occ ) = spo_var_occ[self.__get_spo_pos(pos)]; 
                entries.append((occ, pos[1:]))
            # print(orig_var, entries)
            self.__unify_var(orig_var, entries)
        
    def __get_spo_pos(self, pos):
        return pos[0][0]

    def __get_spo_varname(self, pos, var):
        spo_ch = Triple.spo[self.__get_spo_pos(pos)]
        return f"{var}_{spo_ch}" if len(pos) == 1 else f"coll_{spo_ch}"

    def __unify_var(self, origvar, entries):
        ops = []
        # ex: renvar=coll_o, posns=(0, <coll>) but could be deeper nested
        for (renvar, posns) in entries:
            ref = self.bld.ref(renvar)
            for pos in posns: # keep indexing until we're there
                ref = self.bld.index(ref, pos[0])
            ops.append(ref)
        
        # ex: x_s == x_o ; coll_o[0] == coll_o[1]
        self._cur_op.conds.append(self.bld.comps('eq', ops))
        
        # (not actually needed in case of find_data)
        if not self.find_data:
            self._cur_op.assns.append(self.bld.assn(origvar, ops[0]))
        
    # returns:
    # ( list of de-duplicated, unique variables; map from original var -> list of renamed vars)
    #  e.g., (p, p, s) -> new_vars=(p0, p1, s), uniq_vars={p: [ p0, p1 })
    def _deduplicate_vars(self, vars):
        dupls = { v for v,c in Counter(vars).items() if c > 1 }
        
        new_vars = []; uniq_vars = { v:[] for v in dupls }
        for v in vars:
            if v in dupls:
                nv = f"{v}_o{len(uniq_vars[v])}"
                new_vars.append(nv); uniq_vars[v].append(nv)
            else:
                new_vars.append(v)
        
        return ( new_vars, uniq_vars )
    

# class UnifyCoref_Head(Unify) :
    
#     # gen, bld
    
#     def __init__(self, gen, bld):
#         super().__init__(gen, bld)
    
#     # we do 2 things here:
#     # 1/ ok if all _provided_ (de-)duplicated vars are same
#     # 2/ pass provided var values for non-provided vars
#     def unify(self, head, body, clause_fn):
#         orig_vars = head._recur_vars()
        
#         # whew, no need to unify!
#         if len(orig_vars) == len(set(orig_vars)): 
#             return
        
#         # darn :-(
#         # get de-dupl (new) vars & map from dupl -> de-dupl var
#         ( new_vars, uniq_vars ) = self._deduplicate_vars(orig_vars)
#         # print("dedupl:", new_vars, uniq_vars)
        
#         # de-duplicated vars will be input var params
#         clause_fn.in_vars = new_vars
        
#         # rename vars in head clause
#         # e.g., ?desc :parent ?desc -> ?desc0 :parent ?desc1 
#         # stmts in body will check desc0 = desc1 etc
#         head._rename_recur_vars(uniq_vars,repl_list=True)

#         # rename vars in body clause
#         # (nrs don't matter; desc0, desc1, will all be None or equal here)
#         # e.g., ?desc :abc ?desc -> ?desc0 :abc ?desc1
#         if body.type() == term_types.GRAPH:
#             body._rename_recur_vars(uniq_vars,repl_list=True)
        
#         # for each set of unique vars, add conds
#         # e.g., p: [p1,p2], q:[q1,q2], sets are [p1,p2] and [q1,q2]
#         for var_uniq_vars in uniq_vars.values():
#             self.__unify_head_vars(var_uniq_vars, 0, [], [], clause_fn.body)

    
#     # bound: vars that are bound at this point; unbound: idem for unbound vars
#     def __unify_head_vars(self, vars, idx, bound, unbound, body):
#         var = vars[idx]        
#         if_body = []; else_body = []
        
#         # IF: var is not None
        
#         body.append(self.bld.iif(self.bld.comp(self.bld.ref(var), 'is not', self.bld.cnst(None)), if_body, else_body))
#         # add stuff to if's body from here
        
#         # compare the last two bound vars
#         if len(bound) > 0:
#             if_body2 = []
#             if_body.append(self.bld.iif(self.bld.comp(self.bld.ref(bound[-1]), 'eq', self.bld.ref(var)), if_body2))
#             if_body = if_body2 # add the rest to this if's body!
        
#         # (var is not None, so add to bound)
#         bound.append(var)
#         if idx+1 < len(vars):
#             # for case where this var is bound, process next var
#             self.__unify_head_vars(vars, idx+1, bound[:], unbound[:], if_body)
#         else:
#             # if last var, then we made it!
#             # TODO refer to next clause function if needed (now, simply assuming there is no body)
#             if_body.append(self.bld.stmt(self.gen._rule_fn_call('ctu', self.__ctu_args(vars, bound))))
        
#         # ELSE: (so, var is None)
        
#         bound.pop() # remove from bound
#         unbound.append(var) # add to unbound
        
#         if idx+1 < len(vars):
#             # here, this var is _not_ bound; process next var
#             self.__unify_head_vars(vars, idx+1, bound[:], unbound[:], else_body)
#         elif len(bound) > 0:
#             # if last var, we made it!
#             else_body.append(self.bld.stmt(self.gen._rule_fn_call('ctu', self.__ctu_args(vars, bound))))
            
#     def __ctu_args(self, vars, bound):
#         # (if a var was not provided, pass one of the bound vars instead)
#         return [ self.bld.ref(var) if var in bound else self.bld.ref(bound[0]) for var in vars ]
    

# class UnifyColl(Unify):
    
#     def __init__(self, gen, bld):
#         super().__init__(gen, bld)

#     def unify_find_data(self, clause, clause_fn, ctu_fn):
#         # get all ungrounded collections
#         ungr_colls = [ (pos, term) for pos, term in enumerate(clause) if term.type() == term_types.COLLECTION and not term.is_grounded()]
        
#         # whew, no need to unify!
#         if len(ungr_colls) == 0:
#             return clause
        
#         # darn :-(
        
#         # ex: :x :y ( 1 2 ?z )
#         clause = clause.clone() # only applicable here
        
#         if_test = []; if_body = []
#         for i, (pos, coll) in enumerate(ungr_colls):
#             coll_var = f"coll_{i}"
            
#             # sneak in variables for ungrounded collections
#             # (code will then pass values for these vars to unif fn)
#             clause[pos] = Var(coll_var, get_raw=False)

#             # add code to unify collection from the data (conds, assns)
#             self.__unify_coll(coll, [], self.bld.ref(coll_var), clause_fn, if_test, if_body)
        
#         # populate code for our unif fn (incl. call to original ctu fn)
#         self.__populate_ctu_fn(ctu_fn, if_test, if_body)

#         # (regular algorithm will proceed with reworked clause; i.e., use correct vars for unif fn)
#         # (also, will create unif fn with conds, stmts from above; see __gen_separ_ctu_fn)
        
#         return clause

#     # TODO think about this some more & test better

#     def coll_to_unify(self, clause_coll, match_var, _, ctu_fn, match_fn):
#         match_fn.get_vars.append(match_var.name)
#         match_fn.in_args.append(self.bld.cnst(None))
        
#         # we will find these one by one, so collect them here
#         ctu_fn.to_unify.append((clause_coll, match_var.name))
    
#     def unify_coll_vars(self, clause_fn, ctu_fn):
#         # whew, no need to unify!
#         if len(ctu_fn.to_unify)==0: return
        
#         # darn :-(
        
#         if_test = []; if_body = []
#         for (clause_coll, match_var) in ctu_fn.to_unify:
#             # add code to unify collection from the rule (conds, assns)
#             self.__unify_coll(clause_coll, [], self.bld.ref(match_var), clause_fn, if_test, if_body)
        
#         # populate code for our unif fn (incl. call to original ctu fn)
#         self.__populate_ctu_fn(ctu_fn, if_test, if_body)
        
#         # now, manually update our unif fn with vars we need
#         for (clause_coll, match_var) in ctu_fn.to_unify:
#             ctu_fn.in_vars.append(match_var)
#             ctu_fn.in_args.append(self.bld.ref(match_var))
            
#         # (regular algorithm will create unif fn with vars/args, conds, stmts from above; see __gen_separ_ctu_fn)
    
#     def __populate_ctu_fn(self, ctu_fn, if_test, if_body):
#         # ex: coll0[0]==1 and coll0[1]==2
#         ctu_fn.cond.append(self.bld.conj(if_test) if len(if_test) > 1 else if_test[0])
        
#         # won't be the last fn, because of our intermediary fn
#         ctu_fn.is_last = False
        
#         # now, add call to original ctu as if nothing happened
#         if_body.append(self.bld.stmt(self.gen._rule_fn_call(ctu_fn.name, [ self.bld.ref(v) for v in ctu_fn.in_vars ])))
        
#         # ex: z = coll0[2]; rule_0_1(...)
#         ctu_fn.body.extend(if_body)

#     # 1/ add conditions for element-by-element comparisons
#     # 2/ add assignments of match coll values to clause vars 
#     # clause_coll_term: term in clause_coll
#     # match_coll_expr: corresp. select in match_coll (e.g., coll[0][1])
#     # pos: (nested) position (e.g., [0, 1] for 2nd el in 1st el)
#     def __unify_coll(self, clause_coll_term, pos, match_coll_expr, clause_fn, conds, assns):
#         # match_coll needs to be collection of same length
#         conds.append(
#             self.bld.comp(
#                 self.bld.fn_call(self.bld.attr_ref_expr(match_coll_expr, 'type')),
#                 'eq', self.bld.attr_ref('term_types', 'COLLECTION')))        
#         conds.append(
#             self.bld.comp(self.bld.fn_call(self.bld.ref('len'), [ match_coll_expr ]),
#                                 'eq', self.bld.cnst(len(clause_coll_term))))
        
#         # compare coll's element-by-element
#         for i, clause_el_val in enumerate(clause_coll_term):
#             cur_pos = pos + [ i ]
#             match_el_expr = self.bld.index(match_coll_expr, i)
            
#             match clause_el_val.type():
#                 case term_types.COLLECTION:
#                     self.__unify_coll(clause_el_val, cur_pos, match_el_expr, clause_fn, conds, assns)
                
#                 case term_types.VAR:
#                     # TODO (long-term) only need assignment is var is None
#                     # either var was not provided, or it is equal to value from match_coll
#                     if clause_el_val.name in clause_fn.avail_vars:
#                         conds.append(self.bld.disj([
#                             self.bld.comp(self.bld.ref(clause_el_val.name), 'is', self.bld.cnst(None)),
#                             self.bld.comp(self.bld.ref(clause_el_val.name), 'eq', self.gen._term_val(match_el_expr))
#                         ]))
#                     # assign match_coll value to clause var
#                     assns.append(
#                         self.bld.assn(clause_el_val.name, self.gen._term_val(match_el_expr)))
                    
#                 case _:
#                     # add comparison condition for concrete values
#                     conds.append(
#                         self.bld.comp(self.gen._term_val(match_el_expr), 'eq', self.bld.cnst(clause_el_val.idx_val())))