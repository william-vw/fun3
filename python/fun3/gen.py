from ast import *
from ..n3.terms import *

class GenPython:
    
    # cur_vars
    
    def __init__(self):
        self.__builder = FnBuilder("rule")
    
    def gen_python(self, rules):
        self.__pred_idx = self.__build_pred_idx(rules)
        
        for (head, _, body) in rules:
            self.__gen_rule(head, body)
        
    def __gen_rule(self, head, body):
        head_vars = [ v for v in self.__vars_graph(head) ] # yes
        fn_vars = head_vars + [ 'model', 'state', 'ctu' ]
        
        fn = self.__builder.fn(fn_vars)
        # merge first clause fn into body here
        
        fns = []
        
        self.cur_vars = []
        for i, _ in enumerate(body.model.triples):
            fns.append(self.__gen_clause(head, body, i))
        
    def __gen_clause(self, head, body, index):
        clause = body[index]
        
        clause_fn = self.__builder.fn(self.cur_vars)
        
        # variables only in this clause
        own_vars = []
        
        spo = ['s', 'p', 'o']
        
        # ctu we need to call after searching for triples
        if index < len(body.triples) - 1:
            # e.g., cur_vars = [r, p, a]; clause = ?p address ?a
            # prior_vars = [r]; own_vars = ['s', 'o']
            
            # variables from prior clauses not in this clause
            prior_vars = self.cur_vars.copy()
            
            for i, r in enumerate(clause):
                if isinstance(r, Var):
                    if r.name in prior_vars:
                        prior_vars.remove(r.name)
                    own_vars.append(spo[i])
            
            # unique list of variables from prior & this clause
            self.cur_vars = list(dict.fromkeys(self.cur_vars + own_vars)) # unique but keep ordering
            
            # call the next clause fn
            next_fn = FnSign(self.__builder.next_fn_name(), self.cur_vars)
            

        else:
            # e.g., cur_vars = [r, p, a]; clause = ?p address ?a; head = ?p a Person
            # prior_vars = [], own_vars = ['s']
            
            # only vars that are needed by the original ctu
            prior_vars = self.__vars_graph(head)
            
            # at the last clause, so call the original ctu
            next_fn = FnSign('ctu', prior_vars)
            
            for i, r in enumerate(clause):
                if isinstance(r, Var) and r.name in prior_vars:
                    prior_vars.remove(r.name)
                    own_vars.append(spo[i])
        
        # s, p, o from clause will be search terms
        #   if variable, refer to the function argument (it could have been provided)
        #   else, use resource from clause
        search_terms = [ self.__builder.ref(r.name) if isinstance(r, Var) else self.__builder.cnst(str(r)) for r in clause ]
        
        # store.find will call a lambda
        # this lambda will itself call the ctu from before
        
        # first, build ctu call
        # refer to provided arguments for prior_vars
        ctu_args = [ self.__builder.ref(v) for v in prior_vars ]
        # refer to parts from result triple for own_vars
        ctu_args += [ self.__builder.attr_ref('t', v) for v in own_vars ]
        # additional arguments
        ctu_args += [ self.__builder.ref(v) for v in [ 'model', 'state', 'ctu' ] ]
        # create ctu call
        ctu_call = self.__builder.fn_call(self.__builder.ref(next_fn.name), ctu_args)
        
        # then, create lambda with ctu call
        lmbda = self.__builder.lmbda([ 't', 'state' ], ctu_call)
        
        # finally, create store.find call
        store_call = self.__builder.fn_call(self.__builder.attr_ref('store', 'find'), 
                                            search_terms + self.__builder.ref('state') + lmbda)
        
        # add store call to the function's body
        self.__builder.fn_body_stmt(clause_fn, self.__builder.to_stmt(store_call))
        
        return clause_fn
        
    def __build_pred_idx(self, rules):
        pred_idx = {}
        for r in rules:
            if r.p == "<=":
                for t in r.s:
                    pred_idx[t.p] = r  
        return pred_idx

    def __vars_graph(self, graph):
        for t in graph.model.triples:
            self.__vars_triple(t)

    def __vars_triple(self, t):
        for r in t:
            if isinstance(r, Var):
                yield r

class FnBuilder:
    
    # fn_prefix
    # fn_cnt
    
    def __init__(self, fn_prefix):
        self.__fn_prefix = fn_prefix
        self.__fn_cnt = 0
    
    def fn(self, params=[]):
        args = [ arg(arg=p) for p in params ]
        
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
        return Constant(value=value)
    
    def attr_ref(self, var, attr):
        return Attribute(value=self.ref(var), attr=attr, ctx=Load())
        
    def fn_call(self, fn, args):
        return Call(func=fn, args=args, keywords=[])
    
    def fn_call_arg(self, fn_call, arg):
        fn_call.args.append(arg)
    
    def lmbda(self, params, expr):
        args = [ arg(arg=p) for p in params ]
        
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
        self.__fn_name(self.__fn_cnt + 1)
    
    def __fn_name(self, cnt):
        return f"{self.__fn_prefix}_{cnt}"


class FnSign:
    
    def __init__(self, name, kw_params):
        self.name = name
        self.kw_params = kw_params