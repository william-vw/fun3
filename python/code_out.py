from n3.parse import parse_n3
from n3.terms import Iri, Var, Literal, Collection, ANY, term_types
from n3.ns import NS
from n3.fun.builtins.list import list_append
data = parse_n3('@prefix : <http://example.org/> .\n').data

def rule_0(x_0, final_ctu):
    list_append(Collection([x_0]), Collection([Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int']), Literal(3, NS.xsd['int']), Literal(4, NS.xsd['int'])]), lambda s, o: final_ctu(s[0]))
rule_0(ANY, lambda a0: print(a0))