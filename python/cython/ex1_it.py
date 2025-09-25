import sys
sys.path.insert(0, "..") # noqa
import sys
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit, emitted

data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-bench/zika/data/gen100_pt2.n3').data

def query(x_0):
    for x_0 in rule_0(x_0):
        yield x_0

def rule_0(id_1):
    for p_2 in rule_1(ANY):
        for _, _, o in data.find_yield(p_2, Iri('http://hl7.org/fhir/id'), id_1):
            yield o

def rule_1(p_3):
    for p_3, _, _ in data.find_yield(p_3, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient')):
        yield p_3
                                
for x_0 in query(ANY):
    emit(Triple(Var('x_0'), Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean'])), {'x_0': x_0})
    
for t in emitted:
    print(t)