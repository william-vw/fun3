import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/coll/ungrcoll_4-data.n3').data

def query(a_0, final_ctu):
    data.find(a_0, Iri('http://example.org/partLabels'), Collection([Literal('man', NS.xsd['string']), Literal('machine', NS.xsd['string'])]), lambda s, p, o: final_ctu(s))
    rule_0(a_0, Literal('man', NS.xsd['string']), Literal('machine', NS.xsd['string']), lambda a_1_m, xl_2, yl_3: final_ctu(a_1_m))

def rule_0(a_1, xl_2, yl_3, final_ctu):
    data.find(a_1, Iri('http://example.org/parts'), Collection([Var('x_4'), Var('y_5')]), lambda s, p, o: rule_0_1(s, xl_2, yl_3, o[0], o[1], final_ctu))
    rule_1(a_1, Collection([Var('x_4'), Var('y_5')]), lambda q_6_m, a_7_m: rule_0_1(q_6_m, xl_2, yl_3, a_7_m[0], a_7_m[1], final_ctu))

def rule_0_1(a_1, xl_2, yl_3, x_4, y_5, final_ctu):
    data.find(x_4, Iri('http://example.org/label'), xl_2, lambda s, p, o: rule_0_2(a_1, o, yl_3, s, y_5, final_ctu))

def rule_0_2(a_1, xl_2, yl_3, x_4, y_5, final_ctu):
    data.find(y_5, Iri('http://example.org/label'), yl_3, lambda s, p, o: final_ctu(a_1, xl_2, o))

def rule_1(q_6, a_7, final_ctu):
    data.find(q_6, Iri('http://example.org/hasParts'), a_7, lambda s, p, o: final_ctu(s, o))
query(ANY, lambda a_0: emit(Triple(Var('a_0'), Iri('http://example.org/partLabels'), Collection([Literal('man', NS.xsd['string']), Literal('machine', NS.xsd['string'])])), {'a_0': a_0}))