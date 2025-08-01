import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/bnodes/person_ca_eur.n3').data

def query(p_0, final_ctu):
    data.find(p_0, NS.rdf['type'], Iri('http://example.org/Canadian'), lambda s, p, o: final_ctu(s))
    rule_0(p_0, lambda p_1_m: final_ctu(p_1_m))

def rule_0(p_1, final_ctu):
    data.find(p_1, NS.rdf['type'], Iri('http://example.org/Person'), lambda s, p, o: rule_0_1(s, final_ctu))

def rule_0_1(p_1, final_ctu):
    data.find(p_1, Iri('http://example.org/address'), ANY, lambda s, p, o: rule_0_2(s, o, final_ctu))

def rule_0_2(p_1, b0_bn, final_ctu):
    data.find(b0_bn, Iri('http://example.org/country'), ANY, lambda s, p, o: rule_0_3(p_1, s, o, final_ctu))

def rule_0_3(p_1, b0_bn, b1_bn, final_ctu):
    data.find(b1_bn, Iri('http://example.org/locatedIn'), Literal('EUR', NS.xsd['string']), lambda s, p, o: final_ctu(p_1))

def rule_1(p_2, final_ctu):
    data.find(ANY, Iri('http://example.org/ability'), Iri('http://example.org/think'), lambda s, p, o: final_ctu(p_2))
query(ANY, lambda p_0: emit(Triple(Var('p_0'), NS.rdf['type'], Iri('http://example.org/Canadian')), {'p_0': p_0}))