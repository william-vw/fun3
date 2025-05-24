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
    
    # __inner_fn_params (+ __inner_fn_args)
    # __rule_fn_params (+ __rule_fn_args)

    def __init__(self):
        self.bld = PyBuilder()
        self.__fn_prefix = "rule"
        self.__var_cnt = 0
        
        # parameters that each function will have
        self.__inner_fn_params = [ 'data', 'state', 'ctu' ]
        self.__rule_fn_params = [ 'state' ]
        self.__inner_fn_args = [self.bld.ref(v) for v in self.__inner_fn_params]
        self.__rule_fn_args = [self.bld.ref(v) for v in self.__rule_fn_params]

    def gen_python(self, rules):
        # 
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
        """
        Generates all functions to implement the rule with given rule_no, head & body.
        
        Args:
            rule_no: the rule's unique number (used as basis for function names for body tp's). 
            head: the rule's head graph.
            body: the rule's body graph.
        """
        
        in_vars = head._recur_vars()
        first_fn = RuleFn(in_vars=in_vars)
        
        # if needed, unify coref vars in head
        # (will update clause_fn & its in_vars)
        # self.__unify_head.unify(head, body, first_fn)
        
        # keeps track of vars for subsequent clauses
        # initially, vars in rule head; updated with vars from subsequent clauses
        self.__cur_vars = first_fn.in_vars

        if body.type() == term_types.GRAPH:
            for i, _ in enumerate(body.model.triples()):
                self.__gen_clause(rule_no, head, body, i, (first_fn if i==0 else None))

        elif body.type() == term_types.LITERAL and body.value == True:
            self.__gen_clause(rule_no, head, None, 0, first_fn)

    def __gen_clause(self, rule_no, head, body, clause_no, clause_fn):
        """
        Generates a single function to implement the body tp identified by clause_no.
        
        Args:
            rule_no: the rule's unique number (used as basis for function names for body tp's). 
            head: the rule's head graph.
            body: the rule's body graph.
            clause_no: the body tp's index in the body graph.
            clause_fn: for the first body tp, its function (will have been unified with rule head.)
        """
        
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
                
        # current clause (triple)
        clause = body.model.triple_at(clause_no)
        
        # ADT representing ctu fn (i.e., fn to be called after clause fn)
        # (either fn for the next clause, or original 'ctu' fn for this rule)
        is_last = (clause_no == body.model.len() - 1)
        ctu_fn = RuleFn(name=(self._fn_name(rule_no, clause_no+1) if not is_last else 'ctu'), is_last=is_last)
        
        # vars occurring in clause (non-recursively)
        own_vars = [ v for _, v in clause._vars() ]
        
        if not ctu_fn.is_last:
            # params to pass to next clause fn; unique(prior vars + own vars)
            ctu_fn.in_vars = list(dict.fromkeys(self.__cur_vars + own_vars)) # (keep order)
        else:
            # only pass vars needed by original ctu fn (head vars!)
            ctu_fn.in_vars = head._recur_vars()
        
        # keep track of vars in subsequent clauses
        if not ctu_fn.is_last:
            # (recur_vars; all nested vars have to be passed as well; happens in unify op)
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
        """
        Generates a call to find triples matching the body tp (clause parameter).
        
        Args:
            head: the rule's head graph.
            body: the rule's body graph.
            clause: the body tp.
            clause_fn: the function representing the body tp.
        """
        
        unify = Unify(self, self.bld, find_data=True)
        
        # if needed, unify co-ref vars in clause
        unify.unify_coref(clause)
        
        # if needed, unify ungrounded collections in clause with data
        unify.unify_coll_data(clause, clause_fn)
                 
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
                
                # TODO (long-term) if possible, ground collection and provide as search param
                case term_types.COLLECTION: # (ungrounded-collections)
                    call_args.append(self.bld.cnst(None) if not r.is_grounded() else self._val(r))
                
                case _: call_args.append(self._val(r))
        
        # ctu vars ; ex: { 'p' : 's ', 'a': 'o' }
        clause_vars = { v: Triple.spo[i] for i, v in clause._vars(get_name=True) }
        # for each expected argument for the ctu fn (ctu_fn.in_vars),
        # if found in the clause's own vars, then return the corresponding term in the matched triple
        # if not, simply pass on this function's own argument
        ctu_fn.in_args = [self._triple_val('t', clause_vars[v]) if v in clause_vars else self.bld.ref(v)
                     for v in ctu_fn.in_vars]
        
        # let unif do its thing, if needed
        ctu_fn = unify.finalize(clause_fn, ctu_fn)
        
        # build the ctu call
        
        ctu_call = self._rule_fn_call(ctu_fn.name, ctu_fn.in_args)
        
        # then, create lambda with as body the ctu call
        # will accept the triple and the state
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
        """
        Generates a call to find triples matching the body tp (clause parameter).
        
        Args:
            head: the rule's head graph.
            body: the rule's body graph.
            clause: the body tp.
            clause_fn: the function representing the body tp.
        """
        
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
            # by default, these are simply references to input vars
            ctu_fn.in_args = [ self.bld.ref(p) for p in ctu_fn.in_vars ]
            
            match_fn = MatchRuleFn()
            
            head = match.rule.s
            match_clause = head.model.triples()[0]
            
            self.unify = Unify(self, self.bld, find_data=False, id=match.fn_name)
            
            if not self.__match_clauses(clause, match_clause, clause_fn, ctu_fn, match_fn):
                continue
        
            # if needed, unify co-ref vars in clause
            self.unify.unify_coref(clause)
            
            # let unif do its thing, if needed
            ctu_fn = self.unify.finalize(clause_fn, ctu_fn, match_fn)

            # build the ctu call

            ctu_call = self._rule_fn_call(ctu_fn.name, ctu_fn.in_args)

            # lambda params: vars we want from match rule fn (+ extra params)
            lmbda_params = match_fn.get_vars + [ 'state' ]
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
                    # print("compile-time check: nok")
                    return False
            else:
                # add runtime check, if needed
                if clause_r.name in clause_fn.avail_vars:
                    cmp1 = self.bld.comp(self._var_ref(clause_r.name), 
                                                'is', self.bld.cnst(None))
                    cmp2 = self.bld.comp(self._var_ref(clause_r.name), 'eq', self._val(match_r))
                    match_fn.cond.append(self.bld.disj([cmp1, cmp2]))

                # clause has variable; match rule has concrete value
                if clause_r.name in ctu_fn.in_vars:
                    # pass matching function's value for variable to ctu
                    ctu_fn.in_args[ctu_fn.in_vars.index(clause_r.name)] = self._val(match_r)
        
        else: 
            # matching rule head has term as a var, so it will be a fn parameter there
            
            # var result will always be passed by that fn (even if we don't need it)
            match_fn.get_vars.append(match_r.name) # use same var name in lambda
            if clause_r.is_concrete():
                # simply pass data as argument
                match_fn.in_args.append(self._val(clause_r))
                # (here, we don't need var result)
            else:
                # simply pass the var as an argument, if needed
                match_fn.in_args.append(self._var_ref(clause_r.name) if clause_r.name in clause_fn.avail_vars else self.bld.cnst(None))
                # here, we need var result from function; pass matching function's value for variable to ctu
                ctu_fn.in_args[ctu_fn.in_vars.index(clause_r.name)] = self._var_ref(match_r.name)
                # # trick; ctu_fn already uses clause_r.name in its args (but, won't work in other lang, so don't use it)
                # match_fn.get_vars.append(clause_r.name)
                    
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
            # TODO (long-term) if possible, ground collection and provide as search param
            elif not match_r.is_concrete():
                match_fn.get_vars.append(match_r.name)
                match_fn.in_args.append(self.bld.cnst(None))
                # will require separate unif fn
                self.unify.unify_coll_match(clause_r, match_r, clause_fn)
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
        """
        Pre-process the given set of rules. 
        It renames all variables per rule so they are unique across all rules to simplify matters.
        It creates an index (__pred_idx) that maps head triple predicates to function names.
        
        Args:
            rules (collection): set of triples representing rules 
        """
        
        # map of rule predicates to functions (FnIdxEntry) implementing them.
        # keys:
        #   - 'var': for triples with variable predicate
        #   - 'all': all functions
        #   - <uri>: for triples with concrete predicate
        self.__pred_idx = MultiDict()

        i = 0
        while i < len(rules):
            r = rules[i]
            
            # giving up & just giving all vars unique names
            self.__rename_vars_unique(r.s, r.o)
            
            # top-down rules need heads with len 1
            if r.s.model.len() != 1:
                print(f"warning: cannot use rule, length of head > 1 ({r})")
                del rules[i]; continue
            # only top-down rules
            if r.p.iri == n3Log['implies']:
                print(f"warning: cannot use bottom-up rule ({r})")
                del rules[i]; continue

            entry = FnIdxEntry(r, self._fn_name(i, 0))
            # iterate over all triples in head (just one really)
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
        """
        Generates unique function name for a rule head or body triple
        
        Args:
            rule_no: rule number
            clause_no: 0 if rule head, > 0 if body triple ??
            
        Returns:
            Unique function name
        """
        
        if clause_no == 0:
            return f"{self.__fn_prefix}_{rule_no}"
        else:
            return f"{self.__fn_prefix}_{rule_no}_{clause_no}"

    def _val(self, r):
        return self.bld.cnst(r.idx_val())
    
    def _var_ref(self, name):
        return self.bld.ref(name)
    
    def _triple_val(self, t, spo, raw_val=True):
        triple_ref = self.bld.attr_ref(t, spo)
        if raw_val:
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
    
    def _raw_type_check(self, ref, adt_type):
        raw_type = None
        match adt_type:    
            case term_types.COLLECTION:
                raw_type = 'tuple'
            case _: print("inconceivable!")

        return self.bld.comp(
            self.bld.fn_call(self.bld.ref('type'), [ ref ]), 'eq',
            self.bld.ref(raw_type)
        )
    
    def __rename_vars_unique(self, head, body):
        # all variables (possibly duplicate) in head & body
        triple_it = \
                chain(head._recur_vars(), body._recur_vars()) \
            if body.type() == term_types.GRAPH else \
                head._recur_vars()
        # use dict to have 1 entry per variable
        # (head & body can share same variables)
        unique_vars = { v:0 for v in triple_it }
        # for each unique var in head+body, assign unique value "v_i" based on var count
        unique_vars = { v:f"{v}_{i}" for v,i in zip(unique_vars, range(self.__var_cnt, len(unique_vars)+self.__var_cnt)) }
        
        # rename vars in head & body
        head._rename_recur_vars(unique_vars)
        if body.type() == term_types.GRAPH:
            body._rename_recur_vars(unique_vars)
        
        # update var count
        self.__var_cnt += len(unique_vars)
        

