from ast import dump, unparse, parse
from collections import Counter
from multidict import MultiDict

from n3.parse import parse_n3
from n3.fun.gen2 import gen_py, InputData, InputCall, RuleFn
from n3.terms import Triple, Iri, Collection, ANY
from n3.model import Model
  

class State : 
    def __init__(self, stop):
        self.stop = stop


def fun3():
    
# - input
    
# . test 1
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

# . test 2
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
    
# . test 3
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

# # (2) duplicate vars in head tp
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :partLabels ( ?x ?y ?xl ) } <= { ?a :parts ( ?x ?y ) . ?x :label ?xl } . 
# { ?q :parts ( ?x ?x ) } <= { ?q :hasParts ?a } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :hasParts ( :man :machine ).
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY, ANY, ANY, ANY ]
#     # rule_args = [ ANY, Iri("http://example.org/man"), Iri("http://example.org/machine"), ANY ]

# (3) duplicate vars in body tp
    rules_str =  """@prefix : <http://example.org/> . 
{ ?a :partLabels ( ?x ?xl ) } <= { ?a :parts ( ?x ?x ) . ?x :label ?xl } . 
{ ?q :parts ( ?k ?l ) } <= { ?q :hasParts ( ?k ?l ) } .
"""

    data_str = """@prefix : <http://example.org/> . 
:robocop :hasParts ( :man :man ).
:man :label "man" . :machine :label "machine" .
"""

    rule_args = [ ANY, ANY, ANY ]
    
    # - parse
    
    rules = parse_n3(rules_str).rules
    # print("rules:\n", result.rules)
    # print()
    
    # - generate
    
    # print(dump(mod, indent=4)) # gives an indented version of the ast
    # print(unparse_with_lineno(mod)) # converts the ast to py code with line no
    # unparsed = unparse(mod) # converts the ast to py code
    
    # 1/ save code
    mod = gen_py(rules, InputData(data_str=data_str), InputCall(0, rule_args))
    unparsed = unparse(mod)
    print(unparsed)
    
    with open("code_out.py", 'w') as fh:
        fh.write(unparsed)
    
    # # 2/ run a rule fn
    # mod = gen_py(rules, InputData(data_str=data_str)) # no call yet (won't work)
    
    # exec_ret = get_exec(mod, InputData(data_str=data_str))
    # exec_rule(exec_ret, InputCall(0, rule_args))

    
def unparse_with_lineno(ast):
    code = unparse(ast)
    return "\n".join([ f"{i+1}. {line}" for i, line in enumerate(code.split("\n")) ])

def get_exec(mod, in_data): 
    mod_code = compile(mod, "<fun3>", "exec")
    
    global data
    data = parse_n3(in_data.data_str).data
    
    new_refs = {}
    exec(mod_code, globals(), new_refs)
    # print(new_refs)
    
    for name, code in new_refs.items():
        globals()[name] = code
        
    return new_refs

def exec_rule(exec_ret, in_call):
    fn_name = RuleFn.fn_name(in_call.rule_no, 0)
    
    rule_fn = exec_ret[fn_name] 
    rule_fn(*in_call.args, lambda *args: print(args))

def test_ast():
    print(dump(parse("""class State : 
    def __init__(self, stop):
        pass        
state = State()""")))
    
if __name__ == "__main__":
    fun3()
    # test_ast()