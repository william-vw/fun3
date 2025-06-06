from n3.parse import parse_n3
from n3.objects import Iri, Var, Literal, Collection, ANY, Terms, Triple
from n3.ns import NS
data = parse_n3('@prefix : <http://example.org/> . \n:francois a :Person .\n:jean_marie a :Person .\n').data

def query(x, final_ctu):
    data.find(x, NS.rdf['type'], Iri('http://example.org/French'), lambda s, p, o: final_ctu(s))
    rule_0(x, lambda p_0: final_ctu(p_0))

def rule_0(p_0, final_ctu):
    data.find(p_0, NS.rdf['type'], Iri('http://example.org/Person'), lambda s, p, o: rule_0_1(s, final_ctu))

def rule_0_1(p_0, final_ctu):
    data.find(p_0, Iri('http://example.org/loves'), p_0, lambda s, p, o: final_ctu(o) if s == o else False)
    if p_0 == p_0:
        rule_1(p_0, lambda p_1: final_ctu(p_1) if p_1 == p_1 else False)

def rule_1(p_1, final_ctu):
    final_ctu(p_1)
query(ANY, lambda x: print(Triple(Var('x'), NS.rdf['type'], Iri('http://example.org/French')).instantiate({'x': x})))