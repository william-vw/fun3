import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/dupl_vars/dupl_vars_3-data.n3').data

def query(a_0, x_1, xl_2, final_ctu):
    data.find(a_0, Iri('http://example.org/partLabels'), Collection([x_1, xl_2]), lambda s, p, o: final_ctu(s, o[0], o[1]))
    rule_0(a_0, x_1, xl_2, lambda a_3_m, x_4, xl_5: final_ctu(a_3_m, x_4, xl_5))

def rule_0(a_3, x_4, xl_5, final_ctu):
    data.find(a_3, Iri('http://example.org/parts'), Collection([x_4, x_4]), lambda s, p, o: rule_0_1(s, o[1], xl_5, final_ctu) if o[0] == o[1] else False)
    rule_1(a_3, x_4, x_4, lambda q_6_m, k_7, l_8: rule_0_1(q_6_m, l_8, xl_5, final_ctu) if k_7 == l_8 else False)

def rule_0_1(a_3, x_4, xl_5, final_ctu):
    data.find(x_4, Iri('http://example.org/label'), xl_5, lambda s, p, o: final_ctu(a_3, s, o))

def rule_1(q_6, k_7, l_8, final_ctu):
    data.find(q_6, Iri('http://example.org/hasParts'), Collection([k_7, l_8]), lambda s, p, o: final_ctu(s, o[0], o[1]))
query(ANY, ANY, ANY, lambda a_0, x_1, xl_2: emit(Triple(Var('a_0'), Iri('http://example.org/partLabels'), Collection([Var('x_1'), Var('xl_2')])), {'a_0': a_0, 'x_1': x_1, 'xl_2': xl_2}))