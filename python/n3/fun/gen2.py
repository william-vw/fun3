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


class __UOps(Enum):
	CMP_DIRECT = 1
	CMP_RUNTIME = 2
	PASS_ARG = 3
	ASSN_DIRECT = 4
	ASSN_RUNTIME = 5


class __UOp:
    def __init__(self, op, arg1, arg2):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2


class __Rule:
    
    def __init__(self, no, head, body):
        self.no = no
        self.head = head
        self.body = body
        self.cur_vars = []

    def add_cur_vars(self, vars):
        self.cur_vars = list(dict.fromkeys(self.cur_vars + vars)) 

    def clause_runtime_val(self, var):
        return var in self.cur_vars


class __Clause:
    
    def __init__(self, rule, no, tp):
        self.rule = rule
        self.no = no
        self.tp = tp
        
        
class __RuleFn:
    
    __fn_prefix = "rule"
    
    def __init__(self, rule_no, clause_no):        
        self.name = self.__gen_fn_name(rule_no, clause_no)

    def __gen_fn_name(self, rule_no, clause_no):
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
        


class __FnIndex:
    
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


class __FnEntry:
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
    

class __RuleProcessor_BuildFnIndex:
    
    def __init__(self, gen_python):
        self.fn_idx = __FnIndex()
        gen_python.__fn_idx = self.fn_idx
    
    def process(self, rule_no, rule_triple):        
        entry = __FnEntry(rule_triple, __RuleFn(rule_no, 0))
        # iterate over all triples in head (just one really)
        for t in rule_triple.s.model.triples():
            self.fn_idx.add(t.p, entry)


class __RuleProcessor_UniqueVars:
    
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
        unique_vars = { v:f"{v}_{i}" for v,i in zip(unique_vars, range(self.var_cnt, len(unique_vars)+self.var_cnt)) }
        
        # rename vars in head & body
        head._rename_recur_vars(unique_vars)
        if body.type() == term_types.GRAPH:
            body._rename_recur_vars(unique_vars)
        
        # update var count
        self.var_cnt += len(unique_vars)
    
    
class GenPython:

    def __init__(self):
        self.bld = PyBuilder()
        
        self.__rule_buildFnIdx = __RuleProcessor_BuildFnIndex(self)
        self.__rule_renameVars = __RuleProcessor_UniqueVars(self)

    def gen_python(self, rules):
        self.__process_rules(rules)
        
        for i, (head, _, body) in enumerate(rules):
            rule = __Rule(i, head, body)
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
        
        for i, tp in enumerate(rule.body.model.triples()):
            clause = __Clause(rule, i, tp)
            self.__gen_clause(clause)
            
            rule.add_cur_vars(tp._vars())
            
    def __gen_clause(self, clause):
        self.__gen_find_data(clause)
        self.__gen_find_rule(clause)
    
    def __gen_find_data(self, clause):
        match_tp = ( Var("s"), Var("p"), Var("o") )
        self.__unify(clause, match_tp)
    
    def __gen_find_rule(self, clause):
        # find matching rules
        matches = self.__fn_idx.find(clause.tp)
        
        for match in matches:
            match_tp = match.rule.s.model.triples()[0]
            self.__unify(clause, match_tp)
    
    def __unify(self, clause, match_tp):
        for pos in range(3):
            clause_term = clause.tp[pos]
            clause_runtime_val = clause.rule.has_runtime_val(clause_term)
            match_term = match_tp[pos]
            
            op = self.__unify_terms(clause_term, clause_runtime_val, match_term)
            print(op)
    
    def __unify_terms(self, clause_term, clause_runtime_val, match_term):
        if clause_term.is_concrete():
            if match_term.is_concrete():
                return __UOp(__UOps.CMP_DIRECT, clause_term, match_term)
            else:
                return __UOp(__UOps.PASS_ARG, clause_term, match_term)
        else:
            if match_term.is_concrete():
                if clause_runtime_val:
                    return __UOp(__UOps.CMP_RUNTIME, clause_term, match_term)
                else:
                    return __UOp(__UOps.ASSN_DIRECT, match_term, clause_term)
            else:
                if clause_runtime_val:
                    return __UOp(__UOps.PASS_ARG, clause_term, match_term)
                else:
                    return __UOp(__UOps.ASSN_RUNTIME, match_term, clause_term)