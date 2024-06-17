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
        
        self.__unify_head = UnifyCoref_Head()
        self.__unify_body = UnifyCoref_Body()
        self.__unify_data_coll = UnifyDataColl()
        
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
        in_vars = head._vars()
        
        self.__clause_fn = RuleFn(in_vars=in_vars)
        
        self.__unify_head.unify(head, body, self.__clause_fn, self.__ctu_fn) 
        
        self.__cur_vars = in_vars

        if body.type() == term_types.GRAPH:
            for i, _ in enumerate(body.model.triples()):
                self.__gen_clause(rule_no, head, body, i)

        elif body.type() == term_types.LITERAL and body.value == True:
            self.__gen_clause(rule_no, head, None, 0)

    def __gen_clause(self, rule_no, head, body, clause_no):
        # incoming parameters representing variables
        in_vars = self.__cur_vars
        
        # adt representing clause fn
        self.__clause_fn = self.__clause_fn if self.__clause_fn is not None else RuleFn()
        self.__clause_fn.in_vars = in_vars
        self.__clause_fn.name = self.__fn_name(rule_no, clause_no)
        
        self.__ctu_fn = RuleFn(name=(self.__fn_name(rule_no, clause_no+1) if clause_no < body.model.len() - 1 else 'ctu'))

        # fn ast representing this clause
        self.__clause_fn.fn = self._rule_fn_def(self.__clause_fn.name, in_vars)
        self.__code.append(self.__clause_fn.fn) # add to generated code

        # running example: clause = ?p :address ?a ; cur_vars = [ p, r ] ; head = ?p a :Person

        # e.g., boolean as body
        if body is None:
            if len(self.__clause_fn.body) == 0:
                self.__builder.fn_body_stmt(self.__clause_fn.fn, self.__builder.pss())
            return
        
        clause = body.model.triple_at(clause_no)

        self.__unify_body.unify(clause, self.__clause_fn, self.__ctu_fn)

        # ex: [ p, a ]
        own_vars = clause._vars()

        if clause_no < body.model.len() - 1:
            # parameters for the ctu function; unique(prior + own vars) ; ex: p, r, a
            self.__ctu_fn.in_vars = list(dict.fromkeys(self.__cur_vars + own_vars)) # (keep order)
            self.__cur_vars = self.__ctu_fn.in_vars
        else:
            # only pass var needed by original ctu fn (head vars!) ; ex: p
            self.__ctu_fn.in_vars = head._vars()

        # if self.__is_builtin(clause):
        #     self.__run_builtin(clause_fn, clause, in_vars, ctu_fn, ctu_vars)
        # else:
        self.__find_data_call(clause, self.__clause_fn, self.__ctu_fn)
        self.__match_rule_calls(clause, self.__clause_fn, self.__ctu_fn)

    
    # START find triple
    
    def __find_data_call(self, clause, clause_fn, ctu_fn):
        clause = self.__unify_data_coll.unify(clause, clause_fn, ctu_fn)
        
        #  arguments for data.find call

        # s, p, o from clause will be search terms
        #   if variable: if provided as argument, refer to the function argument, else None
        #   (ungrounded-collections) if coll with variables: provide None (requires separate unification) 
        #   else, use resource from clause
        call_args = []
        for r in clause:
            match r.type():
                
                case term_types.VAR:
                    varname = self.__safe_intn_var(r.name)
                    # when given as var, can pass it
                    call_args.append(self._var_ref(varname) if varname in clause_fn.in_vars else self.__builder.cnst(None))
                
                # TODO if possible, unify collection and pass in search
                case term_types.COLLECTION: # (ungrounded-collections)
                    call_args.append(self.__builder.cnst(None) if not r.is_grounded() else self._val(r))
                
                case _: call_args.append(self._val(r))
                
        # build the ctu call
        ctu_call = self.__find_data_ctu(clause, clause_fn, ctu_fn)
        
        # then, create lambda with as body the ctu call
        lmbda = self.__builder.lmbda(['t', 'state'], ctu_call)

        # finally, create data.find call
        call_args += [self.__builder.ref('state'), lmbda]
        search_call = self.__builder.fn_call(
            self.__builder.attr_ref('data', 'find'), call_args)

        self.__builder.fn_body_stmt(
            clause_fn.fn, self.__builder.stmt(search_call))
    
    def __find_data_ctu(self, clause, clause_fn, ctu_fn):
        # ex: { 'p' : 's', 'a': 'o' }
        clause_vars = {v:['s', 'p', 'o'][i] for i, v in enumerate(clause)}

        # arguments to be passed to ctu
        ctu_fn.in_args = [self._triple_val('t', clause_vars[v]) if v in clause_vars else self.__builder.ref(v)
                     for v in ctu_fn.in_vars]

        # model.find will call a lambda
        # this lambda will itself call a ctu
        
        if ctu_fn.req_separ_fn():
            self.__gen_separ_ctu_fn(clause_fn, ctu_fn)

        # ex: ctu_fn = rule0_1 or ctu (original parameter)
        return self._rule_fn_call(ctu_fn.name, ctu_fn.in_args)
        
    # END find triple    
    
    # START match call
    
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
                    
                    # check consistency between match_r and clause_r
                    # (also, pass appropriate arguments to match rule fn)
                    if not self.__match_call_coll(match_r, clause_r, clause_fn, ctu_fn, match_fn):
                        return False
                else:
                    if not self.__match_call_terms(match_r, clause_r, clause_fn, ctu_fn, match_fn):
                        return False

            # build the ctu call

            if ctu_fn.req_separ_fn():
                self.__gen_separ_ctu_fn(clause_fn, ctu_fn)

            ctu_call = self._rule_fn_call(ctu_fn.name, ctu_fn.in_args)

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
    
    # unify clause term with match clause term
    def __match_call_terms(self, match_r, clause_r, clause_fn, ctu_fn, match_fn):
        if match_r.is_concrete():
            if clause_r.is_concrete():
                # (ungrounded-collections)
                if clause_r.is_grounded() and match_r.is_grounded() and clause_r != match_r:  # compile-time check
                    print("compile-time check: nok")
                    return False
            else:
                clause_varname = self.__safe_intn_var(clause_r.name)
                # add runtime check, if possible
                if clause_varname in clause_fn.in_vars:
                    cmp1 = self.__builder.comp(self._var_ref(clause_varname), 
                                                'is', self.__builder.cnst(None))
                    cmp2 = self.__builder.comp(self._var_ref(clause_varname), 'eq', self._val(match_r))
                    match_fn.conds.append(self.__builder.disj([cmp1, cmp2]))

                # clause has variable; match rule has concrete value
                # if successful, pass concrete value to ctu, if needed
                if clause_varname in ctu_fn.in_vars:
                    ctu_fn.in_args[ctu_fn.in_vars.index(clause_varname)] = self._val(match_r)
        
        else: # pass data as arguments; get results as lambda parameters
            if clause_r.is_concrete():
                match_varname = self.__safe_extn_var(match_r.name)
                match_fn.get_vars.append(match_varname)
                match_fn.in_args.append(self._val(clause_r))
            else:
                clause_varname = self.__safe_intn_var(clause_r.name)
                # always get value from match clause / find call; 
                # either we gave None, or it is the same as what we gave
                match_fn.get_vars.append(clause_varname)
                if clause_varname in clause_fn.in_vars:
                    # pass var to rule fn call, if given as input
                    match_fn.in_args.append(self._var_ref(clause_varname))
                else: # else, pass None
                    match_fn.in_args.append(self.__builder.cnst(None))
                    
        return True
        
    # (ungrounded-collections)
    # returns false if match_r coll is not consistent with clause_r
    # also, fn passes appropriate arguments for these params based on clause_r
    # (note that rule fns will have separate params for each of its coll var)
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
                clause_varname = self.__safe_intn_var(clause_r.name)
                if clause_varname in ctu_fn.in_vars: # only if this var is actually used, lol
                    ctu_fn.in_args[ctu_fn.in_vars.index(clause_varname)] = self._reconstr(match_r, ext_vars=True)
                    
                # (after, still need to process match_r (i.e., pass None's, collect its vars))
        
            # if match_r is var, clause_r was ungrounded coll: 
            # need to pass _grounded collection_ to match fn
            # TODO ensure full grounding by skolemization or whatever
            elif not match_r.is_concrete():
                match_varname = self.__safe_extn_var(match_r.name)
                match_fn.get_vars.append(match_varname)
                match_fn.in_args.append(self._reconstr(clause_r))
                return True # nothing left to do
        
        # compare element-by-element
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
                    match_varname = self.__safe_extn_var(match_r2.name)
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
            
    # END match call
    
    def __gen_separ_ctu_fn(self, clause_fn, ctu_fn):
        ctu_fn.name = f"{clause_fn.name}_unify"
        
        new_fn = self._rule_fn_def(ctu_fn.name, ctu_fn.in_vars)
        self.__code.append(new_fn)
        
        to_add = ctu_fn.body
        if len(ctu_fn.conds) > 0:
            to_add = self.__builder.iif(
                self.__builder.conj(ctu_fn.conds),
                ctu_fn.body
            )
        
        self.__builder.fn_body_stmts(new_fn, to_add)
            
    # def __is_builtin(self, clause):
    #     return clause.p.type() == term_types.IRI and clause.p.ns.startswith(swapNs.iri)
    
    # def __run_builtin(self, clause_fn, clause, in_vars, ctu_fn, ctu_vars, rest_args):
    #     match clause.p.ln:
    #         case 'notEqualTo': ...
    #         case _: raise GenError(f"unsupported builtin: '{clause.p.ln}'")
         
    # helper functions
    
    def __fn_name(self, rule_no, clause_no):
        if clause_no == 0:
            return f"{self.__fn_prefix}_{rule_no}"
        else:
            return f"{self.__fn_prefix}_{rule_no}_{clause_no}"

    def _val(self, r):
        return self.__builder.cnst(r.idx_val())
    
    def _var_ref(self, name):
        return self.__builder.ref(name)
    
    def _triple_val(self, t, spo):
        return self.__builder.fn_call(self.__builder.attr_ref_expr(self.__builder.attr_ref(t, spo), 'idx_val'))

    def _term_val(self, expr):
        return self.__builder.fn_call(self.__builder.attr_ref_expr(expr, 'idx_val'))
        
    def _rule_fn_def(self, fn_name, params):
        my_params = params + self.__inner_fn_params
        return self.__builder.fn(fn_name, my_params)
        
    def _rule_fn_call(self, fn_name, args):
        my_args = args + (self.__rule_fn_args if fn_name == 'ctu' else self.__inner_fn_args)
        return self.__builder.fn_call(self.__builder.ref(fn_name), my_args)
            
    def _reconstr(self, r, ext_vars=False):
        match r.type():
            case term_types.IRI: 
                cls = "Iri"; arg = r.iri
            case term_types.LITERAL: 
                cls = "Literal"; arg = r.value
            case term_types.COLLECTION: 
                cls = "Collection"
                arg = self.__builder.lst([ self._reconstr(e, ext_vars) for e in r ])
            case term_types.VAR: 
                return self._var_ref(self.__safe_var(r.name, ext_vars))
            case _: print("inconceivable")

        return self.__builder.fn_call(fn=self.__builder.ref(cls), args=[arg])

    # NOTE code assumes this does not occur often
    # (else, optimize this)
    # consider simply renaming all unique vars to unique names 
    # (cfr. eye)
    
    def __safe_var(self, n, ext_vars=False):
        return self.__safe_extn_var(n) if ext_vars else self.__safe_intn_var(n)
    
    def __safe_intn_var(self, n):
        n2 = None
        match n:
            case 't': n2 = 'tt'
            case 'data': n2 = 'dataa'
            case 'state': n2 = 'statee'
            case 'ctu': n2 = 'ctuu'
            case _: return n
        
        # ensure new var does not occur in this rule
        return self.__safe_extn_var(n2)
        
    def __safe_extn_var(self, n):
        if n not in self.__all_rule_vars:
            return n
        else:
            return self.__safe_extn_var(n + "2")


