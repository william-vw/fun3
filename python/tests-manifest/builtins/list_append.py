import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.list import list_append
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/builtins/list_append-data.n3').data

def query(x_0, final_ctu):
    data.find(Iri('http://example.org/result'), Iri('http://example.org/is'), x_0, lambda s, p, o: final_ctu(o))
    rule_0(x_0, lambda x_1_m: final_ctu(x_1_m))

def rule_0(x_1, final_ctu):
    list_append(Collection([Collection([Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int'])]), Collection([Literal(3, NS.xsd['int']), Literal(4, NS.xsd['int'])])]), x_1, lambda s, o: final_ctu(o))
query(ANY, lambda x_0: emit(Triple(Iri('http://example.org/result'), Iri('http://example.org/is'), Var('x_0')), {'x_0': x_0}))