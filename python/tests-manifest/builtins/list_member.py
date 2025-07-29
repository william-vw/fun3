import sys # noqa
sys.path.insert(0, "../..") # noqa
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.list import list_member
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/builtins/list_member-data.n3').data

def query(m_0, final_ctu):
    data.find(Iri('http://example.org/result'), Iri('http://example.org/element'), m_0, lambda s, p, o: final_ctu(o))
    rule_0(m_0, lambda m_1_m: final_ctu(m_1_m))

def rule_0(m_1, final_ctu):
    list_member(Collection([Literal('a', NS.xsd['string']), Literal(1, NS.xsd['int']), Literal(2, NS.xsd['int'])]), m_1, lambda s, o: final_ctu(o))
query(ANY, lambda m_0: emit(Triple(Iri('http://example.org/result'), Iri('http://example.org/element'), Var('m_0')), {'m_0': m_0}))