class RuleFn:
    
    # name (string)
    # in_vars (strings; incoming parameters representing variables)
    # in_args (ast; arguments for in_vars)
    # clause_vars (strings)
    # fn (ast)
    
    # cond
    # body
    
    def __init__(self, name=None, in_vars=None, fn=None):
        self.name = name
        self.in_vars = in_vars
        self.fn = fn
        
        self.cond = []
        self.body = []
        
    def req_separ_fn(self):
        return len(self.cond) > 0 or len(self.body) > 0
    
    
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
    

# unify hooks

class UnifyCoref:
    
    # gen, bld
        
    def __init__(self, gen):
        self.gen = gen
        self.bld = gen.__builder
        
    # returns:
    # ( list of de-duplicated, unique variables; map from original var -> list of renamed vars)
    #  e.g., (p, p, s) -> new_vars=(p0, p1, s), ren_vars={p: [ p0, p1 })
    def _deduplicate_vars(self, vars):
        counts = { v:0 for v, c in Counter(vars).items() if c > 1 }
        
        new_vars = []; ren_vars = { v: [] for v in counts }
        for v in vars:
            if v in counts:
                nv = f"{v}{len(counts[v])}"
                counts[v] += 1
                new_vars.append(nv); ren_vars[v].append(nv)
            else:
                new_vars.append(v)
        
        return ( new_vars, ren_vars )
    