class RuleFn:
    """
    A function implementing a body triple from a rule.
    
    Attributes:
        name (str): function name
        in_vars (list of str): incoming params representing vars
        in_args (list of ast): argument ast's for in_vars
        fn (ast): corresponding ast object
        is_last (bool): whether the body triple is the last one in the body
    """
    
    
    def __init__(self, name=None, in_vars=None, in_args=None, fn=None, is_last=False):
        self.name = name
        self.in_vars = in_vars if in_vars is not None else []
        self.in_args = in_args if in_args is not None else []
        self.fn = fn
        self.is_last = is_last
        self.body = [] # TODO head unif
        
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
    
    """
    Call of a function that was matched to a rule body triple pattern (btp).
    
    Attributes:
        cond (list): potential conditions to be checked before function call should be made.
        in_args (list): arguments (ast's) that will be passed to the function call.
        get_vars (list): parameters that will be received from the called function 
            (i.e., the function will itself call a ctu with arguments for these parameters)
    """
    
    # conds (runtime conditions before calling match rule fn)
    # in_args (args to provide to match fn's vars)
    # get_vars (vars to get from match rule fn; will serve as lambda params)

    def __init__(self):
        self.cond = []
        self.in_args = []
        self.get_vars = []

class FnIdxEntry:

    """
    An index entry for a function related to a rule head or a body triple.
    
    Attributes:
        rule: entire rule (rule head) or triple (body triple)
        fn_name (str): function name
    """

    # rule (triple)
    # fn_name

    def __init__(self, rule, fn_name):
        self.rule = rule
        self.fn_name = fn_name

    def __str__(self):
        return f"<{self.fn_name} - {str(self.rule)}>"
    def __repr__(self):
        return self.__str__()
    

