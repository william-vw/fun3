from ast import dump, unparse
from collections import Counter
from multidict import MultiDict

from n3.parse import parse_n3
from n3.fun.gen2 import gen_py
from n3.terms import Triple

def test():
    rule = """@prefix : <http://example.org/> .
    { ?p a :Canadian } <= { ?x :d ?x . ?y :e ( ?x ?x ?y ?y ) } ."""
    
    result = parse_n3(rule)
    # print("rules:\n", result.rules)
    
    rule = result.rules[0]
    body = rule.o
    clause = body.model.triples()[1]
    
    
def get_spo_pos(pos):
    return pos[0][0]

def get_spo_varname(pos, var):
    spo_ch = Triple.spo[get_spo_pos(pos)]
    return f"{var}_{spo_ch}" if len(pos) == 1 else f"coll_{spo_ch}"


class State : 
    def __init__(self, stop):
        self.stop = stop

def result_fn(*args):
    print(f"solution: { [ a for a in args[:-1] ] }")
    # state.stop = True


def fun3():
# - test 1
# (straightforward, non-recursive rules)

# (1) only query data
    rules =  """@prefix : <http://example.org/> . 
{ ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a :country "CA" } . 
"""

# # (2) call other rules (both terms concrete)
#     rules =  """@prefix : <http://example.org/> . 
# { ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a :country "CA" } . 
# { ?pe a :Person } <= { ?pe :ability :think } .
# { ?pe a :Belgian } <= { ?pe :ability :drink } .
# """

# # (3) call other rules (clause term concrete, match term var)
#     rules =  """@prefix : <http://example.org/> . 
# { ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a :country "CA" } . 
# { ?pe a ?ty } <= { ?pe :describedAs ?ty } .
# """

# # (4) call other rules (clause term var, match term concrete)
# # ("label"; not doing recursion yet)
#     rules =  """@prefix : <http://example.org/> . 
# { ?p :label :Canadian } <= { ?p a ?t . ?p :address ?a . ?a :country "CA" } . 
# { ?pe a :Person } <= { ?pe :ability :think } .
# """

# # (5) same level of specificity; all clauses have 2 variables
# # ("label"; not doing recursion yet)
#     rules =  """@prefix : <http://example.org/> . 
# { ?p :label :Canadian } <= { ?p a ?t . ?p :address ?a . ?a :country "CA" } . 
# { ?p a ?t } <= { ?p :describedAs ?t } .
# { ?p a ?t } <= { ?p :name "Socrates" } . # t not used in body
# """

    data = """@prefix : <http://example.org/> . 
:will a :Person ; :address :addr1 . :addr1 :country "CA" .
:ed :ability :think ; :address :addr1 ; :describedAs :Person .
:el :ability :drink ; :address :addr1 ; :describedAs :Belgian .
:dor :ability :think ; :address :addr2 ; :describedAs :German .
:soc :name "Socrates" ; :address :addr1 .
"""

    call = lambda data, state, rule_fn: rule_fn(None, data, state, result_fn)

# # - test 2
# # (simple example of recursive rules)

#     rules =  """@prefix log: <http://www.w3.org/2000/10/swap/log#> .
# @prefix : <http://example.org/> . 
# { ?desc :ancestor ?anc } <= { ?desc :parent ?parent . ?parent :ancestor ?anc } .
# { ?desc :ancestor ?desc } <= true .
# """
#     data = """@prefix : <http://example.org/> . 
# :c :parent :b . :b :parent :a .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, data, state, result_fn)

# # - test 3
# # (list unification (nested); only querying data)

#     rules =  """@prefix : <http://example.org/> . 
# { ?z :aliasNames ( ?xn ?yn ) } <= { ( ?z ) :alias ( ( ?x ) ( ?y ?q ) ) . ?x :name ?xn . ?y :name ?yn } .
# """
#     data = """@prefix : <http://example.org/> . 
# ( :wil ) :alias ( ( :edw ) ( :elb :wil ) ) .  # ( ( :edw ) :elb )
# :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, None, data, state, result_fn)

# # - test 4
# # (list unification; refer to other rules; calling, called rules have similar lists)

