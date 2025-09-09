import sys
sys.path.insert(0, "..") # noqa
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from lib.memoize import MemoizeCtuPass
from n3.fun.builtins.list import list_member
from n3.fun.builtins.list import list_member
from n3.fun.builtins.math import math_greaterThan
from n3.fun.builtins.math import math_difference
from n3.fun.builtins.math import math_difference
from n3.fun.builtins.list import list_append
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-misc/fob_data.n3').data

@MemoizeCtuPass
def query(f_0, final_ctu):
    data.find(Literal(3, NS.xsd['int']), Iri('http://example.org/fob'), f_0, lambda s, p, o: final_ctu(o))
    rule_2(Literal(3, NS.xsd['int']), f_0, lambda n_3_m, f_4_m: final_ctu(f_4_m))

@MemoizeCtuPass
def rule_0(m_1, final_ctu):
    list_member(Collection([Literal('a', NS.xsd['string']), Literal('b', NS.xsd['string'])]), m_1, lambda s, o: final_ctu(o))

@MemoizeCtuPass
def rule_1(m_2, final_ctu):
    list_member(Collection([Literal('c', NS.xsd['string']), Literal('d', NS.xsd['string'])]), m_2, lambda s, o: final_ctu(o))

@MemoizeCtuPass
def rule_2(n_3, f_4, final_ctu):
    math_greaterThan(n_3, Literal(1, NS.xsd['int']), lambda s, o: rule_2_1(s, f_4, final_ctu))

def rule_2_1(n_3, f_4, final_ctu):
    math_difference(Collection([n_3, Literal(1, NS.xsd['int'])]), ANY, lambda s, o: rule_2_2(s[0], f_4, o, final_ctu))

def rule_2_2(n_3, f_4, n1_5, final_ctu):
    math_difference(Collection([n_3, Literal(2, NS.xsd['int'])]), ANY, lambda s, o: rule_2_3(s[0], f_4, n1_5, o, final_ctu))

def rule_2_3(n_3, f_4, n1_5, n2_6, final_ctu):
    data.find(n1_5, Iri('http://example.org/fob'), ANY, lambda s, p, o: rule_2_4(n_3, f_4, s, n2_6, o, final_ctu))
    if n1_5 == Literal(0, NS.xsd['int']):
        rule_0(ANY, lambda m_1_m: rule_2_4(n_3, f_4, Literal(0, NS.xsd['int']), n2_6, m_1_m, final_ctu))
    if n1_5 == Literal(1, NS.xsd['int']):
        rule_1(ANY, lambda m_2_m: rule_2_4(n_3, f_4, Literal(1, NS.xsd['int']), n2_6, m_2_m, final_ctu))
    rule_2(n1_5, ANY, lambda n_3_m, f_4_m: rule_2_4(n_3, f_4, n_3_m, n2_6, f_4_m, final_ctu))

def rule_2_4(n_3, f_4, n1_5, n2_6, f1_7, final_ctu):
    data.find(n2_6, Iri('http://example.org/fob'), ANY, lambda s, p, o: rule_2_5(n_3, f_4, n1_5, s, f1_7, o, final_ctu))
    if n2_6 == Literal(0, NS.xsd['int']):
        rule_0(ANY, lambda m_1_m: rule_2_5(n_3, f_4, n1_5, Literal(0, NS.xsd['int']), f1_7, m_1_m, final_ctu))
    if n2_6 == Literal(1, NS.xsd['int']):
        rule_1(ANY, lambda m_2_m: rule_2_5(n_3, f_4, n1_5, Literal(1, NS.xsd['int']), f1_7, m_2_m, final_ctu))
    rule_2(n2_6, ANY, lambda n_3_m, f_4_m: rule_2_5(n_3, f_4, n1_5, n_3_m, f1_7, f_4_m, final_ctu))

def rule_2_5(n_3, f_4, n1_5, n2_6, f1_7, f2_8, final_ctu):
    list_append(Collection([Collection([f1_7]), Collection([f2_8])]), f_4, lambda s, o: final_ctu(n_3, o))
query(ANY, lambda f_0: emit(Triple(Literal(3, NS.xsd['int']), Iri('http://example.org/fob'), Var('f_0')), {'f_0': f_0}))