import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.list import list_iterate
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/builtins/list_iterate_5-data.n3').data

def query(x_0, final_ctu):
    data.find(Iri('http://example.org/result'), Iri('http://example.org/value'), x_0, lambda s, p, o: final_ctu(o))
    if x_0 == Iri('http://example.org/correct'):
        rule_0(lambda: final_ctu(Iri('http://example.org/correct')))

def rule_0(final_ctu):
    list_iterate(Collection([Literal('c', NS.xsd['string']), Literal('b', NS.xsd['string']), Literal('c', NS.xsd['string'])]), Collection([Literal(2, NS.xsd['int']), Literal('c', NS.xsd['string'])]), lambda s, o: final_ctu())
query(ANY, lambda x_0: emit(Triple(Iri('http://example.org/result'), Iri('http://example.org/value'), Var('x_0')), {'x_0': x_0}))