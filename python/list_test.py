from n3.terms import term_types
from n3.model import Model
from n3.parse import parse_n3

def unify_coll_result(head_list, pos, match_conds, unify_vars):
    for i, el in enumerate(head_list):
        cur_pos = pos + [ i ]
        match el.type():
            case term_types.COLLECTION:
                unify_coll_result(el, cur_pos, match_conds, unify_vars)
            case term_types.VAR:
                unify_vars.append((el, cur_pos))
            case _:
                match_conds.append((el, cur_pos))
                

data = """@prefix : <http://example.org/> .
# :x :y ( 1 2 3 ) .
# :x :y ( ( 1 ) ( 2 3 ) ) .
# :x :y ( ( ?x 2 ) ( 3 ?y ) ?z ) .
{ :will :aliasNames ( ?xn ?yn ) } <= { :wil :alias ?x , ?y . ?x :name ?xn . ?y :name ?yn } .
"""
result = parse_n3(data)
data = result.data
rules = result.rules

# coll = data.df.iloc[0]
coll = rules[0].s.model.triples()[0].o
print("coll", coll, type(coll), coll._vars())#, coll._max_depth())

match_conds = []; unify_vars = []
unify_coll_result(coll, [], match_conds, unify_vars)

print("match_conds", match_conds, "unify_vars", unify_vars)