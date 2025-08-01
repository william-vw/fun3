import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/simple/person_ca.ttl').data

def query(x_0, final_ctu):
    data.find(x_0, NS.rdf['type'], Iri('http://example.org/Canadian'), lambda s, p, o: final_ctu(s))
    rule_0(x_0, lambda p_1_m: final_ctu(p_1_m))

def rule_0(p_1, final_ctu):
    data.find(p_1, NS.rdf['type'], Iri('http://example.org/Person'), lambda s, p, o: rule_0_1(s, final_ctu))

def rule_0_1(p_1, final_ctu):
    data.find(p_1, Iri('http://example.org/address'), ANY, lambda s, p, o: rule_0_2(s, o, final_ctu))

def rule_0_2(p_1, a_2, final_ctu):
    data.find(a_2, Iri('http://example.org/country'), Literal('CA', NS.xsd['string']), lambda s, p, o: final_ctu(p_1))
query(ANY, lambda x_0: emit(Triple(Var('x_0'), NS.rdf['type'], Iri('http://example.org/Canadian')), {'x_0': x_0}))