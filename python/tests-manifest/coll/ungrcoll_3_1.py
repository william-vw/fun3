import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/coll/ungrcoll_3-data.n3').data

def query(a_0, b_1, final_ctu):
    data.find(a_0, Iri('http://example.org/hasParts'), b_1, lambda s, p, o: final_ctu(s, o))
    rule_0(a_0, b_1, lambda a_2_m, b_3_m: final_ctu(a_2_m, b_3_m))

def rule_0(a_2, b_3, final_ctu):
    data.find(a_2, Iri('http://example.org/parts'), b_3, lambda s, p, o: final_ctu(s, o))
    if b_3 == Collection([Var('x_5'), Var('y_6')]):
        rule_1(a_2, b_3[0], b_3[1], lambda q_4_m, x_5, y_6: final_ctu(q_4_m, Collection([x_5, y_6])))

def rule_1(q_4, x_5, y_6, final_ctu):
    data.find(q_4, Iri('http://example.org/part'), x_5, lambda s, p, o: rule_1_1(s, o, y_6, final_ctu))

def rule_1_1(q_4, x_5, y_6, final_ctu):
    data.find(q_4, Iri('http://example.org/part'), y_6, lambda s, p, o: final_ctu(s, x_5, o))
query(ANY, ANY, lambda a_0, b_1: emit(Triple(Var('a_0'), Iri('http://example.org/hasParts'), Var('b_1')), {'a_0': a_0, 'b_1': b_1}))