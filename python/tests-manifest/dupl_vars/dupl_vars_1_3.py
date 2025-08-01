import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/dupl_vars/dupl_vars_1-data.n3').data

def query(a_0, b_1, final_ctu):
    data.find(a_0, Iri('http://example.org/part'), b_1, lambda s, p, o: final_ctu(s, o))
    if a_0 == b_1:
        rule_0(b_1, lambda a_2_m: final_ctu(a_2_m, a_2_m))

def rule_0(a_2, final_ctu):
    data.find(a_2, Iri('http://example.org/parts'), Collection([Var('x_3'), Var('y_4')]), lambda s, p, o: rule_0_1(s, o[0], o[1], final_ctu))
    rule_1(a_2, Collection([Var('x_3'), Var('y_4')]), lambda q_7_m, a_8_m: rule_0_1(q_7_m, a_8_m[0], a_8_m[1], final_ctu))

def rule_0_1(a_2, x_3, y_4, final_ctu):
    data.find(x_3, Iri('http://example.org/label'), ANY, lambda s, p, o: rule_0_2(a_2, s, y_4, o, final_ctu))

def rule_0_2(a_2, x_3, y_4, xl_5, final_ctu):
    data.find(y_4, Iri('http://example.org/label'), ANY, lambda s, p, o: final_ctu(a_2))

def rule_1(q_7, a_8, final_ctu):
    data.find(q_7, Iri('http://example.org/hasParts'), a_8, lambda s, p, o: final_ctu(s, o))
query(ANY, ANY, lambda a_0, b_1: emit(Triple(Var('a_0'), Iri('http://example.org/part'), Var('b_1')), {'a_0': a_0, 'b_1': b_1}))