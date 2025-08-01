import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/gterm/ungraph2-data.n3').data

def query(a_0, data_1, final_ctu):
    data.find(a_0, Iri('http://example.org/partData'), data_1, lambda s, p, o: final_ctu(s, o))
    rule_0(a_0, data_1, lambda a_2_m, data_3_m: final_ctu(a_2_m, data_3_m))

def rule_0(a_2, data_3, final_ctu):
    data.find(a_2, Iri('http://example.org/parts'), data_3, lambda s, p, o: final_ctu(s, o))
    if data_3 == GraphTerm(triples=[Triple(Var('part_5'), NS.rdf['type'], Var('t_6'))]):
        rule_1(a_2, data_3[0][0], data_3[0][2], lambda q_4_m, part_5, t_6: final_ctu(q_4_m, GraphTerm(triples=[Triple(part_5, NS.rdf['type'], t_6)])))

def rule_1(q_4, part_5, t_6, final_ctu):
    data.find(q_4, Iri('http://example.org/has'), part_5, lambda s, p, o: rule_1_1(s, o, t_6, final_ctu))

def rule_1_1(q_4, part_5, t_6, final_ctu):
    data.find(part_5, NS.rdf['type'], t_6, lambda s, p, o: final_ctu(q_4, s, o))
query(ANY, ANY, lambda a_0, data_1: emit(Triple(Var('a_0'), Iri('http://example.org/partData'), Var('data_1')), {'a_0': a_0, 'data_1': data_1}))