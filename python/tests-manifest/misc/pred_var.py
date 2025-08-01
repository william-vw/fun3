import sys # noqa
sys.path.insert(0, "../..") # noqa
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/misc/pred_var-data.n3').data

def query(x_0, final_ctu):
    data.find(Iri('http://example.org/a'), x_0, Iri('http://example.org/b'), lambda s, p, o: final_ctu(p))
    rule_0(x_0, lambda x_1_m: final_ctu(x_1_m))

def rule_0(x_1, final_ctu):
    data.find(Iri('http://example.org/a'), x_1, Iri('http://example.org/c'), lambda s, p, o: final_ctu(p))
    if x_1 == Iri('http://example.org/k'):
        rule_1(Iri('http://example.org/a'), lambda y_2_m: final_ctu(Iri('http://example.org/k')))

def rule_1(y_2, final_ctu):
    data.find(y_2, Iri('http://example.org/m'), ANY, lambda s, p, o: final_ctu(s))
    if y_2 == Iri('http://example.org/a'):
        rule_0(Iri('http://example.org/m'), lambda x_1_m: final_ctu(Iri('http://example.org/a')))
query(ANY, lambda x_0: emit(Triple(Iri('http://example.org/a'), Var('x_0'), Iri('http://example.org/b')), {'x_0': x_0}))