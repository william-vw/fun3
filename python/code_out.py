from n3.parse import parse_n3
from n3.terms import Iri, Var, Literal, Collection, ANY, term_types
from n3.ns import NS
from n3.fun.builtins.list import list_iterate
data = parse_n3('@prefix : <http://example.org/> .\n').data

def rule_0(y_0, final_ctu):
    list_iterate(Collection([Literal('c', NS.xsd['string']), Literal('b', NS.xsd['string']), Literal('c', NS.xsd['string'])]), Collection([Literal(1, NS.xsd['int']), Literal('c', NS.xsd['string'])]), lambda s, o: final_ctu(y_0))
rule_0(ANY, lambda a0: print(a0))