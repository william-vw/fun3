import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.list import list_iterate
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/builtins/list_iterate-data.n3').data

def query(c_0, final_ctu):
    data.find(Iri('http://example.org/result'), Iri('http://example.org/cell'), c_0, lambda s, p, o: final_ctu(o))
    rule_0(c_0, lambda c_1_m: final_ctu(c_1_m))

def rule_0(c_1, final_ctu):
    list_iterate(Collection([Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int']), Literal(3, NS.xsd['int'])]), c_1, lambda s, o: final_ctu(o))
query(ANY, lambda c_0: emit(Triple(Iri('http://example.org/result'), Iri('http://example.org/cell'), Var('c_0')), {'c_0': c_0}))