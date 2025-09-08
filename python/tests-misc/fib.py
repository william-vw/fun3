import sys
sys.path.insert(0, "..") # noqa
import sys
from lib.trace import trace_calls
sys.settrace(trace_calls) # noqa
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.math import math_greaterThan
from n3.fun.builtins.math import math_difference
from n3.fun.builtins.math import math_difference
from n3.fun.builtins.math import math_sum
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-misc/fib_data.n3').data

def query(f_0, final_ctu):
    data.find(Literal(5, NS.xsd['int']), Iri('http://example.org/fib'), f_0, lambda s, p, o: final_ctu(o))
    rule_2(Literal(5, NS.xsd['int']), f_0, lambda n_1_m, f_2_m: final_ctu(f_2_m))

def rule_0(final_ctu):
    final_ctu()

def rule_1(final_ctu):
    final_ctu()

def rule_2(n_1, f_2, final_ctu):
    math_greaterThan(n_1, Literal(1, NS.xsd['int']), lambda s, o: rule_2_1(s, f_2, final_ctu))

def rule_2_1(n_1, f_2, final_ctu):
    math_difference(Collection([n_1, Literal(1, NS.xsd['int'])]), ANY, lambda s, o: rule_2_2(s[0], f_2, o, final_ctu))

def rule_2_2(n_1, f_2, n1_3, final_ctu):
    math_difference(Collection([n_1, Literal(2, NS.xsd['int'])]), ANY, lambda s, o: rule_2_3(s[0], f_2, n1_3, o, final_ctu))

def rule_2_3(n_1, f_2, n1_3, n2_4, final_ctu):
    data.find(n1_3, Iri('http://example.org/fib'), ANY, lambda s, p, o: rule_2_4(n_1, f_2, s, n2_4, o, final_ctu))
    if n1_3 == Literal(0, NS.xsd['int']):
        rule_0(lambda: rule_2_4(n_1, f_2, Literal(0, NS.xsd['int']), n2_4, Literal(1, NS.xsd['int']), final_ctu))
    if n1_3 == Literal(1, NS.xsd['int']):
        rule_1(lambda: rule_2_4(n_1, f_2, Literal(1, NS.xsd['int']), n2_4, Literal(1, NS.xsd['int']), final_ctu))
    rule_2(n1_3, ANY, lambda n_1_m, f_2_m: rule_2_4(n_1, f_2, n_1_m, n2_4, f_2_m, final_ctu))

def rule_2_4(n_1, f_2, n1_3, n2_4, f1_5, final_ctu):
    data.find(n2_4, Iri('http://example.org/fib'), ANY, lambda s, p, o: rule_2_5(n_1, f_2, n1_3, s, f1_5, o, final_ctu))
    if n2_4 == Literal(0, NS.xsd['int']):
        rule_0(lambda: rule_2_5(n_1, f_2, n1_3, Literal(0, NS.xsd['int']), f1_5, Literal(1, NS.xsd['int']), final_ctu))
    if n2_4 == Literal(1, NS.xsd['int']):
        rule_1(lambda: rule_2_5(n_1, f_2, n1_3, Literal(1, NS.xsd['int']), f1_5, Literal(1, NS.xsd['int']), final_ctu))
    rule_2(n2_4, ANY, lambda n_1_m, f_2_m: rule_2_5(n_1, f_2, n1_3, n_1_m, f1_5, f_2_m, final_ctu))

def rule_2_5(n_1, f_2, n1_3, n2_4, f1_5, f2_6, final_ctu):
    math_sum(Collection([f1_5, f2_6]), f_2, lambda s, o: final_ctu(n_1, o))
query(ANY, lambda f_0: emit(Triple(Literal(5, NS.xsd['int']), Iri('http://example.org/fib'), Var('f_0')), {'f_0': f_0}))