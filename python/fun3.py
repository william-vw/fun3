from ast import dump, unparse

from n3.parse import parse_n3
from n3.fun.gen import gen_py
from n3.terms import Iri

class State : 
    def __init__(self, stop):
        self.stop = stop

def result_fn(*args):
    print(f"solution: { [ a for a in args[:-1] ] }")
    # state.stop = True


def fun3():
#     rules =  """@prefix : <http://example.org/> . 
# # -
# # { ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a :country "CA" } . 
# # { ?pe a :Person } <= { ?pe :ability :think } .
# # { ?pe a :Belgian } <= { ?pe :ability :drink } .
# # -
# # { ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a :country "CA" } . 
# # { ?pe a ?ty } <= { ?pe :describedAs ?ty } .
# # -
# # { ?p a :Canadian } <= { ?p a ?t . ?p :address ?a . ?a :country "CA" } . 
# # { ?pe a ?ty } <= { ?pe :describedAs ?ty } .
# # -
# { ?p a :Canadian } <= { ?p a ?t . ?p :address ?a . ?a :country "CA" } . 
#  { ?pe a :Person } <= { ?pe :ability :think } .
#  { ?p a ?t } <= { ?p :name "Socrates" } .
# """
#     data = """@prefix : <http://example.org/> . 
# :will a :Person ; :address :addr1 . :addr1 :country "CA" .
# :ed :ability :think ; :address :addr1 ; :describedAs :Person .
# :el :ability :drink ; :address :addr1 ; :describedAs :Belgian .
# :dor :ability :think ; :address :addr2 ; :describedAs :German .
# :soc :name "Socrates" ; :address :addr1 .
# """

    rules =  """@prefix log: <http://www.w3.org/2000/10/swap/log#> .
@prefix : <http://example.org/> . 
{ ?desc :ancestor ?anc } <= { ?desc :parent ?parent . ?parent :ancestor ?anc } .
{ ?desc :ancestor ?desc } <= true .
"""
    data = """@prefix : <http://example.org/> . 
:c :parent :b . :b :parent :a .
"""
    
    # parse
    
    result = parse_n3(rules)
    # print(result.model)
    print("rules:\n", result.rules)
    
    data = parse_n3(data).model
    print("model:\n", data)
    
    print()
    
    # generate
    
    mod = gen_py(result.rules)
    # print(dump(mod, indent=4))
    # print(unparse_with_lineno(mod))
    print(unparse(mod))
    
    print()
    
    # compile
    
    rule_fn = compile_py(mod)
    # print(rule_fn)
    
    print()
    
    # test
    
    state = State(False)
    
    print("run -")
    rule_fn(None, None, data, state, result_fn)
    
    
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