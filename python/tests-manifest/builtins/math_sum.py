import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.math import math_sum
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/builtins/math_sum-data.n3').data

def query(r_0, final_ctu):
    data.find(Iri('http://example.org/r'), Iri('http://example.org/result'), r_0, lambda s, p, o: final_ctu(o))
    rule_0(r_0, lambda r_1_m: final_ctu(r_1_m))

def rule_0(r_1, final_ctu):
    math_sum(Collection([Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int'])]), r_1, lambda s, o: final_ctu(o))
query(ANY, lambda r_0: emit(Triple(Iri('http://example.org/r'), Iri('http://example.org/result'), Var('r_0')), {'r_0': r_0}))