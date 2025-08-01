import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/coll/ungrcoll_1-data.n3').data

def query(a_0, xl_1, yl_2, final_ctu):
    data.find(a_0, Iri('http://example.org/partLabels'), Collection([xl_1, yl_2]), lambda s, p, o: final_ctu(s, o[0], o[1]))
    rule_0(a_0, xl_1, yl_2, lambda a_3_m, xl_4, yl_5: final_ctu(a_3_m, xl_4, yl_5))

def rule_0(a_3, xl_4, yl_5, final_ctu):
    data.find(a_3, Iri('http://example.org/parts'), Collection([Var('x_6'), Iri('http://example.org/machine')]), lambda s, p, o: rule_0_1(s, xl_4, yl_5, o[0], final_ctu))
    rule_1(a_3, Iri('http://example.org/machine'), lambda q_7_m, b_8: rule_0_1(q_7_m, xl_4, yl_5, Iri('http://example.org/man'), final_ctu))

def rule_0_1(a_3, xl_4, yl_5, x_6, final_ctu):
    data.find(x_6, Iri('http://example.org/label'), xl_4, lambda s, p, o: rule_0_2(a_3, o, yl_5, s, final_ctu))

def rule_0_2(a_3, xl_4, yl_5, x_6, final_ctu):
    data.find(Iri('http://example.org/machine'), Iri('http://example.org/label'), yl_5, lambda s, p, o: final_ctu(a_3, xl_4, o))

def rule_1(q_7, b_8, final_ctu):
    data.find(q_7, Iri('http://example.org/part'), Iri('http://example.org/man'), lambda s, p, o: rule_1_1(s, b_8, final_ctu))

def rule_1_1(q_7, b_8, final_ctu):
    data.find(q_7, Iri('http://example.org/part'), b_8, lambda s, p, o: final_ctu(s, o))
query(ANY, ANY, ANY, lambda a_0, xl_1, yl_2: emit(Triple(Var('a_0'), Iri('http://example.org/partLabels'), Collection([Var('xl_1'), Var('yl_2')])), {'a_0': a_0, 'xl_1': xl_1, 'yl_2': yl_2}))