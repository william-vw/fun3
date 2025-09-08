from n3.parse import parse_n3
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from lib.memoize import MemoizeCtuPass
data = parse_n3('@prefix : <http://example.org/> . \n@prefix : <http://example.org/> . \n\n:will :hasParent :paul .\n:paul :hasParent :edward .\n# :edward :hasParent :peter . \n').data

@MemoizeCtuPass
def query(x_0, y_1, final_ctu):
    data.find(x_0, Iri('http://example.org/descendantOf'), y_1, lambda s, p, o: final_ctu(s, o))
    rule_0(x_0, y_1, lambda x_2_m, y_3_m: final_ctu(x_2_m, y_3_m))
    rule_1(x_0, y_1, lambda x_4_m, z_5_m: final_ctu(x_4_m, z_5_m))

@MemoizeCtuPass
def rule_0(x_2, y_3, final_ctu):
    data.find(x_2, Iri('http://example.org/hasParent'), y_3, lambda s, p, o: final_ctu(s, o))

@MemoizeCtuPass
def rule_1(x_4, z_5, final_ctu):
    data.find(x_4, Iri('http://example.org/hasParent'), ANY, lambda s, p, o: rule_1_1(s, z_5, o, final_ctu))

@MemoizeCtuPass
def rule_1_1(x_4, z_5, y_6, final_ctu):
    data.find(y_6, Iri('http://example.org/descendantOf'), z_5, lambda s, p, o: final_ctu(x_4, o))
    rule_0(y_6, z_5, lambda x_2_m, y_3_m: final_ctu(x_4, y_3_m))
    rule_1(y_6, z_5, lambda x_4_m, z_5_m: final_ctu(x_4, z_5_m))
query(ANY, ANY, lambda x_0, y_1: emit(Triple(Var('x_0'), Iri('http://example.org/descendantOf'), Var('y_1')), {'x_0': x_0, 'y_1': y_1}))