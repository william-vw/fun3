import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/gterm/ungraph2-data.n3').data

def query(a_0, final_ctu):
    data.find(a_0, Iri('http://example.org/partData'), GraphTerm(triples=[Triple(Iri('http://example.org/robotorso'), NS.rdf['type'], Iri('http://example.org/machine'))]), lambda s, p, o: final_ctu(s))
    rule_0(a_0, GraphTerm(triples=[Triple(Iri('http://example.org/robotorso'), NS.rdf['type'], Iri('http://example.org/machine'))]), lambda a_1_m, data_2_m: final_ctu(a_1_m))

def rule_0(a_1, data_2, final_ctu):
    data.find(a_1, Iri('http://example.org/parts'), data_2, lambda s, p, o: final_ctu(s, o))
    if data_2 == GraphTerm(triples=[Triple(Var('part_4'), NS.rdf['type'], Var('t_5'))]):
        rule_1(a_1, data_2[0][0], data_2[0][2], lambda q_3_m, part_4, t_5: final_ctu(q_3_m, GraphTerm(triples=[Triple(part_4, NS.rdf['type'], t_5)])))

def rule_1(q_3, part_4, t_5, final_ctu):
    data.find(q_3, Iri('http://example.org/has'), part_4, lambda s, p, o: rule_1_1(s, o, t_5, final_ctu))

def rule_1_1(q_3, part_4, t_5, final_ctu):
    data.find(part_4, NS.rdf['type'], t_5, lambda s, p, o: final_ctu(q_3, s, o))
query(ANY, lambda a_0: emit(Triple(Var('a_0'), Iri('http://example.org/partData'), GraphTerm(triples=[Triple(Iri('http://example.org/robotorso'), NS.rdf['type'], Iri('http://example.org/machine'))])), {'a_0': a_0}))