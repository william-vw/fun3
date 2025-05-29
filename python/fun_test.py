from ast import dump, unparse, parse
from collections import Counter
from multidict import MultiDict

from n3.parse import parse_n3
from n3.fun.gen2 import gen_py
from n3.terms import Triple, Iri, Collection, ANY
from n3.model import Model
  

class State : 
    def __init__(self, stop):
        self.stop = stop

def result_fn(*args):
    print(f"solution: { args }")
    # state.stop = True


def fun3():
    
# - test 1
# (non-recursive rules without collections)

# # (1) only query data
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a :country "CA" } . 
# """
#   rule_args = [ ANY ]

# # (2) call other rules (both terms concrete)
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a :country "CA" } . 
# { ?p a :Person } <= { ?p :ability :think } .
# { ?pe a :Belgian } <= { ?pe :ability :drink } .
# """
#   rule_args = [ ANY ]

# # (3) call other rules (clause term concrete, match term var)
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a :country "CA" } . 
# { ?pe a ?ty } <= { ?pe :describedAs ?ty } .
# """
#    rule_args = [ ANY ]

# # (4) call other rules (clause term var, match term concrete)
# # ("label"; not doing recursion yet)
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?p :label :Canadian } <= { ?p a ?t . ?p :address ?a . ?a :country "CA" } . 
# { ?pe a :Person } <= { ?pe :ability :drink } .
# """
#     rule_args = [ ANY ]

# # (5) call other rules (clause term var w/ runtime value, match term concrete)
# # ("label"; not doing recursion yet)
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?p :label ?t } <= { ?p a ?t . ?p :address ?a . ?a :country "CA" } . 
# { ?pe a :Person } <= { ?pe :ability :drink } .
# """
#     rule_args = [ ANY, ANY ]

# # (6) same level of specificity; all clauses have 2 variables
# # ("label"; not doing recursion yet)
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?p :label ?t } <= { ?p a ?t . ?p :address ?a . ?a :country "CA" } . 
# { ?p a ?t } <= { ?p :describedAs ?t } .
# { ?p a ?t } <= { ?p :name "Socrates" } . # t not used in body
# """
#     # rule_args = [ ANY, ANY ]
#     rule_args = [ Iri("http://example.org/el"), Iri("http://example.org/Belgian") ]

#     data_str = """@prefix : <http://example.org/> . 
# :will a :Person ; :address :addr1 . :addr1 :country "CA" .
# :ed :ability :think ; :address :addr1 ; :describedAs :Person .
# :el :ability :drink ; :address :addr1 ; :describedAs :Belgian .
# :dor :ability :think ; :address :addr1 ; :describedAs :German .
# :soc :name "Socrates" ; :address :addr1 .
# """

# - test 2
# (non-recursive rules with grounded/ungrounded collections)

# # (1) grounded; same nesting level
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :partLabels ( ?xl ?yl ) } <= { ?a :parts ( :man :machine ) . :man :label ?xl . :machine :label ?yl } . 
# { ?q :parts ( :man :machine ) } <= { ?q :part :man , :machine } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :part :man , :machine .
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY, ANY, ANY ]
    
# # (2) ungrounded (some vars); same nesting level
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :partLabels ( ?xl ?yl ) } <= { ?a :parts ( ?x :machine ) . ?x :label ?xl . :machine :label ?yl } . 
# { ?q :parts ( :man ?b ) } <= { ?q :part :man , ?b } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :part :man , :machine .
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY, ANY, ANY ]

# # (3) ungrounded (all vars); same nesting level
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :partLabels ( ?xl ?yl ) } <= { ?a :parts ( ?x ?y ) . ?x :label ?xl . ?y :label ?yl } . 
# { ?q :parts ( ?a ?b ) } <= { ?q :part ?a , ?b } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :part :man , :machine .
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY, ANY, ANY ]
    
# # (4) ungrounded (some vars); different nesting level
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :hasParts ?b } <= { ?a :parts ?b } . 
# { ?q :parts ( ?x ?y ) } <= { ?q :part ?x , ?y } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :part :man , :machine .
# :man :label "man" . :machine :label "machine" .
# """

#     # rule_args = [ ANY, ANY ]
#     # rule_args = [ ANY, Collection([ Iri("http://example.org/man"), Iri("http://example.org/machine") ]) ]
#     rule_args = [ ANY, Collection([ Iri("http://example.org/man") ]) ]
    
# # (5) ungrounded (some vars); different nesting level
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :partLabels ( ?xl ?yl ) } <= { ?a :parts ( ?x ?y ) . ?x :label ?xl . ?y :label ?yl } . 
# { ?q :parts ?a } <= { ?q :hasParts ?a } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :hasParts ( :man :machine ).
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY, ANY, ANY ]
    
# # (6) ungrounded (some vars); different nesting level
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :partLabels ( ?x ?y ) } <= { ?a :parts ( ?x ?y ) . ?x :label ?xl . ?y :label ?yl } . 
# { ?q :parts ?a } <= { ?q :hasParts ?a } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :hasParts ( :man :machine ).
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY, ANY, ANY ]
    
# # (7) ungrounded (some vars); nested lists
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :partLabels ( ?x ?y ) } <= { ?a :parts ( ( 1 2 ) ?b ) . ?x :label ?xl . ?y :label ?yl } . 
# { ?q :parts ( ?x ( 3 4 ) ) } <= { ?q :hasParts ?a } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :hasParts ( :man :machine ).
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY, ANY, ANY ]
    
# - test 3
# (non-recursive rules with duplicate vars)
    
# # (1) duplicate vars in non-called head tp
# # (no unification needed)
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :part ?a } <= { ?a :parts ( ?x ?y ) . ?x :label ?xl . ?y :label ?yl } . 
# { ?q :parts ?a } <= { ?q :hasParts ?a } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :hasParts ( :man :machine ).
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY ]

# (2) duplicate vars in head tp
    rules_str =  """@prefix : <http://example.org/> . 
{ ?a :partLabels ( ?x ?y ?xl ) } <= { ?a :parts ( ?x ?y ) . ?x :label ?xl } . 
{ ?q :parts ( ?x ?x ) } <= { ?q :hasParts ?a } .
"""

    data_str = """@prefix : <http://example.org/> . 
:robocop :hasParts ( :man :machine ).
:man :label "man" . :machine :label "machine" .
"""

    rule_args = [ ANY, ANY, ANY, ANY ]
    # rule_args = [ ANY, Iri("http://example.org/man"), Iri("http://example.org/machine"), ANY ]

# # (3) duplicate vars in body tp
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :partLabels ( ?x ?xl ) } <= { ?a :parts ( ?x ?x ) . ?x :label ?xl } . 
# { ?q :parts ( ?k ?l ) } <= { ?q :hasParts ?a } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :hasParts ( :man :machine ).
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY, ANY, ANY ]
    
    # parse
    
    rules = parse_n3(rules_str).rules
    # print("rules:\n", result.rules)
    
    global data
    data = parse_n3(data_str).data
    # print("data:\n", data)
    
    print()
    
    # generate
    
    mod = gen_py(rules)
    # print()
    # print(dump(mod, indent=4))
    # print(unparse_with_lineno(mod))
    print(unparse(mod))
    print()
    
    # compile
    
    rule_fn = compile_py(mod)
        
    # test
        
    # print("run -")
    rule_fn(*rule_args, result_fn)

    
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

def test_ast():
    print(dump(parse("""class State : 
    def __init__(self, stop):
        pass        
state = State()""")))
    
if __name__ == "__main__":
    fun3()
    # test_ast()