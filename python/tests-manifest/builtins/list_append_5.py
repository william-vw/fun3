import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.list import list_append
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/builtins/list_append_5-data.n3').data

def query(x_0, y_1, z_2, final_ctu):
    data.find(Iri('http://example.org/result'), Iri('http://example.org/is'), Collection([x_0, y_1, z_2]), lambda s, p, o: final_ctu(o[0], o[1], o[2]))
    rule_0(x_0, y_1, z_2, lambda x_3, y_4, z_5: final_ctu(x_3, y_4, z_5))

def rule_0(x_3, y_4, z_5, final_ctu):
    list_append(Collection([Collection([Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int']), Literal(3, NS.xsd['int'])]), x_3, y_4, z_5]), Collection([Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int']), Literal(3, NS.xsd['int']), Literal(4, NS.xsd['int'])]), lambda s, o: final_ctu(s[1], s[2], s[3]))
query(ANY, ANY, ANY, lambda x_0, y_1, z_2: emit(Triple(Iri('http://example.org/result'), Iri('http://example.org/is'), Collection([Var('x_0'), Var('y_1'), Var('z_2')])), {'x_0': x_0, 'y_1': y_1, 'z_2': z_2}))