from n3.parse import parse_n3
from n3.objects import Iri, Var, Literal, Collection, ANY, term_types, Triple
from n3.ns import NS
from n3.fun.builtins.list import list_append
data = parse_n3('@prefix : <http://example.org/> .\n').data

def query(x, final_ctu):
    data.find(Iri('http://example.org/result'), Iri('http://example.org/is'), x, lambda s, p, o: final_ctu(o))
    if x == Iri('http://example.org/works'):
        rule_0(lambda: final_ctu(Iri('http://example.org/works')))

def rule_0(final_ctu):
    list_append(Collection([Collection([Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int'])]), Collection([Literal(3, NS.xsd['int']), Literal(4, NS.xsd['int'])])]), Collection([Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int']), Literal(3, NS.xsd['int']), Literal(4, NS.xsd['int'])]), lambda s, o: final_ctu())
query(ANY, lambda x: print(Triple(Iri('http://example.org/result'), Iri('http://example.org/is'), Var('x')).instantiate({'x': x})))