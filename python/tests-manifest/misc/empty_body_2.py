import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/misc/french.n3').data

def query(x_0, final_ctu):
    data.find(x_0, NS.rdf['type'], Iri('http://example.org/French'), lambda s, p, o: final_ctu(s))
    rule_0(x_0, lambda p_1_m: final_ctu(p_1_m))

def rule_0(p_1, final_ctu):
    data.find(p_1, NS.rdf['type'], Iri('http://example.org/Person'), lambda s, p, o: rule_0_1(s, final_ctu))

def rule_0_1(p_1, final_ctu):
    data.find(p_1, Iri('http://example.org/loves'), p_1, lambda s, p, o: final_ctu(o) if s == o else False)
    if p_1 == p_1:
        rule_1(p_1, lambda p_2_m: final_ctu(p_2_m) if p_2_m == p_2_m else False)

def rule_1(p_2, final_ctu):
    final_ctu(p_2)
query(ANY, lambda x_0: emit(Triple(Var('x_0'), NS.rdf['type'], Iri('http://example.org/French')), {'x_0': x_0}))