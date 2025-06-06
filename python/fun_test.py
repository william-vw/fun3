from ast import dump, unparse, parse
from collections import Counter
from multidict import MultiDict

from n3.parse import parse_n3
from n3.fun.gen import gen_py, InputData, QueryFn
from n3.objects import Triple, Iri, Collection, ANY, Literal
from n3.model import Model
from n3.ns import xsdNs
  
  
def fun3():
    
# - input
    
# . test 1
# non-recursive rules without collections

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
#     rule_args = [ ANY ]

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
# non-recursive rules with grounded/ungrounded collections

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
# non-recursive rules with duplicate vars
    
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

# # (3) duplicate vars in body tp
#     rules_str =  """@prefix : <http://example.org/> . 
# { ?a :partLabels ( ?x ?xl ) } <= { ?a :parts ( ?x ?x ) . ?x :label ?xl } . 
# { ?q :parts ( ?k ?l ) } <= { ?q :hasParts ( ?k ?l ) } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :robocop :hasParts ( :man :man ).
# :man :label "man" . :machine :label "machine" .
# """

#     rule_args = [ ANY, ANY, ANY ]

# # . test 4
# # recursive rules

#     rules_str = """@prefix : <http://example.org/> . 
# { ?x :descendantOf ?y } <= { ?x :hasParent ?y } .
# { ?x :descendantOf ?z } <= { ?x :descendantOf ?y . ?y :descendantOf ?z } .
# """

#     data_str = """@prefix : <http://example.org/> . 
# :will :hasParent :paul .
# :paul :hasParent :edward .
# :edward :hasParent :peter .    
# """

#     rule_args = [ ANY, ANY ]

# . test 5
# builtins

# . test 5.1: math:sum

# (1) concrete list
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix math: <http://www.w3.org/2000/10/swap/math#> .
# { :r :result ?r } <= { (1 2) math:sum ?r } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     rule_args = [ ANY ]
    
# # (2) math:sum with var
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix math: <http://www.w3.org/2000/10/swap/math#> .
# { ?a :result ?r } <= { ?a math:sum ?r } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """
    
#     rule_args = [ Collection([ Literal(2, xsdNs['int']), Literal(3, xsdNs['int']) ]), ANY ]
#     # rule_args = [ Collection([ Literal(2, xsdNs['int']), Literal(3, xsdNs['int']) ]), Literal(5, xsdNs['int']) ]

# # (3) math:sum with ungrounded list
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix math: <http://www.w3.org/2000/10/swap/math#> .
# { ( ?x ?y ) :result ?r } <= { ( ?x ?y ) math:sum ?r } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     rule_args = [ Literal(3, xsdNs['int']), Literal(4, xsdNs['int']), ANY ]
#     # rule_args = [ Literal(3, xsdNs['int']), Literal(4, xsdNs['int']), Literal(7, xsdNs['int']) ]
    
# . test 5.2
# list:iterate
    
# # (1) list:iterate with var object
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix list: <http://www.w3.org/2000/10/swap/list#> .
# { :result :cell ?c } <= { ( 1 2 3 ) list:iterate ?c } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     rule_args = [ ANY ]
    
# # (2) list:iterate with ungrounded object
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix list: <http://www.w3.org/2000/10/swap/list#> .
# { :result :cell ( ?x ?y ) } <= { ( 1 2 3 ) list:iterate ( ?x ?y ) } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     rule_args = [ ANY, ANY ]
    
# # (3) list:iterate with (partially) grounded object
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix list: <http://www.w3.org/2000/10/swap/list#> .
# { :result :value ?x } <= { ( 'c' 'b' 'c' ) list:iterate ( 2 ?x ) } . # ( 2 'c' ), ( ?x 'c' )
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     rule_args = [ ANY ]
    
# test 5.3:
# list:append
    
# # (1)
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix list: <http://www.w3.org/2000/10/swap/list#> .
# { :result :is ?x . } <= { ( (1 2) (3 4) ) list:append ?x . } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     query_str = """@prefix : <http://example.org/> .
# :result :is ?x ."""

# # (2)
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix list: <http://www.w3.org/2000/10/swap/list#> .
# { :result :is :works . } <= { ( (1 2) (3 4) ) list:append (1 2 3 4) . } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     query_str = """@prefix : <http://example.org/> .
# :result :is ?x ."""
    
# # (3)
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix list: <http://www.w3.org/2000/10/swap/list#> .
# { :result :is ( ?x ) . } <= { ( ?x ) list:append (1 2 3 4) . } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     query_str = """@prefix : <http://example.org/> .
# :result :is ( ?x ) ."""

# # (4)
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix list: <http://www.w3.org/2000/10/swap/list#> .
# { :result :is ( ?x ?y ) . } <= { ( ?x ?y ) list:append (1 2 3 4) . } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     query_str = """@prefix : <http://example.org/> .
# :result :is ( ?x ?y ) ."""
    
