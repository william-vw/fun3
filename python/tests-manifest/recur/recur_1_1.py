import sys # noqa
import pathlib # noqa
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent.resolve())) # noqa
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/recur/recur_1-data.n3').data

def query(x_0, y_1, final_ctu):
    data.find(x_0, Iri('http://example.org/descendantOf'), y_1, lambda s, p, o: final_ctu(s, o))
    rule_0(x_0, y_1, lambda x_2, y_3: final_ctu(x_2, y_3))
    rule_1(x_0, y_1, lambda x_4, z_5: final_ctu(x_4, z_5))

def rule_0(x_2, y_3, final_ctu):
    data.find(x_2, Iri('http://example.org/hasParent'), y_3, lambda s, p, o: final_ctu(s, o))

def rule_1(x_4, z_5, final_ctu):
    data.find(x_4, Iri('http://example.org/hasParent'), ANY, lambda s, p, o: rule_1_1(s, z_5, o, final_ctu))

def rule_1_1(x_4, z_5, y_6, final_ctu):
    data.find(y_6, Iri('http://example.org/descendantOf'), z_5, lambda s, p, o: final_ctu(x_4, o))
    rule_0(y_6, z_5, lambda x_2, y_3: final_ctu(x_4, y_3))
    rule_1(y_6, z_5, lambda x_4, z_5: final_ctu(x_4, z_5))
query(ANY, ANY, lambda x_0, y_1: print(Triple(Var('x_0'), Iri('http://example.org/descendantOf'), Var('y_1')).instantiate({'x_0': x_0, 'y_1': y_1})))