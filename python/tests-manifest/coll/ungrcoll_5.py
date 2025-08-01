import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/coll/ungrcoll_5-data.n3').data

def query(a_0, x_1, y_2, final_ctu):
    data.find(a_0, Iri('http://example.org/partLabels'), Collection([x_1, y_2]), lambda s, p, o: final_ctu(s, o[0], o[1]))
    rule_0(a_0, x_1, y_2, lambda a_3_m, x_4, y_5: final_ctu(a_3_m, x_4, y_5))

def rule_0(a_3, x_4, y_5, final_ctu):
    data.find(a_3, Iri('http://example.org/parts'), Collection([x_4, y_5]), lambda s, p, o: rule_0_1(s, o[0], o[1], final_ctu))
    rule_1(a_3, Collection([x_4, y_5]), lambda q_8_m, a_9_m: rule_0_1(q_8_m, a_9_m[0], a_9_m[1], final_ctu))

def rule_0_1(a_3, x_4, y_5, final_ctu):
    data.find(x_4, Iri('http://example.org/label'), ANY, lambda s, p, o: rule_0_2(a_3, s, y_5, o, final_ctu))

def rule_0_2(a_3, x_4, y_5, xl_6, final_ctu):
    data.find(y_5, Iri('http://example.org/label'), ANY, lambda s, p, o: final_ctu(a_3, x_4, s))

def rule_1(q_8, a_9, final_ctu):
    data.find(q_8, Iri('http://example.org/hasParts'), a_9, lambda s, p, o: final_ctu(s, o))
query(ANY, ANY, ANY, lambda a_0, x_1, y_2: emit(Triple(Var('a_0'), Iri('http://example.org/partLabels'), Collection([Var('x_1'), Var('y_2')])), {'a_0': a_0, 'x_1': x_1, 'y_2': y_2}))