# # (5)
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix list: <http://www.w3.org/2000/10/swap/list#> .
# { :result :is ( ?x ?y ?z ?a ) . } <= { ( ?x ?y ?z ?a ) list:append (1 2 3 4) . } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     query_str = """@prefix : <http://example.org/> .
# :result :is ( ?x ?y ?z ?a ) ."""

# # (6)
#     rules_str = """@prefix : <http://example.org/> . 
# @prefix list: <http://www.w3.org/2000/10/swap/list#> .
# { :result :is ( ?x ?y ?z ) . } <= { ( (1 2 3) ?x ?y ?z ) list:append (1 2 3 4) . } .
# """

#     data_str = """@prefix : <http://example.org/> .
# """

#     query_str = """@prefix : <http://example.org/> .
# :result :is ( ?x ?y ?z ) ."""

# (for other tests, checkout test_blt.py)

# test 6
# blank nodes

# # (1) bnode in body triple
#     rules_str = """@prefix : <http://example.org/> . 
# { ?p a :Canadian } <= { ?p a :Person . ?p :address _:a . _:a :country "CA" } .
# { ?p a :Person } <= { ?p :ability :think } .
# """

#     query_str = """@prefix : <http://example.org/> .
# ?x a :Canadian .
# """

# # (2) bnode in rule head
#     rules_str = """@prefix : <http://example.org/> . 
# { ?p a :Canadian } <= { ?p a :Person . ?p :address _:a . _:a :country "CA" } .
# { ?p a _:p } <= { ?p :ability :think } .
# """

#     query_str = """@prefix : <http://example.org/> .
# ?x a :Canadian .
# """

# # (3) same bnode in rule head & body
#     rules_str = """@prefix : <http://example.org/> . 
# { ?p a :Canadian } <= { ?p a :Person . ?p :address _:a . _:a :country "CA" } .
# { ?p a _:p } <= { _:p :ability :think . } .
# """

#     query_str = """@prefix : <http://example.org/> .
# ?x a :Canadian .
# """

# (4) resource path!
    rules_str = """@prefix : <http://example.org/> . 
{ ?p a :Canadian } <= { ?p a :Person . ?p!:address!:country :locatedIn "EUR" } .
{ ?p a _:p } <= { _:p :ability :think . } .
"""

    query_str = """@prefix : <http://example.org/> .
?x a :Canadian .
"""

    data_str = """@prefix : <http://example.org/> . 
:will a :Person ; :address :addr1 . :addr1 :country "CA" .
:ed :ability :think ; :address :addr1 ; :describedAs :Person .
:el :ability :drink ; :address :addr1 ; :describedAs :Belgian .
:dor :ability :think ; :address :addr1 ; :describedAs :German .
:soc :name "Socrates" ; a :Person ; :address :addr2 . :addr2 :country "GR" . "GR" :locatedIn "EUR" .
"""

    
    # - parse
    
    rules = parse_n3(rules_str).rules
    # print("rules:\n", rules)
    query = parse_n3(query_str).data.triple_at(0)
    # print()
    
    # - generate
    
    # print(dump(mod, indent=4)) # gives an indented version of the ast
    # print(unparse_with_lineno(mod)) # converts the ast to py code with line no
    # unparsed = unparse(mod) # converts the ast to py code
    
    # # 1/ save code
    # mod = gen_py(rules, query, InputData(data_str=data_str))
    # unparsed = unparse(mod)
    # print(unparsed)
    
    # with open("code_out.py", 'w') as fh:
    #     fh.write(unparsed)
    
    # 2/ run a rule fn
    mod = gen_py(rules, query, InputData(data_str=data_str), call_query=False)
    print(unparse(mod) + "\n\n")
    
    exec_ret = get_exec(mod, InputData(data_str=data_str))
    exec_query(exec_ret, query)

    
def unparse_with_lineno(ast):
    code = unparse(ast)
    return "\n".join([ f"{i+1}. {line}" for i, line in enumerate(code.split("\n")) ])

def get_exec(mod, in_data):
    mod_code = compile(mod, "<fun3>", "exec")
    
    global data
    data = parse_n3(in_data.data_str).data
    
    new_refs = {}
    exec(mod_code, globals(), new_refs)
    
    for name, code in new_refs.items():
        globals()[name] = code
        
    return new_refs

def exec_query(exec_ret, query):
    fn_name = QueryFn.fn_name()
    variables = query.recur_vars()
    
    query_fn = exec_ret[fn_name]
    query_fn(*[ANY for _ in variables], lambda *args: print(query.instantiate({ var: args[idx] for idx, var in enumerate(variables) })))

def test_ast():
    print(dump(parse("""a = 'abc'""")))
    
if __name__ == "__main__":
    fun3()
    # test_ast()