class UnifyCoref_Head(UnifyCoref) :
    
    # gen, bld
    
    def __init__(self, gen):
        super().__init__(gen)
    
    # we do 2 things here:
    # 1/ ok if all _provided_ (de-)duplicated vars are same
    # 2/ pass provided var values for non-provided vars
    def unify(self, head, body, clause_fn):
        orig_vars = head._vars()
        
        # whew, no need to unify!
        if len(orig_vars) == len(set(orig_vars)): 
            return
        
        # darn :-(
        # start with renaming variables so each are unique
        # (also, keep map from original to renamed vars)
        ( new_vars, ren_vars ) = self._deduplicate_vars(orig_vars)
        # print("dedupl:", dupl_vars, ren_vars)
        
        # unique vars will be input var params
        clause_fn.in_vars = new_vars
        
        # rename vars in head clause
        # e.g., ?desc :parent ?desc -> ?desc0 :parent ?desc1 
        # stmts in body will check desc0 = desc1 etc
        head._rename_vars(ren_vars)

        # rename vars in body clause
        # (nrs don't matter; desc0, desc1, will all be None or equal here)
        # e.g., ?desc :abc ?desc -> ?desc0 :abc ?desc1
        body._rename_vars(ren_vars)
        
        in_vars = [ v for v in ren_vars ]
        self.__unify_head_vars(in_vars, 0, [], [], clause_fn.body)

    
    # bound: vars that are bound at this point; unbound: idem for unbound vars
    def __unify_head_vars(self, vars, idx, bound, unbound, body):
        var = vars[idx]
        
        if_body = []; else_body = []
        
        # IF: var is not None
        
        body.append(self.bld.iif(self.bld.comp(self.bld.ref(var), 'is not', self.bld.cnst(None)), if_body, else_body))
        # add stuff to if's body from here
        
        # compare the last two bound vars
        if len(bound) > 0:
            if_body2 = []
            if_body.append(self.bld.iif(self.bld.comp(self.bld.ref(bound[-1]), 'eq', self.bld.ref(var)), if_body2))
            if_body = if_body2 # add the rest to this if's body!
        
        # (var is not None, so add to bound)
        bound.append(var)
        if idx+1 < len(vars):
            # for case where this var is bound, process next var
            self.__unify_head_vars(vars, idx+1, bound[:], unbound[:], if_body)
        else:
            # if last var, then we made it!
            if_body.append(self.bld.stmt(self.gen._rule_fn_call(self.bld.ref('ctu'), self.__ctu_args(vars, bound))))
        
        # ELSE: (so, var is None)
        
        bound.pop() # remove from bound
        unbound.append(var) # add to unbound
        
        if idx+1 < len(vars):
            # here, this var is _not_ bound; process next var
            self.__unify_head_vars(vars, idx+1, bound[:], unbound[:], else_body)
        elif len(bound) > 0:
            # if last var, we made it!
            else_body.append(self.bld.stmt(self.gen._rule_fn_call(self.bld.ref('ctu'), self.__ctu_args(vars, bound))))
            
    def __ctu_args(self, vars, bound):
        # (if a var was not provided, pass one of the bound vars instead)
        return [ self.bld.ref(var) if var in bound else self.bld.ref(bound[0]) for var in vars ] + [ self.bld.ref('state') ]
        
        
