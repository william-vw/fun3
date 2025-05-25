from enum import Enum
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


class Rule:
    
    def __init__(self, no, head, body):
        self.no = no
        self.head = head
        self.body = body
        self.cur_vars = []

    def add_cur_vars(self, vars):
        self.cur_vars = list(dict.fromkeys(self.cur_vars + vars)) 

    def set_new_vars(self, new_vars):
        self.new_vars = list(dict.fromkeys(self.cur_vars + new_vars)) 

    def update_new_vars(self):
        self.cur_vars = self.new_vars

    def has_runtime_val(self, var):
        return var in self.cur_vars

class Clause:
    
    def __init__(self, rule, no, tp):
        self.rule = rule
        self.no = no
        self.tp = tp
        
    def next_fn_name(self):
        return RuleFn.fn_name(self.rule.no, self.no + 1)
        
class RuleFn:
    
    __fn_prefix = "rule"
    
    def __init__(self, rule_no, clause_no):        
        self.name = RuleFn.fn_name(rule_no, clause_no)

    @staticmethod
    def fn_name(rule_no, clause_no):
        """
        Generates unique function name for a rule head or body triple

        Args:
        rule_no: rule number
        clause_no: 0 if rule head, > 0 if body triple ??

        Returns:
        Unique function name
        """

        if clause_no == 0:
            return f"{RuleFn.__fn_prefix}_{rule_no}"
        else:
            return f"{RuleFn.__fn_prefix}_{rule_no}_{clause_no}"
        

class FnIndex:
    
    """Map of rule predicates to functions (FnIdxEntry) implementing them.
    
    Attributes:
        - idx (MultiDict): predicate index with the following keys:
            <uri>: for triples with concrete predicate
            'var': for triples with variable predicate
            'all': all functions
    """
    
    def __init__(self):
        self.idx = MultiDict()
    
    def add(self, pred, entry):
        if pred.type() == term_types.VAR:
            self.idx.add('var', entry)
        else:
            self.idx.add(pred.idx_val(), entry)
            
        self.idx.add('all', entry)
        
    def find(self, tp):
        if tp.p.type() == term_types.VAR:
            return self.idx.getall('all')

        ret = []
        if tp.p.idx_val() in self.__pred_idx:
            ret.extend(self.idx.getall(tp.p.idx_val()))
        if 'var' in self.idx:
            ret.extend(self.idx.getall('var'))
        return ret

    def print(self):
        for k, v in self.idx.items(): print(k, ":\n", v, "\n")


class FnEntry:
    """
    An index entry for a function related to a rule head or a body triple.
    
    Attributes:
        rule: entire rule (rule head) or triple (body triple)
        fn_name (str): function name
    """

    def __init__(self, rule, rule_fn):
        self.rule = rule
        self.rule_fn = rule_fn

    def __str__(self):
        return f"<{self.rule_fn.name} - {str(self.rule)}>"
    def __repr__(self):
        return self.__str__()
    

class RuleProcessor_BuildFnIndex:
    
    def __init__(self, gen_python):
        self.fn_idx = FnIndex()
        gen_python.__fn_idx = self.fn_idx
    
    def process(self, rule_no, rule_triple):        
        entry = FnEntry(rule_triple, RuleFn(rule_no, 0))
        
        t = rule_triple.s.model.triple_at(0) # only 1 triple
        self.fn_idx.add(t.p, entry)


class RuleProcessor_UniqueVars:
    
    def __init__(self, _):
        self.var_cnt = 0
    
    # giving up & just giving all vars unique names
    def process(self, _, rule_triple):
        head = rule_triple.s
        body = rule_triple.o
        # all variables (possibly duplicate) in head & body
        triple_it = \
                chain(head._recur_vars(), body._recur_vars()) \
            if body.type() == term_types.GRAPH else \
                head._recur_vars()
        # use dict to have 1 entry per variable
        # (head & body can share same variables)
        unique_vars = { v:0 for v in triple_it }
        # for each unique var in head+body, assign unique value "v_i" based on var count
        unique_vars = { v:f"{v}_{i}" for v,i in 
                            zip(unique_vars, range(self.var_cnt, len(unique_vars)+self.var_cnt)) }
        
        # rename vars in head & body
        head._rename_recur_vars(unique_vars)
        if body.type() == term_types.GRAPH:
            body._rename_recur_vars(unique_vars)
        
        # update var count
        self.var_cnt += len(unique_vars)


