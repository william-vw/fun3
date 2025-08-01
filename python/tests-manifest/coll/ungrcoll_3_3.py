import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/coll/ungrcoll_3-data.n3').data

def query(final_ctu):
    data.find(Iri('http://example.org/robocop'), Iri('http://example.org/hasParts'), Collection([Iri('http://example.org/man'), Iri('http://example.org/machine')]), lambda s, p, o: final_ctu())
    rule_0(Iri('http://example.org/robocop'), Collection([Iri('http://example.org/man'), Iri('http://example.org/machine')]), lambda a_0_m, b_1_m: final_ctu())

def rule_0(a_0, b_1, final_ctu):
    data.find(a_0, Iri('http://example.org/parts'), b_1, lambda s, p, o: final_ctu(s, o))
    if b_1 == Collection([Var('x_3'), Var('y_4')]):
        rule_1(a_0, b_1[0], b_1[1], lambda q_2_m, x_3, y_4: final_ctu(q_2_m, Collection([x_3, y_4])))

def rule_1(q_2, x_3, y_4, final_ctu):
    data.find(q_2, Iri('http://example.org/part'), x_3, lambda s, p, o: rule_1_1(s, o, y_4, final_ctu))

def rule_1_1(q_2, x_3, y_4, final_ctu):
    data.find(q_2, Iri('http://example.org/part'), y_4, lambda s, p, o: final_ctu(s, x_3, o))
query(lambda: emit(Triple(Iri('http://example.org/robocop'), Iri('http://example.org/hasParts'), Collection([Iri('http://example.org/man'), Iri('http://example.org/machine')])), {}))