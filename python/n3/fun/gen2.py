from enum import Enum
from collections import Counter
from multidict import MultiDict
from n3.fun.py_build import PyBuilder
from n3.terms import Var, term_types, Triple
from n3.ns import n3Log, swapNs
from itertools import chain
from ast import dump, unparse

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

    def set_avail_vars(self, vars):
        self.avail_vars = vars

    @staticmethod
    def unique_vars(prior_vars, new_vars):
        return list(dict.fromkeys(prior_vars + new_vars)) 

    def update_new_vars(self):
        self.avail_vars = self.new_vars

    def has_runtime_val(self, r):
        return r.name in self.avail_vars if not r.is_concrete() else False
        

class Clause:
    
    def __init__(self, rule, no, tp):
        self.rule = rule
        self.no = no
        self.tp = tp
        
        self.fn_name = RuleFn.fn_name(self.rule.no, self.no)
        
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
        if tp.p.idx_val() in self.idx:
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
    
    def __init__(self):
        self.fn_idx = FnIndex()
    
    def process(self, rule_no, rule_triple):        
        entry = FnEntry(rule_triple, RuleFn(rule_no, 0))
        
        t = rule_triple.s.model.triple_at(0) # only 1 triple
        self.fn_idx.add(t.p, entry)

    def get_index(self):
        return self.fn_idx


class RuleProcessor_UniqueVars:
    
    def __init__(self):
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
        
    def __str__(self):
        return f"{self.type}.{self.ref}: {self.val1} <> {self.val2}"
    
    
class ConditionalStmt:
    
    def __init__(self, conds = None):
        self.conds = conds if conds is not None else []
    
    
class FnCall(ConditionalStmt):
    
    def __init__(self, ref, params=None, args=None):
        super().__init__()
        
        self.ref = ref        
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
        return list(self.args.values())

    
