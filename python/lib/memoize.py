import functools

# default memoize
class Memoize():
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.args_res = {}
        
    def memorize(self, args, res):
        self.args_res[args] = res
        
    def can_recall(self, args):
        return args in self.args_res
        
    def recall(self, args):
        return self.args_res[args]
    
    def __call__(self, *args):
        if not self.can_recall(args):
            res = self.func(*args)
            self.memorize(args, res)
        
        return self.recall(args)

# memoization for continuation passing
class MemoizeCtuPass(Memoize):
    
    def __init__(self, func, verbose=True, only_mod_flow=False):
        super().__init__(func)
        self.verbose = verbose
        # only modify the ctu call flow (testing)
        self.only_mod_flow = only_mod_flow
    
    def __call__(self, *args):
        pass_args = args[:-1] # all but last
        ctu_fn = args[-1] # last
        
        if self.verbose:
            print(self.func.__name__, "<--", pass_args, "(", "cache:", self.args_res, ")")
        if self.only_mod_flow or not self.can_recall(pass_args):
            res = []
            # add cb_args (= result) to res = all results
            # (cannot call ctu_fn for each indiv result; fib.n3 example)
            self.func(*pass_args, lambda *cb_args: res.append(cb_args))
            # get here when all ctu_fn calls are done
            if self.verbose:
                print(self.func.__name__, "-->", res)
            self.memorize(pass_args, res)
        else:
            res = self.recall(pass_args)
            if self.verbose:
                print(self.func.__name__, "-m->", res)
            
        for cb_args in res:
            ctu_fn(*cb_args)