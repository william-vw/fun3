from n3.terms import term_types
from n3.model import Model
from n3.parse import parse_n3

# if clause_el is coll w/ vars:
# 	if match_el is coll (any case): call recursively
# 		(recursive call will add var assns & conds)

# conditions & assignments
# if clause_el is var:
#   if clause_el in in_vars:
#       add runtime condition: if clause el is none, add var assn for clause_el at pos; else, add equality check for clause_el with match_el at pos
#   else: add var assn for clause_el at pos
# else: if match_el is not var:
#   compile-time check

# pass arguments to match
# if match_el is var: 
#    if clause_el is var:
#       if clause_el in in_vars:
#           pass clause_el as arg
#       else: pass None as arg
#    else: pass clause_el as arg


def unify_coll(clause_coll, match_coll, pos, stmts, pass_args, in_vars):
    if len(clause_coll) != len(match_coll):
        return False

    for i, clause_el in enumerate(clause_coll):
        cur_pos = pos + [i]
        match_el = match_coll[i]
        
        if clause_el.type() == term_types.VAR:
            if clause_el.idx_val() in in_vars:
                stmts.append(f"{clause_el} is None then {clause_el} = match{cur_pos} else {clause_el} == match{cur_pos}")
            else:
                stmts.append(f"{clause_el} = match{cur_pos}")
        
        elif clause_el.type() == term_types.COLLECTION and len(clause_el._vars()) > 0:
            if match_el.type() == term_types.COLLECTION:
                unify_coll(clause_el, match_el, cur_pos, stmts, pass_args, in_vars)
        
        # both are concrete
        elif match_el.type() != term_types.VAR and clause_el != match_el:
            return False
        
        if not match_el.is_concrete():
            if not clause_el.is_concrete():
                if clause_el.idx_val() in in_vars:
                    pass_args.append(clause_el)
                else:
                    pass_args.append(None)
            else:
                pass_args.append(clause_el)
        
data = """@prefix : <http://example.org/> .
# :x :y ( 1 ?y ?z ) . :x :y ( 1 2 3 ) .
# :x :y ( 1 ?y ?z ) . :x :y ( 1 2 3 ) .
# :x :y ( 1 ?y ?z ) . :x :y ( 1 2 ?a ) .
:x :y ( 1 ?y 4 ) . :x :y ( 1 2 ?a ) .
"""
result = parse_n3(data)
data = result.data

coll1 = data.triples()[0].o
coll2 = data.triples()[1].o

print("coll?", coll1, "<>", coll2)

in_vars = ['y', 'z']; stmts = []; pass_args = []
unify_coll(coll1, coll2, [], stmts, pass_args, in_vars)

print("stmts:", stmts, "pass_args:", pass_args)