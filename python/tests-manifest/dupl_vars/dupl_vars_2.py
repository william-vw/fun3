import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/dupl_vars/dupl_vars_2-data.n3').data

def query(a_0, x_1, y_2, xl_3, final_ctu):
    data.find(a_0, Iri('http://example.org/partLabels'), Collection([x_1, y_2, xl_3]), lambda s, p, o: final_ctu(s, o[0], o[1], o[2]))
    rule_0(a_0, x_1, y_2, xl_3, lambda a_4_m, x_5, y_6, xl_7: final_ctu(a_4_m, x_5, y_6, xl_7))

def rule_0(a_4, x_5, y_6, xl_7, final_ctu):
    data.find(a_4, Iri('http://example.org/parts'), Collection([x_5, y_6]), lambda s, p, o: rule_0_1(s, o[0], o[1], xl_7, final_ctu))
    if x_5 == y_6:
        rule_1(a_4, y_6, lambda q_8_m, x_9: rule_0_1(q_8_m, x_9, x_9, xl_7, final_ctu))

def rule_0_1(a_4, x_5, y_6, xl_7, final_ctu):
    data.find(x_5, Iri('http://example.org/label'), xl_7, lambda s, p, o: final_ctu(a_4, s, y_6, o))

def rule_1(q_8, x_9, final_ctu):
    data.find(q_8, Iri('http://example.org/hasParts'), Collection([x_9, x_9]), lambda s, p, o: final_ctu(s, o[1]) if o[0] == o[1] else False)
query(ANY, ANY, ANY, ANY, lambda a_0, x_1, y_2, xl_3: emit(Triple(Var('a_0'), Iri('http://example.org/partLabels'), Collection([Var('x_1'), Var('y_2'), Var('xl_3')])), {'a_0': a_0, 'x_1': x_1, 'y_2': y_2, 'xl_3': xl_3}))