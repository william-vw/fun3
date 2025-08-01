import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/dupl_vars/dupl_vars_1-data.n3').data

def query(final_ctu):
    data.find(Iri('http://example.org/robocop'), Iri('http://example.org/part'), Iri('http://example.org/robocop'), lambda s, p, o: final_ctu())
    if Iri('http://example.org/robocop') == Iri('http://example.org/robocop'):
        rule_0(Iri('http://example.org/robocop'), lambda a_0_m: final_ctu())

def rule_0(a_0, final_ctu):
    data.find(a_0, Iri('http://example.org/parts'), Collection([Var('x_1'), Var('y_2')]), lambda s, p, o: rule_0_1(s, o[0], o[1], final_ctu))
    rule_1(a_0, Collection([Var('x_1'), Var('y_2')]), lambda q_5_m, a_6_m: rule_0_1(q_5_m, a_6_m[0], a_6_m[1], final_ctu))

def rule_0_1(a_0, x_1, y_2, final_ctu):
    data.find(x_1, Iri('http://example.org/label'), ANY, lambda s, p, o: rule_0_2(a_0, s, y_2, o, final_ctu))

def rule_0_2(a_0, x_1, y_2, xl_3, final_ctu):
    data.find(y_2, Iri('http://example.org/label'), ANY, lambda s, p, o: final_ctu(a_0))

def rule_1(q_5, a_6, final_ctu):
    data.find(q_5, Iri('http://example.org/hasParts'), a_6, lambda s, p, o: final_ctu(s, o))
query(lambda: emit(Triple(Iri('http://example.org/robocop'), Iri('http://example.org/part'), Iri('http://example.org/robocop')), {}))