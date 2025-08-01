import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/coll/ungrcoll_3-data.n3').data

def query(a_0, final_ctu):
    data.find(a_0, Iri('http://example.org/hasParts'), Collection([Iri('http://example.org/man'), Iri('http://example.org/machine')]), lambda s, p, o: final_ctu(s))
    rule_0(a_0, Collection([Iri('http://example.org/man'), Iri('http://example.org/machine')]), lambda a_1_m, b_2_m: final_ctu(a_1_m))

def rule_0(a_1, b_2, final_ctu):
    data.find(a_1, Iri('http://example.org/parts'), b_2, lambda s, p, o: final_ctu(s, o))
    if b_2 == Collection([Var('x_4'), Var('y_5')]):
        rule_1(a_1, b_2[0], b_2[1], lambda q_3_m, x_4, y_5: final_ctu(q_3_m, Collection([x_4, y_5])))

def rule_1(q_3, x_4, y_5, final_ctu):
    data.find(q_3, Iri('http://example.org/part'), x_4, lambda s, p, o: rule_1_1(s, o, y_5, final_ctu))

def rule_1_1(q_3, x_4, y_5, final_ctu):
    data.find(q_3, Iri('http://example.org/part'), y_5, lambda s, p, o: final_ctu(s, x_4, o))
query(ANY, lambda a_0: emit(Triple(Var('a_0'), Iri('http://example.org/hasParts'), Collection([Iri('http://example.org/man'), Iri('http://example.org/machine')])), {'a_0': a_0}))