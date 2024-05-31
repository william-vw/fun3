from ast import *
from types import *

from util import *

def build_fn():
    rule_fn = FunctionDef(
        name="r1",
        args=arguments(
            args=[ ], 
            posonlyargs=[], vararg=None, kwarg=None, defaults=[], kwonlyargs=[], kw_defaults=[]
        ),
        body=[],
        decorator_list=[]
    )
    
    rule_fn.args.args.extend([arg(arg='p'), arg(arg='store'), arg(arg='state'), arg(arg='ctu')])
    rule_fn.body.append(Expr(
        Call(
            func=Attribute(value=Name(id='store', ctx=Load()), attr='find', ctx=Load()),
            args=[
                Name(id='p', ctx=Load()), Constant(value='ability'), Constant(value='think'), Name(id='state', ctx=Load()),
                Lambda(
                    args=arguments(
                        args=[ arg(arg='t'), arg(arg='state') ],
                        posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[]
                    ),
                    body=Call(
                        func=Name(id='ctu', ctx=Load()),
                        args=[ Attribute(value=Name(id='t', ctx=Load()), attr='s', ctx=Load()), Name(id='state', ctx=Load()) ],
                        keywords=[]
                    )
                )
            ],
            keywords=[]
        )
    ))
    
    rule_mod = Module(body=[rule_fn], type_ignores=[])
    fix_missing_locations(rule_mod)
    print(dump(rule_mod, indent=4))
    
    mod_code = compile(rule_mod, "<?p, type, Person>", "exec")
    fn_code = [c for c in mod_code.co_consts if isinstance(c, CodeType)][0]
    
    return FunctionType(fn_code, {})

def result(p, state):
    print(f"solution: {p}")
    # state.stop = True

def main():
    # (?p, type, Person) :-
    #   (?p, ability, think) .

    # def r1(p, store, state, ctu):
    #     store.find(p, "ability", "think", state, lambda t, state: ctu(t.s, state) )
    
    state = State(False)
    
    # # - ex1
    
    store = Store([ 
        Triple( s="ed", p="type", o="Person" ),
        Triple( s="will", p="ability", o="think" ),
        Triple( s="soc", p="name", o="\"Socrates\"" ),
    
        Triple( s="ed", p="address", o="addr1" ),
        Triple( s="will", p="address", o="addr2" ),
        Triple( s="soc", p="address", o="addr3" ),
    
        Triple( s="addr1", p="country", o="\"BE\"" ),
        Triple( s="addr2", p="country", o="\"CA\"" ),
        Triple( s="addr3", p="country", o="\"CA\"" )
    ])
    
    fn = build_fn()
    
    fn(None, store, state, result)
    
if __name__ == "__main__":
    main()