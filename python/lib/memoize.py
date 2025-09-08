import functools

# default memoize
class Memoize():
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.args_res = {}
        
    def remember(self, args, res):
        self.args_res[args] = res
        
    def __call__(self, *args):
        if args not in self.args_res:
            res = self.func(*args)
            self.remember(args, res)
        
        return self.args_res[args]

# memoization for continuation passing
class MemoizeCtuPass(Memoize):
    
    def __init__(self, func):
        super().__init__(func)
    
    def wrap_ctu_call(self, all_cb_args, cb_args, ctu_fn):
        print(self.func.__name__, "->", cb_args)
        all_cb_args.append(cb_args)
        ctu_fn(*cb_args)
    
    def __call__(self, *args):
        pass_args = args[:-1] # all but last
        ctu_fn = args[-1] # last
        
        print(self.func.__name__, "<--", pass_args, self.args_res)
        if pass_args not in self.args_res:
            all_cb_args = []
            # wrap ctu call; cb_args is result of func
            # add cb_args to all_cb_args; these represent all results
            # call ctu_fn for each individual cb_args
            self.func(*pass_args, lambda *cb_args: self.wrap_ctu_call(all_cb_args, cb_args, ctu_fn))
            # get here when all ctu_fn calls are done
            self.remember(pass_args, all_cb_args)
        else:
            result = self.args_res[pass_args]
            print(self.func.__name__, "-m->", result)
            for cb_args in result:
                ctu_fn(*cb_args)