class UnifyCoref_Body(UnifyCoref):
    
    # gen, bld
    
    def __init__(self, gen):
        super().__init__(gen)
    
    def unify(self, clause, clause_fn, ctu_fn):
        orig_vars = clause._vars()
        (new_vars, ren_vars) = self._deduplicate_vars(clause._vars())
        
        # e.g., x -> x1, x2
        
        clause._rename_vars(self, ren_vars)
        
        # x1 = x; x2 = x        
        clause_fn.body.extend([ self.bld.assn(ren_var, self.bld.ref(orig_var)) for orig_var in ren_vars for ren_var in ren_vars[orig_var] ])
        
        # x1 == x2
        ctu_fn.cond.extend(self.bld.comps('eq', [ ren_var for orig_var in ren_vars for ren_var in ren_vars[orig_var] ]))
        
        # x = x1 (x1, x2 are guaranteed the same at this point)
        ctu_fn.body.extend([ self.bld.assn(orig_var, self.bld.ref(ren_vars[orig_var][0])) for orig_var in ren_vars ])
        
        # vars for the "original" ctu call (which we substituted)
        origin_ctu_vars = list(dict.fromkeys(clause_fn.in_vars + orig_vars))
        # create call to original ctu
        ctu_fn.body.append(self.gen._rule_fn_call(ctu_fn.name, [ self.bld.ref(v) for v in origin_ctu_vars ]))
        


