import sys
sys.path.insert(0, "../../../..") # noqa
import sys
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from timeit import default_timer as timer

start = timer()
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-bench/zika/data/gen100000_pt2.n3').data
end = timer()
print("load:", end-start)

# - but, perhaps more flexibility; 
# if some clause does not contribute any variable values, 
# then it is enough to check if it returns _anything_ (don't have to loop over all results)

# e.g., 
# for _, _ in rule_3(vstatus_7, Literal('confirmed', NS.xsd['string'])):
#    yield p_3

# instead of looping there, simply check if rule_3 yields anything
# but, won't have a benefit here, since rule_3 will only have 1 result

# - this is really one long join (since we don't use builtins)
# (if you also count the parts in the called rules)
# maybe we could use pandas here to optimize those joins
# but, might as well directly compile to C then lol

def query(x_0):
    for s, _, _ in data.find_yield(x_0, Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean'])):
        yield s
        
    for x_0 in rule_0(x_0):
        yield x_0

def rule_0(id_1):
    for p_2, _, _ in data.find_yield(ANY, Iri('http://example.org/zika#isPregnant'), Literal(True, NS.xsd['boolean'])):
        for _, _, o in data.find_yield(p_2, Iri('http://hl7.org/fhir/id'), id_1):
            yield o

    for p_2 in rule_1(ANY):
        for _, _, o in data.find_yield(p_2, Iri('http://hl7.org/fhir/id'), id_1):
            yield o

def rule_1(p_3):
    for p_3, _, _ in data.find_yield(p_3, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient')):
        for p_3, _, c_4 in data.find_yield(p_3, Iri('http://example.org/utils#hasCondition'), ANY):
            for c_4, _, ccode_5 in data.find_yield(c_4, Iri('http://hl7.org/fhir/code'), ANY):
                for ccode_5, _, _ in data.find_yield(ccode_5, Iri('http://example.org/utils#hasCodeValue'), Literal(77386006, NS.xsd['int'])):
                    for c_4, _, cstatus_6 in data.find_yield(c_4, Iri('http://hl7.org/fhir/clinicalStatus'), ANY):
                        for cstatus_6, _, _ in data.find_yield(cstatus_6, Iri('http://example.org/utils#hasCodeValue'), Literal('active', NS.xsd['string'])):
                            for c_4, _, vstatus_7 in data.find_yield(c_4, Iri('http://hl7.org/fhir/verificationStatus'), ANY):
                                for _, _, _ in data.find_yield(vstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                                for _, _ in rule_3(vstatus_7, Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                        for cstatus_6, _ in rule_3(cstatus_6, Literal('active', NS.xsd['string'])):
                            for c_4, _, vstatus_7 in data.find_yield(c_4, Iri('http://hl7.org/fhir/verificationStatus'), ANY):
                                for _, _, _ in data.find_yield(vstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                                for _, _ in rule_3(vstatus_7, Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                for ccode_5, _ in rule_3(ccode_5, Literal(77386006, NS.xsd['int'])):
                    for c_4, _, cstatus_6 in data.find_yield(c_4, Iri('http://hl7.org/fhir/clinicalStatus'), ANY):
                        for cstatus_6, _, _ in data.find_yield(cstatus_6, Iri('http://example.org/utils#hasCodeValue'), Literal('active', NS.xsd['string'])):
                            for c_4, _, vstatus_7 in data.find_yield(c_4, Iri('http://hl7.org/fhir/verificationStatus'), ANY):
                                for _, _, _ in data.find_yield(vstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                                for _, _ in rule_3(vstatus_7, Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                        for cstatus_6, _ in rule_3(cstatus_6, Literal('active', NS.xsd['string'])):
                            for c_4, _, vstatus_7 in data.find_yield(c_4, Iri('http://hl7.org/fhir/verificationStatus'), ANY):
                                for _, _, _ in data.find_yield(vstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                                for _, _ in rule_3(vstatus_7, Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
        
        for p_3, c_4 in rule_4(p_3, ANY):
            for c_4, _, ccode_5 in data.find_yield(c_4, Iri('http://hl7.org/fhir/code'), ANY):
                for ccode_5, _, _ in data.find_yield(ccode_5, Iri('http://example.org/utils#hasCodeValue'), Literal(77386006, NS.xsd['int'])):
                    for c_4, _, cstatus_6 in data.find_yield(c_4, Iri('http://hl7.org/fhir/clinicalStatus'), ANY):
                        for cstatus_6, _, _ in data.find_yield(cstatus_6, Iri('http://example.org/utils#hasCodeValue'), Literal('active', NS.xsd['string'])):
                            for c_4, _, vstatus_7 in data.find_yield(c_4, Iri('http://hl7.org/fhir/verificationStatus'), ANY):
                                for _, _, _ in data.find_yield(vstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                                for _, _ in rule_3(vstatus_7, Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                        for cstatus_6, _ in rule_3(cstatus_6, Literal('active', NS.xsd['string'])):
                            for c_4, _, vstatus_7 in data.find_yield(c_4, Iri('http://hl7.org/fhir/verificationStatus'), ANY):
                                for _, _, _ in data.find_yield(vstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                                for _, _ in rule_3(vstatus_7, Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                for ccode_5, _ in rule_3(ccode_5, Literal(77386006, NS.xsd['int'])):
                    for c_4, _, cstatus_6 in data.find_yield(c_4, Iri('http://hl7.org/fhir/clinicalStatus'), ANY):
                        for cstatus_6, _, _ in data.find_yield(cstatus_6, Iri('http://example.org/utils#hasCodeValue'), Literal('active', NS.xsd['string'])):
                            for c_4, _, vstatus_7 in data.find_yield(c_4, Iri('http://hl7.org/fhir/verificationStatus'), ANY):
                                for _, _, _ in data.find_yield(vstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                                for _, _ in rule_3(vstatus_7, Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                        for cstatus_6, _ in rule_3(cstatus_6, Literal('active', NS.xsd['string'])):
                            for c_4, _, vstatus_7 in data.find_yield(c_4, Iri('http://hl7.org/fhir/verificationStatus'), ANY):
                                for _, _, _ in data.find_yield(vstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string'])):
                                    yield p_3
                                for _, _ in rule_3(vstatus_7, Literal('confirmed', NS.xsd['string'])):
                                    yield p_3

def rule_2(p_8, r_9):
    for p_8, _, id_10 in data.find_yield(p_8, Iri('http://hl7.org/fhir/id'), ANY):
        for s, _, _ in data.find_yield(r_9, Iri('http://hl7.org/fhir/subject'), id_10):
            yield p_8, s

def rule_3(r_11, c_12):
    for r_11, _, cod_13 in data.find_yield(r_11, Iri('http://hl7.org/fhir/coding'), ANY):
        for _, _, o in data.find_yield(cod_13, Iri('http://hl7.org/fhir/code'), c_12):
            yield r_11, o

def rule_4(p_14, c_15):
    for p_14, _, c_15 in data.find_yield(p_14, Iri('http://example.org/utils#has'), c_15):
        for s, _, _ in data.find_yield(c_15, NS.rdf['type'], Iri('http://hl7.org/fhir/Condition')):
            yield p_14, s
        
    for p_14, c_15 in rule_2(p_14, c_15):
        for s, _, _ in data.find_yield(c_15, NS.rdf['type'], Iri('http://hl7.org/fhir/Condition')):
            yield p_14, s

start = timer()
for x_0 in query(ANY):
    emit(Triple(Var('x_0'), Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean'])), {'x_0': x_0})
end = timer()
print("reason:", end-start)