import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.math import math_sum
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/builtins/math_sum_3-data.n3').data

def query(final_ctu):
    data.find(Collection([Literal(3, NS.xsd['int']), Literal(4, NS.xsd['int'])]), Iri('http://example.org/result'), Literal(7, NS.xsd['int']), lambda s, p, o: final_ctu())
    rule_0(Literal(3, NS.xsd['int']), Literal(4, NS.xsd['int']), Literal(7, NS.xsd['int']), lambda x_0, y_1, r_2_m: final_ctu())

def rule_0(x_0, y_1, r_2, final_ctu):
    math_sum(Collection([x_0, y_1]), r_2, lambda s, o: final_ctu(s[0], s[1], o))
query(lambda: emit(Triple(Collection([Literal(3, NS.xsd['int']), Literal(4, NS.xsd['int'])]), Iri('http://example.org/result'), Literal(7, NS.xsd['int'])), {}))