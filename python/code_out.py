from n3.parse import parse_n3
from n3.terms import Iri, Var, Literal, Collection, ANY, term_types
from n3.fun.builtins.math import math_sum
data = parse_n3('@prefix : <http://example.org/> .\n').data

def rule_0(x_0, y_1, r_2, final_ctu):
    math_sum(Collection([x_0, y_1]), r_2, lambda s, o: final_ctu(s[0], s[1], o))
rule_0(Literal(3, Iri('http://www.w3.org/2001/XMLSchema#int')), Literal(4, Iri('http://www.w3.org/2001/XMLSchema#int')), Literal(8, Iri('http://www.w3.org/2001/XMLSchema#int')), lambda a0, a1, a2: print(a0, a1, a2))