class GenPython:

    def __init__(self):
        self.bld = PyBuilder()
                
        self.__rule_buildFnIdx = RuleProcessor_BuildFnIndex()
        self.__rule_renameVars = RuleProcessor_UniqueVars()
        
        self.names = {
            'final_ctu': "final_ctu"
        }

    def gen_python(self, rules):
        self.__process_rules(rules)
        
        return self.__gen_rule_mod(rules)

    def __gen_rule_mod(self, rules):
        self.code = [self.__gen_imports()]
        
        for i, (head, _, body) in enumerate(rules):
            rule = Rule(i, head, body)
            self.__gen_rule(rule)

        return self.bld.module(self.code)

    def __gen_imports(self):
        return self.bld.imports('n3.terms', ['Iri', 'Var', 'Literal', 'Collection', 'term_types'])
        
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
            if len(rule.s.model) != 1:
                print(f"warning: cannot use rule, length of head > 1 ({rule})")
                del rules[rule_no]; continue
            # only top-down rules
            if rule.p.iri == n3Log['implies']:
                print(f"warning: cannot use bottom-up rule ({rule})")
                del rules[rule_no]; continue

            self.__rule_renameVars.process(rule_no, rule)
            self.__rule_buildFnIdx.process(rule_no, rule)
        
        self.__fn_idx = self.__rule_buildFnIdx.get_index()
        # self.__fn_idx.print()
    
    def __gen_rule(self, rule):
        head_triple = rule.head.model.triple_at(0)
        rule.set_avail_vars(head_triple._vars(get_name=True))
        
        for no, tp in enumerate(rule.body.model.triples()):
            clause = Clause(rule, no, tp)
            new_avail_vars = Rule.unique_vars(rule.avail_vars, tp._vars(get_name=True))

            if no == len(rule.body.model)-1:
                ctu_call = self.__get_ctu_call(self.names['final_ctu'], head_triple._vars(get_name=True), final=True)
            else:
                ctu_call = self.__get_ctu_call(clause.next_fn_name(), new_avail_vars)
            self.__gen_clause(clause, ctu_call)

            rule.set_avail_vars(new_avail_vars)

    def __gen_clause(self, clause, ctu_call):
        clause_fn_def = self.bld.fn(clause.fn_name, self.__get_fn_params(clause.rule.avail_vars))

        clause_fn_body = chain(
            self.__gen_find_data(clause, ctu_call),
            self.__gen_find_rules(clause, ctu_call)
        )

        self.bld.fn_body_stmts(clause_fn_def, clause_fn_body)
        # print(unparse(clause_fn_def))
        
        self.code.append(clause_fn_def)

    def __gen_find_data(self, clause, ctu_call):
        match_tp = Triple(Var("s"), Var("p"), Var("o"))
        fn_call = FnCall(self.bld.attr_ref('data', 'find'))
        
        yield from self.__gen_match_call(clause, match_tp, fn_call, ctu_call)

    def __gen_find_rules(self, clause, ctu_call):
        matches = self.__fn_idx.find(clause.tp)
            
        for match in matches:
            match_tp = match.rule.s.model.triple_at(0)
            fn_call = FnCall(self.bld.ref(match.rule_fn.name))
            
            yield from self.__gen_match_call(clause, match_tp, fn_call, ctu_call)
                
    def __gen_match_call(self, clause, match_tp, fn_call, ctu_call):
        fn_call.set_params(match_tp._vars(get_name=True), default=self.bld.cnst(None))

        if not self.__unify(clause, match_tp, fn_call, ctu_call):
            return

        ctu_args = ctu_call.get_args()
        ctu_call_bld = self.bld.fn_call(ctu_call.ref, ctu_args)

        lmbda_params = match_tp._vars(get_name=True)
        lmbda_bld = self.bld.lmbda(lmbda_params, ctu_call_bld)

        fn_args = fn_call.get_args()
        fn_args.append(lmbda_bld)
        fn_call_bld = self.bld.stmt(self.bld.fn_call(fn_call.ref, fn_args))
        
        if len(fn_call.conds) > 0:
            fn_call_bld = self.bld.iif(
                self.bld.conj(fn_call.conds), fn_call_bld)

        yield fn_call_bld

    def __unify(self, clause, match_tp, fn_call, ctu_call):
        for pos in range(3):
            clause_term = clause.tp[pos]
            has_runtime_val = clause.rule.has_runtime_val(clause_term)
            match_term = match_tp[pos]
            
            for op in self.__unify_terms(clause_term, has_runtime_val, match_term):
                # print(op)
                match (op.type):
                    case UOpTypes.CMP:
                        match (op.ref):
                            case UOpRefs.DIRECT:
                                if clause_term != match_term:
                                    return False
                            case UOpRefs.RUNTIME:
                                cmp1 = self.bld.comp(self.bld.ref(clause_term.name), 'is', self.bld.cnst(None))
                                cmp2 = self.bld.comp(self.bld.ref(clause_term.name), 'eq', self.val(match_term))
                                fn_call.conds.append(self.bld.disj([cmp1, cmp2]))    

                    case UOpTypes.TO_MATCH:
                        match (op.ref):
                            case UOpRefs.DIRECT:
                                fn_call.set_arg(op.val2.name, self.bld.val(op.val1))
                            case UOpRefs.RUNTIME:
                                fn_call.set_arg(op.val2.name, self.bld.var_ref(op.val1))

                    case UOpTypes.FROM_MATCH:
                        match (op.ref):
                            case UOpRefs.DIRECT:
                                ctu_call.set_arg(op.val2.name, self.bld.val(op.val1))
                            case UOpRefs.RUNTIME:
                                ctu_call.set_arg(op.val2.name, self.bld.var_ref(op.val1))
                            
        return True
    
    def __unify_terms(self, clause_term, clause_runtime_val, match_term):
        if clause_term.is_concrete():
            if match_term.is_concrete():
                yield UOp(UOpTypes.CMP, UOpRefs.DIRECT, clause_term, match_term)
            else:
                yield UOp(UOpTypes.TO_MATCH, UOpRefs.DIRECT, clause_term, match_term)
        else:
            if match_term.is_concrete():
                if clause_runtime_val:
                    yield UOp(UOpTypes.CMP, UOpRefs.RUNTIME, clause_term, match_term)
                else:
                    yield UOp(UOpTypes.FROM_MATCH, UOpRefs.DIRECT, match_term, clause_term)
            else:
                # possible that runtime var is None (when called from other rule, or initial call)
                # so also unify by getting result from match
                if clause_runtime_val:
                    yield UOp(UOpTypes.TO_MATCH, UOpRefs.RUNTIME, clause_term, match_term)

                yield UOp(UOpTypes.FROM_MATCH, UOpRefs.RUNTIME, match_term, clause_term)
                
    
    def __get_ctu_call(self, name, params, final=False):
        params = self.__get_fn_params(params, final)
        
        return FnCall(self.bld.ref(name), 
            params=params, 
            args=[self.bld.ref(p) for p in params])
    
    def __get_fn_params(self, params, final=False):
        return params + [ self.names['final_ctu'] ] if not final else params
            
