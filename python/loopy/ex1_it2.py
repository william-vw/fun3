import sys
sys.path.insert(0, "..") # noqa
import sys
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit, emitted

data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-bench/zika/data/gen100_pt2.n3').data

def query(x_0):
    for p_3, _, _ in data.find_yield(ANY, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient')):
        for _, _, o in data.find_yield(p_3, Iri('http://hl7.org/fhir/id'), x_0):
            yield o
                
for x_0 in query(ANY):
    emit(Triple(Var('x_0'), Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean'])), {'x_0': x_0})
    
for t in emitted:
    print(t)