class UnifyDataColl(UnifyCoref):
    
    def __init__(self, gen):
        super().__init__(gen)
        
    def unify(self, clause, clause_fn, ctu_fn):
        ungr_colls = [ (pos, term) for pos, term in enumerate(clause) if term.type() == term_types.COLLECTION and not term.is_grounded()]
        
        # whew, no need to unify!
        if len(ungr_colls) == 0:
            return
        
        # e.g., :x :y ( 1 2 ?z )
        
        # darn :-(
            
        clause = clause.clone() # shallow copy
        
        if_test = []; if_body = []    
        for i, (pos, coll) in enumerate(ungr_colls):
            coll_var = self.bld.ref(f'coll_{i}')
            
            # replace ungrounded collections with variables
            clause[pos] = coll_var # TODO var-conflicts

            self.__unify_coll(coll, [], coll_var, clause_fn, if_test, if_body)
            
        # coll0[0]==1 and coll0[1]==2
        ctu_fn.cond.append(self.bld.conj(if_test) if len(if_test) > 1 else if_test[0])
        
        # z = coll0[2]
        ctu_fn.body.extend(if_body)
        
        return clause

    # 1/ add conditions for element-by-element comparisons
    # 2/ add assignments of match coll values to clause vars 
    # clause_coll_term: term in clause_coll
    # match_coll_expr: corresp. select in match_coll (e.g., coll[0][1])
    # pos: (nested) position (e.g., [0, 1] for 2nd el in 1st el)
    def __unify_coll(self, clause_coll_term, pos, match_coll_expr, clause_fn, conds, assns):
        # match_coll needs to be collection of same length
        conds.append(
            self.bld.comp(
                self.gen._rule_fn_call(self.bld.attr_ref_expr(match_coll_expr, 'type')),
                'eq', self.bld.attr_ref('term_types', 'COLLECTION'))
        )        
        conds.append(
            self.bld.comp(self.gen._rule_fn_call(self.bld.ref('len'), [ match_coll_expr ]),
                                'eq', self.bld.cnst(len(clause_coll_term)))
        )
        
        # compare coll's element-by-element
        for i, clause_el_val in enumerate(clause_coll_term):
            cur_pos = pos + [ i ]
            match_el_expr = self.bld.index(match_coll_expr, i)
            
            match clause_el_val.type():
                case term_types.COLLECTION:
                    self.__unify_coll(clause_el_val, cur_pos, match_el_expr, clause_fn, conds, assns)
                
                case term_types.VAR:
                    # TODO only need assignment is var is None
                    # either var was not provided, or it is equal to value from match_coll
                    if clause_el_val.idx_val() in clause_fn.in_vars:
                        conds.append(self.bld.disj([
                            self.bld.comp(self.bld.ref(clause_el_val.name), 'is', self.bld.cnst(None)),
                            self.bld.comp(self.bld.ref(clause_el_val.name), 'eq', self.gen._term_val(match_el_expr))
                        ]))
                    # assign match_coll value to clause var
                    assns.append(
                        self.bld.assn(clause_el_val.name, self._term_val(match_el_expr)))
                    
                case _:
                    # add comparison condition for concrete values
                    conds.append(
                        self.bld.comp(self.gen._term_val(match_el_expr), 'eq', self.bld.cnst(clause_el_val.idx_val())))