class UOpTypes(Enum):
    CMP = 1
    TO_MATCH = 2
    FROM_MATCH = 3
    
class UOpRefs(Enum):
    DIRECT = 1
    RUNTIME = 2

class UOp:
    def __init__(self, type, ref, val1, val2):
        self.type = type
        self.ref = ref
        self.val1 = val1
        self.val2 = val2
    
    
class FnCall:
    
    def __init__(self, fn_ref, params=None, args=None):
        self.fn_ref = fn_ref
        
        self.args = {}
        if params is not None:
            for i in range(len(params)):
                self.args[params[i]] = args[i]
    
    def set_params(self, params, default):
        for param in params:
            self.args[param] = default
            
    def set_arg(self, param, arg):
        if param in self.args:
            self.args[param] = arg
            
    def get_args(self):
        return self.args.values()

    
class GenPython:

    def __init__(self):
        self.bld = PyBuilder()
        
        self.__rule_buildFnIdx = RuleProcessor_BuildFnIndex(self)
        self.__rule_renameVars = RuleProcessor_UniqueVars(self)

    def gen_python(self, rules):
        self.__process_rules(rules)
        
        for i, (head, _, body) in enumerate(rules):
            rule = Rule(i, head, body)
            self.__gen_rule(rule)

    def __process_rules(self, rules):
        """
        Pre-process the given set of rules. 
        It renames all variables per rule so they are unique across all rules to simplify matters.
        It creates an index (__pred_idx) that maps head triple predicates to function names.
        
        Args:
            rules (collection): set of triples representing rules 
        """

        for rule_no in range(len(rules)):
            rule = rules[rule_no]
            
            # top-down rules need heads with len 1
            if rule.s.model.len() != 1:
                print(f"warning: cannot use rule, length of head > 1 ({rule})")
                del rules[rule_no]; continue
            # only top-down rules
            if rule.p.iri == n3Log['implies']:
                print(f"warning: cannot use bottom-up rule ({rule})")
                del rules[rule_no]; continue

            self.__rule_renameVars.process(rule_no, rule)
            self.__rule_buildFnIdx.process(rule_no, rule)
        
        # self.__fn_idx.print()
    
    def __gen_rule(self, rule):
        rule.add_cur_vars(rule.head._vars())
        
        for no, tp in enumerate(rule.body.model.triples()):
            clause = Clause(rule, no, tp)
            rule.set_new_vars(tp._vars())

            if no == len(rule.body.model)-1:
                ctu_call = self.__gen_ctu_call('final_ctu', rule.head._vars(get_name=True))
            else:
                ctu_call = self.__gen_ctu_call(clause.next_fn_name(), rule.new_vars)

            self.__gen_clause(clause, ctu_call)

            rule.update_cur_vars()

    def __gen_ctu_call(self, name, params):
        return FnCall(self.bld.ref(name), 
            params=params, 
            args=[self.bld.ref(p) for p in params])

    def __gen_clause(self, clause, ctu_call):
        clause_fn = self.bld.fn(clause.fn_name(), clause.rule.cur_vars())

        clause_fn_body = chain(
            self.__gen_find_data(clause, ctu_call),
            self.__gen_find_rules(clause, ctu_call)
        )

        self.bld.fn_body_stmts(clause_fn, clause_fn_body)

    def __gen_find_data(self, clause, ctu_call):
        match_tp = ( Var("s"), Var("p"), Var("o") )
        fn_call = FnCall(self.bld.attr_ref('data', 'find'))
        
        yield from self.__gen_match_call(clause, match_tp, fn_call, ctu_call)

    def __gen_find_rules(self, clause, ctu_call):
        matches = self.__fn_idx.find(clause.tp)
            
        for match in matches:
            match_tp = match.rule.s.model.triple_at(0)
            fn_call = FnCall(self.bld.ref(match.name))
            
            yield from self.__gen_match_call(clause, match_tp, fn_call, ctu_call)
                
    def __gen_match_call(self, clause, match_tp, fn_call, ctu_call):
        fn_call.set_params(match_tp._vars(get_name=True), default=self.bld.cnst(None))

        if self.__unify(clause, match_tp, fn_call, ctu_call):
            return

        ctu_args = ctu_call.get_args()
        ctu_call_bld = self.bld.fn_call(ctu_call.ref, ctu_args)

        lmbda_params = match_tp._vars(get_name=True)
        lmbda_bld = self.bld.lmbda(lmbda_params, ctu_call_bld)

        fn_args = fn_call.get_args()
        fn_args.append(lmbda_bld)
        fn_call_bld = self.bld.fn_call(fn_call.ref, fn_args)
        
        if len(fn_call.conds) > 0:
            fn_call_bld = self.bld.iif(
                self.bld.conj(fn_call.conds), fn_call_bld)

        yield fn_call_bld

    def __unify(self, clause, match_tp, fn_call, ctu_call):
        for pos in range(3):
            clause_term = clause.tp[pos]
            has_runtime_val = clause.rule.has_runtime_val(clause_term)
            match_term = match_tp[pos]
            
            op = self.__unify_terms(clause_term, has_runtime_val, match_term)

            match (op.type):
                case UOpTypes.CMP:
                    match (op.ref):
                        case UOpRefs.DIRECT:
                            if clause_term != match_term:
                                return False
                        case UOpRefs.RUNTIME:
                            cmp1 = self.bld.comp(self.bld.ref(clause_term.name), 'is', self.bld.cnst(None))
                            cmp2 = self.bld.comp(self.bld.ref(clause_term.name), 'eq', self._val(match_term))
                            fn_call.conds.append(self.bld.disj([cmp1, cmp2]))    

                case UOpTypes.TO_MATCH:
                    match (op.ref):
                        case UOpRefs.DIRECT:
                            fn_call.set_arg(op.val2.name, self.bld._val(op.val1))
                        case UOpRefs.RUNTIME:
                            fn_call.set_arg(op.val2.name, self.bld.bld.ref(op.val1.name))

                case UOpTypes.FROM_MATCH:
                    match (op.ref):
                        case UOpRefs.DIRECT:
                            ctu_call.set_arg(op.val2.name, self.bld._val(op.val1))
                        case UOpRefs.RUNTIME:
                            ctu_call.set_arg(op.val2.name, self.bld.bld.ref(op.val1.name))
    
    def __unify_terms(self, clause_term, clause_runtime_val, match_term):
        if clause_term.is_concrete():
            if match_term.is_concrete():
                return UOp(UOpTypes.CMP, UOpRefs.DIRECT, clause_term, match_term)
            else:
                return UOp(UOpTypes.TO_MATCH, UOpRefs.DIRECT, clause_term, match_term)
        else:
            if match_term.is_concrete():
                if clause_runtime_val:
                    return UOp(UOpTypes.CMP, UOpRefs.RUNTIME, clause_term, match_term)
                else:
                    return UOp(UOpTypes.FROM_MATCH, UOpRefs.DIRECT, match_term, clause_term)
            else:
                if clause_runtime_val:
                    return UOp(UOpTypes.TO_MATCH, UOpRefs.RUNTIME, clause_term, match_term)
                else:
                    return UOp(UOpTypes.FROM_MATCH, UOpRefs.RUNTIME, match_term, clause_term)