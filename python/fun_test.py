from ast import dump, unparse

from n3.parse import parse_n3
from n3.fun.gen import gen_py

class State : 
    def __init__(self, stop):
        self.stop = stop

def result_fn(*args):
    print(f"solution: { [ a for a in args[:-1] ] }")
    # state.stop = True


def fun3():
# # ex 1
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
#     call = lambda data, state, rule_fn: rule_fn(None, data, state, result_fn)


# # ex 2
#     rules =  """@prefix log: <http://www.w3.org/2000/10/swap/log#> .
# @prefix : <http://example.org/> . 
# { ?desc :ancestor ?anc } <= { ?desc :parent ?parent . ?parent :ancestor ?anc } .
# { ?desc :ancestor ?desc } <= true .
# """
#     data = """@prefix : <http://example.org/> . 
# :c :parent :b . :b :parent :a .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, data, state, result_fn)

# # ex 3
#     rules =  """@prefix : <http://example.org/> . 
# # { ?z :aliasNames ( ?xn ?yn ) } <= { ?z :alias ( ?x ?y ) . ?x :name ?xn . ?y :name ?yn } .
# { ?z :aliasNames ( ?xn ?yn ) } <= { ( ?z ) :alias ( ( ?x ) ( ?y ?q ) ) . ?x :name ?xn . ?y :name ?yn } .
# """
#     data = """@prefix : <http://example.org/> . 
# # :wil :alias ( :edw :elb ) . 
# ( :wil ) :alias ( ( :edw ) ( :elb :wil ) ) .  # ( ( :edw ) :elb )
# :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, None, data, state, result_fn)

# # ex 4
#     rules =  """@prefix : <http://example.org/> . 
# { ?z :aliasNames ( ?xn ) } <= { ?z :aliasPair ( :edw ?x ) . ?x :name ?xn } .
# # { ?z :aliasPair ( :edw :elb ) } <= { ?z :alias ( :edw :elb ) } .
# # { ?z :aliasPair ( :edw ?a ) } <= { ?z :alias ( :edw ?a ) } .
# { ?z :aliasPair ( ?a ?b ) } <= { ?z :alias ( ?a ?b ) } .
# """
#     data = """@prefix : <http://example.org/> . 
# :wil :alias ( :edw :elb ) . 
# :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, data, state, result_fn)

# # ex 5
#     rules =  """@prefix : <http://example.org/> . 
# { ?z :aliasNames ?a } <= { ?z :aliasPair ?a } .
# { ?z :aliasPair ( ?x ?y ) } <= { ?z :alias ( ?x ?y ) } .
# """
#     data = """@prefix : <http://example.org/> . 
# :wil :alias ( :edw :elb ) . 
# :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, data, state, result_fn)

# # ex 6
#     rules =  """@prefix : <http://example.org/> . 
# { ?z :aliasNames ( ?a ?x ) } <= { ?z :aliasPair ( ?a ?x ) } .
# { ?z :aliasPair ( ( ?x ?y ) ?k ) } <= { ?z :alias ( ?x ?y ) } .
# """
#     data = """@prefix : <http://example.org/> . 
# :wil :alias ( :edw :elb ) . 
# :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, None, data, state, result_fn)

# # ex 7
#     rules =  """@prefix : <http://example.org/> . 
# { ?z :aliases ( ?x ?y ) } <= { ?z :aliasPair ( ( ?x ?y ) ?k ) . ?x :name ?xn . ?y :name ?yn } .
# { ?z :aliasPair ( ?a ?k ) } <= { ?z :alias :k , :l } .
# """
#     data = """@prefix : <http://example.org/> . 
# :wil :alias ( :edw :elb ) . 
# :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, None, data, state, result_fn)

# TODO
# . extra lambda params for 2nd, 3rd.. occurrence of duplicate var
# . separate function for unifying these vars
# . avoid potential name conflicts
#   update self.__all_rule_vars/params with renamed lambda params, unify-head's fn params

# # ex 8
#     rules =  """@prefix : <http://example.org/> . 
# # { ?x :lonerName ?xn } <= { ?x :onlyFriend ?x . ?x :name ?xn } .
# # { ?x :blah ( ?y ?y ) } <= { ?x :onlyFriend ?x } .
# """
#     data = """@prefix : <http://example.org/> . 
# :edw :onlyFriend :wil .
# :wil :name "wil" . :edw :name "edw" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None,  data, state, result_fn)


    # parse
    
    result = parse_n3(rules)
    print("rules:\n", result.rules)
    
    data = parse_n3(data).data
    print("data:\n", data)
    
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
    call(data, state, rule_fn)

    
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