#     rules =  """@prefix : <http://example.org/> . 
# # (partially concrete list in calling rule; compile-time check on :edw)
# { ?z :aliasNames ( ?xn ) } <= { ?z :aliasPair ( :edw ?x ) . ?x :name ?xn } .
# { ?z :aliasPair ( :edw :elb ) } <= { ?z :alias ( :edw :elb ) } .
# # { ?z :aliasPair ( :edw ?a ) } <= { ?z :alias ( :edw ?a ) } .
# # { ?z :aliasPair ( :edu ?a ) } <= { ?z :alias ( :edw ?a ) } .
# """
#     data = """@prefix : <http://example.org/> . 
# :wil :alias ( :edw :elb ) . 
# :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, data, state, result_fn)

# # - test 5
# # (list unification; called rule has list where calling rule has var)
#     rules =  """@prefix : <http://example.org/> . 
# { ?z :aliasNames ?a } <= { ?z :aliasPair ?a } .
# { ?z :aliasPair ( ?x ?y ) } <= { ?z :alias ( ?x ?y ) } .
# """
#     data = """@prefix : <http://example.org/> . 
# :wil :alias ( :edw :elb ) . 
# :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, data, state, result_fn)

# # - test 6
# # (list unification (nested); called rule has sublist where calling rule has var)
#     rules =  """@prefix : <http://example.org/> . 
# { ?z :aliasNames ( ?a ?x ) } <= { ?z :aliasPair ( ?a ?x ) } .
# { ?z :aliasPair ( ( ?x ?y ) ?k ) } <= { ?z :alias ( ?x ?y ) } .
# """
#     data = """@prefix : <http://example.org/> . 
# :wil :alias ( :edw :elb ) . 
# :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, None, data, state, result_fn)

# # - test 7
# # (list unification (nested); calling rule has sublist where called rule has var)
#     rules =  """@prefix : <http://example.org/> . 
# { ?z :aliases ( ?x ?y ) } <= { ?z :aliasPair ( ( ?x ?y ) ?k ) . ?x :name ?xn . ?y :name ?yn } .
# { ?z :aliasPair ( ?a ?k ) } <= { ?z :alias ( ?a ?k ) } .
# """
#     data = """@prefix : <http://example.org/> . 
# :wil :alias ( ( :wil :edw ) :elb ) . 
# :wil :name "wil" . :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, None, data, state, result_fn)

# # - test 8
# # (co-referencing; simple triple)
#     rules =  """@prefix : <http://example.org/> . 
# { ?x :lonerName ?xn } <= { ?x :onlyFriend ?x . ?x :name ?xn } .
# { ?x :onlyFriend ?y } <= { ?x :blah ?y } .
# """
#     data = """@prefix : <http://example.org/> . 
# :edw :onlyFriend :edw .
# :elb :blah :elb .
# :edw :name "edw" . :elb :name "elb" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None,  data, state, result_fn)

# # - test 9
# # (co-referencing; lists)
#     rules =  """@prefix : <http://example.org/> . 
# { ?z :aliases ( ?xn ) } <= { ?z :aliasPair ( ?x ?x ) . ?x :name ?xn } .
# # { ?z :aliasPair ( ?a ?k ) } <= { ?z :alias ( ?a ?k ) } .
# """
#     data = """@prefix : <http://example.org/> . 
# :wil :aliasPair ( :edw :edw ) . 
# :wil :name "wil" . :edw :name "edward" . :elb :name "elbert" .
# """
#     call = lambda data, state, rule_fn: rule_fn(None, None, data, state, result_fn)


    # parse
    
    result = parse_n3(rules)
    # print("rules:\n", result.rules)
    
    data = parse_n3(data).data
    # print("data:\n", data)
    
    print()
    
    # generate
    
    mod = gen_py(result.rules)
    print()
    # print(dump(mod, indent=4))
    # print(unparse_with_lineno(mod))
    print(unparse(mod))
    
    print()
    
    # compile
    
    rule_fn = compile_py(mod)
    print(rule_fn)
    
    print()
    
    # test
    
    # state = State(False)
    
    # print("run -")
    # call(data, state, rule_fn)

    
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
    # test()