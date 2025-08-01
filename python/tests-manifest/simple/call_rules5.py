import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/simple/person_ca.ttl').data

def query(x_0, t_1, final_ctu):
    data.find(x_0, Iri('http://example.org/label'), t_1, lambda s, p, o: final_ctu(s, o))
    rule_0(x_0, t_1, lambda p_2_m, t_3_m: final_ctu(p_2_m, t_3_m))

def rule_0(p_2, t_3, final_ctu):
    data.find(p_2, NS.rdf['type'], t_3, lambda s, p, o: rule_0_1(s, o, final_ctu))
    rule_1(p_2, t_3, lambda p_5_m, t_6_m: rule_0_1(p_5_m, t_6_m, final_ctu))
    if t_3 == Iri('http://example.org/Greek'):
        rule_2(p_2, lambda p_7_m: rule_0_1(p_7_m, Iri('http://example.org/Greek'), final_ctu))

def rule_0_1(p_2, t_3, final_ctu):
    data.find(p_2, Iri('http://example.org/address'), ANY, lambda s, p, o: rule_0_2(s, t_3, o, final_ctu))

def rule_0_2(p_2, t_3, a_4, final_ctu):
    data.find(a_4, Iri('http://example.org/country'), Literal('CA', NS.xsd['string']), lambda s, p, o: final_ctu(p_2, t_3))

def rule_1(p_5, t_6, final_ctu):
    data.find(p_5, Iri('http://example.org/describedAs'), t_6, lambda s, p, o: final_ctu(s, o))

def rule_2(p_7, final_ctu):
    data.find(p_7, Iri('http://example.org/name'), Literal('Socrates', NS.xsd['string']), lambda s, p, o: final_ctu(s))
query(ANY, ANY, lambda x_0, t_1: emit(Triple(Var('x_0'), Iri('http://example.org/label'), Var('t_1')), {'x_0': x_0, 't_1': t_1}))