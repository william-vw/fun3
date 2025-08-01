import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/gterm/ungraph1-data.n3').data

def query(a_0, xl_1, final_ctu):
    data.find(a_0, Iri('http://example.org/partLabel'), xl_1, lambda s, p, o: final_ctu(s, o))
    rule_0(a_0, xl_1, lambda a_2_m, xl_3_m: final_ctu(a_2_m, xl_3_m))

def rule_0(a_2, xl_3, final_ctu):
    data.find(a_2, Iri('http://example.org/parts'), GraphTerm(triples=[Triple(Iri('http://example.org/robotorso'), NS.rdf['type'], Var('x_4'))]), lambda s, p, o: rule_0_1(s, xl_3, o[0][2], final_ctu))
    rule_1(a_2, Iri('http://example.org/robotorso'), ANY, lambda q_5_m, part_6, t_7: rule_0_1(q_5_m, xl_3, t_7, final_ctu))

def rule_0_1(a_2, xl_3, x_4, final_ctu):
    data.find(x_4, Iri('http://example.org/label'), xl_3, lambda s, p, o: final_ctu(a_2, o))

def rule_1(q_5, part_6, t_7, final_ctu):
    data.find(q_5, Iri('http://example.org/has'), part_6, lambda s, p, o: rule_1_1(s, o, t_7, final_ctu))

def rule_1_1(q_5, part_6, t_7, final_ctu):
    data.find(part_6, NS.rdf['type'], t_7, lambda s, p, o: final_ctu(q_5, s, o))
query(ANY, ANY, lambda a_0, xl_1: emit(Triple(Var('a_0'), Iri('http://example.org/partLabel'), Var('xl_1')), {'a_0': a_0, 'xl_1': xl_1}))