# unify

class Unify:
    
    # gen, bld
    # find_data
    
    # in_args, in_var, new_vars, lmbda_vars
    # conds, assns
        
    def __init__(self, gen, bld, find_data, id=None):
        self.gen = gen
        self.bld = bld
        self.find_data = find_data
        self.id = id if id is not None else 'data'
        
        self.in_args = []; self.in_vars = []; self.new_vars = []
        self.lmbda_vars = MultiDict()
        self.conds = []; self.assns = []
        
    def __unify_entry(self, arg, var):
        if var not in self.in_vars:
            self.in_args.append(arg)
            self.in_vars.append(var)
            
    def __unify_found_var(self, var):
        if var not in self.new_vars:
            self.new_vars.append(var)
        
    def __update_lmbda_vars(self, lmbda_vars):
        self.lmbda_vars.extend(lmbda_vars)
        
    def __req_unify_fn(self):
        return len(self.in_args) == 0
        
    # if needed, build separate unif fn & return it    
    
    def finalize(self, clause_fn, ctu_fn, match_fn=None):
        if self.__req_unify_fn():
            return ctu_fn

        # create separ unif fn
        unif_fn = ctu_fn.clone()
        # won't be the last due to our unify fn
        unif_fn.is_last = False
        unif_fn.name = f"{clause_fn.name}_unify_{self.id}"
        # extend with unif fn args, params
        unif_fn.in_args.extend(self.in_args)
        unif_fn.in_vars.extend(self.in_vars)
        
        new_fn = self.gen._rule_fn_def(unif_fn.name, unif_fn.in_vars)
        self.gen._code.append(new_fn)
        
        # orig ctu fn will be called in body of unif fn
        
        # update ctu fn in_vars, if needed, with nested vars from ungr coll
        # (these are now avail in our unif fn)
        ctu_fn.in_vars.extend([ v for v in self.new_vars if v not in ctu_fn.in_vars ])
        # these will all be var refs (either from in params, or assns)
        ctu_fn.in_args = [ self.bld.ref(v) for v in ctu_fn.in_vars ]
        
        fn_body = self.assns
        # add call to orig ctu to our unif fn body
        fn_body.append(self.bld.stmt(self.gen._rule_fn_call(ctu_fn.name, ctu_fn.in_args)))
        
        # wrap fn body in if-stmt w/ unif conds
        if len(self.conds) > 0:
            fn_body = [ self.bld.iif(
                self.bld.conj(self.conds), fn_body) ]
            
        self.bld.fn_body_stmts(new_fn, fn_body)
        
        # ugh, have to update lambda params
        # TODO replace this with simply using var names from _called rule_
        # (no problem with var name clashes in lambda params)
        if not self.find_data:
            match_fn.get_vars = list(dict.fromkeys(match_fn.get_vars)) # may have duplicates
            get_vars = []
            # expand each dupl var with unique occ names
            # together, will constitute all vars given by match fn
            for v in match_fn.get_vars:
                if v in self.lmbda_vars:
                    get_vars.extend(self.lmbda_vars.getall(v))
                else:
                    get_vars.append(v)
            match_fn.get_vars = get_vars
        
        # will be called by 'regular' code!
        return unif_fn
    
    # START unify_coref
    
    # - gather extra args & params for unify fn
    # - build conds, assns for unific in fn

    def unify_coref(self, clause):
        orig_vars_pos = clause._recur_vars_pos()
        # print("orig_vars_pos", orig_vars_pos)
        orig_vars = [ v for _, v in orig_vars_pos ]
        
        # whew, no need to unify!
        if len(orig_vars) == len(set(orig_vars)): 
            return
        
        # darn :-(
        dupls = { v for v,c in Counter(orig_vars).items() if c > 1 }
        # print("dupls", dupls)
        
        # per triple spo, get unique names for dupl var occ (if needed, also for coll w/ dupl)
        # ex: { ?x :p ?x } = 0 -> ( x, x_s ), 2 -> ( x, x_o ) ; ex: { :a :p ( ?x ?x ) } = 2 -> ( x, coll_o )
        spo_var_occ = { self.__get_spo_pos(pos): (var, self.__get_spo_varname(pos, var)) for pos, var in orig_vars_pos if var in dupls }
        # print("spo_var_occ", spo_var_occ)
        
        # per dupl var occ, need extra in_arg and in_var for unif fn
        # (so we can manually unify them in unif fn)
        # TODO (long-term) results in redundant args
        for spo, (_, occ) in spo_var_occ.items():
            arg = self.gen._triple_val('t', Triple.spo[spo]) if self.find_data else self.bld.ref(occ)
            self.__unify_entry(arg, occ)
            # print(arg, "->", occ)
        
        if not self.find_data:
            # update lambda params
            # match rule will return values for each of its vars
            # "catch" those values with our dupl var occ
            lmbda_vars = MultiDict()
            for spo, (orig_var, occ) in spo_var_occ.items():
                # map orig_var to its occ's (will be replaced by latter)
                lmbda_vars.add(orig_var, occ)
            self.__update_lmbda_vars(lmbda_vars)

        # now, let's setup the unify conds

        # per orig (dupl) var, get positions of its occ's
        # ex: { ?x :p ?x } = x -> ((0, <triple>)), ((2, <triple>))
        # ex: { :a :p ( ?x ?x ) } = x -> ((2, <triple>), (0, <coll>)), ((2, <triple>), (1, <coll>))
        origvar_pos = MultiDict((orig_var, pos) for pos, orig_var in orig_vars_pos if orig_var in dupls)
        
        for orig_var in set(origvar_pos.keys()):
            # per orig (dupl) var, for each occ, get in_var & pos
            # ex: { ?x :p ?x } = [ ( x_s, () ), ( x_o, () ) ]
            # ex: { :a :p ( ?x ?x ) } = [ ( coll_o, (0, <coll>) ), ( coll_o, (1, <coll>) ) ]
            entries = []
            for pos in origvar_pos.getall(orig_var):
                ( _, occ ) = spo_var_occ[self.__get_spo_pos(pos)]; 
                entries.append((occ, pos[1:]))
            # print(origvar, entries)
            self.__unify_coref_var(orig_var, entries)
        
    def __get_spo_pos(self, pos):
        return pos[0][0]

    def __get_spo_varname(self, pos, var):
        i = self.__get_spo_pos(pos)
        return self.__varname(i, var) if len(pos) == 1 else self.__col_varname(i)

    def __unify_coref_var(self, origvar, entries):
        ops = []
        # ex: renvar=coll_o, posns=(0, <coll>) but could be deeper nested
        for (renvar, posns) in entries:
            ref = self.bld.ref(renvar)
            for pos in posns: # keep indexing until we're there
                ref = self.bld.index(ref, pos[0])
            ops.append(ref)
        
        # ex: x_s == x_o ; coll_o[0] == coll_o[1]
        self.conds.append(self.bld.comps('eq', ops))
        
        # (not actually needed in case of find_data)
        if not self.find_data:
            self.assns.append(self.bld.assn(origvar, ops[0]))
        
    # END unify_coref
    
    # START unify_coll
            
    def unify_coll_data(self, clause, clause_fn):
        ungr_colls = [ (i, term) for i, term in enumerate(clause) \
            if term.type() == term_types.COLLECTION and not term.is_grounded()]
        
        # whew, no need to unify!
        if len(ungr_colls) == 0:
            return clause
        
        # darn :-(
        # ex: :x :y ( 1 2 ?z )
        
        for (i, coll) in ungr_colls:
            # for each ungr coll, need extra in_arg and in_var for unif fn
            var = self.__col_varname(i)
            arg = self.gen._triple_val('t', Triple.spo[i])
            self.__unify_entry(arg, var)
            
            # add code to unify collection from the data (conds, assns)
            self.__unify_ungr_coll(coll, [], self.bld.ref(var), clause_fn, self.conds, self.assns)
    
    def unify_coll_match(self, clause_coll, match_var, clause_fn):
        self.__unify_entry(self.bld.ref(match_var.name), match_var.name)
        
        # add code to unify collection from data (conds, assns)
        self.__unify_ungr_coll(clause_coll, [], self.bld.ref(match_var.name), clause_fn, self.conds, self.assns)
        
    
    # 1/ add conditions for element-by-element comparisons
    # 2/ add assignments of match coll values to clause vars 
    # clause_coll_term: term in clause_coll ; match_coll_expr: corresp. in match_coll (e.g., coll[0][1])
    # pos: (nested) position (e.g., [0, 1] for 2nd el in 1st el)
    def __unify_ungr_coll(self, clause_coll_term, pos, match_coll_expr, clause_fn, conds, assns):
        # match_coll needs to be type collection of same length
        conds.append(self.gen._raw_type_check(match_coll_expr, term_types.COLLECTION))
        # conds.append(
        #     self.bld.comp(
        #         self.bld.fn_call(self.bld.attr_ref_expr(match_coll_expr, 'type')),
        #         'eq', self.bld.attr_ref('term_types', 'COLLECTION')))        
        conds.append(
            self.bld.comp(self.bld.fn_call(self.bld.ref('len'), [ match_coll_expr ]),
                                'eq', self.bld.cnst(len(clause_coll_term))))
        
        # compare coll's element-by-element
        for i, clause_el_val in enumerate(clause_coll_term):
            cur_pos = pos + [ i ]
            match_el_expr = self.bld.index(match_coll_expr, i)
            
            match clause_el_val.type():
                case term_types.COLLECTION:
                    self.__unify_ungr_coll(clause_el_val, cur_pos, match_el_expr, clause_fn, conds, assns)
                
                case term_types.VAR:
                    varname = clause_el_val.name
                    # TODO (long-term) only need assignment is var is None
                    # either var was not provided, or it is equal to value from match_coll
                    if varname in clause_fn.avail_vars:
                        conds.append(self.bld.disj([
                            self.bld.comp(self.bld.ref(varname), 'is', self.bld.cnst(None)),
                            self.bld.comp(self.bld.ref(varname), 'eq', match_el_expr) #self.gen._term_val(match_el_expr))
                        ]))
                    # assign match_coll value to clause var
                    assns.append(
                        self.bld.assn(varname, match_el_expr)) #self.gen._term_val(match_el_expr)))
                    # new var that we will now provide to orig ctu fn
                    self.__unify_found_var(varname)
                    
                case _:
                    # add comparison condition for concrete values
                    conds.append(
                        self.bld.comp(self.bld.cnst(clause_el_val.idx_val()), 'eq', match_el_expr)) #self.gen._term_val(match_el_expr)))
    
    # END unify_coll
    
    def __varname(self, pos, var):
        return f"{var}_{Triple.spo[pos]}"
    
    def __col_varname(self, pos):
        return f"coll_{Triple.spo[pos]}"
        
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
    
# TODO

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
#         return [ self.bld.ref(var) if var in bound else self.bld.ref(bound[0]) for var in vars 