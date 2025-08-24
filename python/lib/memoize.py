import functools

class Memoize():
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.args_res = {}
        
    def __call__(self, *args):
        if args not in self.args_res:
            self.args_res[args] = self.func(*args)
        
        return self.args_res[args]

class MemoizeCtuPass():
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.args_res = {}
    
    def memoize(self, args, res):
        self.args_res[args] = res
    
    def __call__(self, *args):
        pass_args = args[:-1]
        ctu_fn = args[-1]
        
        if pass_args not in self.args_res:            
            # cannot use assignment expressions when indexing dictionary
            self.func(*pass_args, lambda *cb_args: self.memoize(pass_args, cb_args))
            
        res = self.args_res[pass_args]
        ctu_fn(*res)