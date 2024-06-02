from ast import dump, unparse

from n3.parse import parse_n3
from n3.fun.gen import gen_py

class State : 
    def __init__(self, stop):
        self.stop = stop

def result_fn(p, state):
    print(f"solution: {p}")
    # state.stop = True


def fun3():
    # (?x, a, Cool) :- (?x, name, "will")
    # rules =  """@prefix : <http://example.org/> . 
# { ?x a :Cool } <= { ?x :name \"will\" } . """
    
    # (?p, type, Canadian) :-
    #   (?p, type, Person), (?p, address, ?a), (?a, country, "CA") .
    # (?p, type, Person) :-
    #   (?p, ability, think) .
    
    rules =  """@prefix : <http://example.org/> . 
{ ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a ?c "CA" } . 
{ ?p a :Person } <= { ?p :ability :think } .
"""
    
    data = """@prefix : <http://example.org/> . 
:will a :Person ; :address :addr1 . :addr1 :country "CA" .
:ed :ability :think ; :address :addr1 .
"""
    
    # parse
    
    result = parse_n3(rules)
    # print(result.model)
    print(result.rules)
    
    model = parse_n3(data).model
    print(model)
    
    print()
    
    # generate
    
    mod = gen_py(result.rules)
    # print(dump(mod, indent=4))
    print(unparse_with_lineno(mod))
    
    print()
    
    # # compile
    
    # rule_fn = compile_py(mod)
    # print(rule_fn)
    
    # print()
    
    # # test
    
    # state = State(False)
    
    # rule_fn(None, model, state, result_fn)
    
    
def unparse_with_lineno(ast):
    code = unparse(ast)
    return "\n".join([ f"{i+1}. {line}" for i, line in enumerate(code.split("\n")) ])

def compile_py(mod):    
    mod_code = compile(mod, "<fun3>", "exec")
    
    new_refs = {}
    exec(mod_code, globals(), new_refs)
    # print(new_refs)
    
    for name, code in new_refs.items():
        globals()[name] = code

    return new_refs['rule_0']


if __name__ == "__main__":
    fun3()