import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.list import list_iterate
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/builtins/list_iterate_2-data.n3').data

def query(x_0, y_1, final_ctu):
    data.find(Iri('http://example.org/result'), Iri('http://example.org/cell'), Collection([x_0, y_1]), lambda s, p, o: final_ctu(o[0], o[1]))
    rule_0(x_0, y_1, lambda x_2, y_3: final_ctu(x_2, y_3))

def rule_0(x_2, y_3, final_ctu):
    list_iterate(Collection([Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int']), Literal(3, NS.xsd['int'])]), Collection([x_2, y_3]), lambda s, o: final_ctu(o[0], o[1]))
query(ANY, ANY, lambda x_0, y_1: emit(Triple(Iri('http://example.org/result'), Iri('http://example.org/cell'), Collection([Var('x_0'), Var('y_1')])), {'x_0': x_0, 'y_1': y_1}))