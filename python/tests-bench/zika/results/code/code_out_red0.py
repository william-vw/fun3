import sys
sys.path.insert(0, "../../../..") # noqa
import sys
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-bench/zika/data/gen5000_pt2.n3').data

def query(x_0, final_ctu):
    data.find(x_0, Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean']), lambda s, p, o: final_ctu(s))
    rule_0(x_0, lambda id_1_m: final_ctu(id_1_m))

def rule_0(id_1, final_ctu):
    data.find(ANY, Iri('http://example.org/zika#isPregnant'), Literal(True, NS.xsd['boolean']), lambda s, p, o: rule_0_1(id_1, s, final_ctu))
    rule_1(ANY, lambda p_3_m: rule_0_1(id_1, p_3_m, final_ctu))

def rule_0_1(id_1, p_2, final_ctu):
    data.find(p_2, Iri('http://hl7.org/fhir/id'), id_1, lambda s, p, o: final_ctu(o))

def rule_1(p_3, final_ctu):
    data.find(p_3, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s, p, o: rule_1_1(s, final_ctu))

def rule_1_1(p_3, final_ctu):
    data.find(p_3, Iri('http://example.org/utils#hasCondition'), ANY, lambda s, p, o: rule_1_2(s, o, final_ctu))
    rule_4(p_3, ANY, lambda p_14_m, c_15_m: rule_1_2(p_14_m, c_15_m, final_ctu))

def rule_1_2(p_3, c_4, final_ctu):
    data.find(c_4, Iri('http://hl7.org/fhir/code'), ANY, lambda s, p, o: rule_1_3(p_3, s, o, final_ctu))

def rule_1_3(p_3, c_4, ccode_5, final_ctu):
    data.find(ccode_5, Iri('http://example.org/utils#hasCodeValue'), Literal(77386006, NS.xsd['int']), lambda s, p, o: rule_1_4(p_3, c_4, s, final_ctu))
    rule_3(ccode_5, Literal(77386006, NS.xsd['int']), lambda r_11_m, c_12_m: rule_1_4(p_3, c_4, r_11_m, final_ctu))

def rule_1_4(p_3, c_4, ccode_5, final_ctu):
    data.find(c_4, Iri('http://hl7.org/fhir/clinicalStatus'), ANY, lambda s, p, o: rule_1_5(p_3, s, ccode_5, o, final_ctu))

def rule_1_5(p_3, c_4, ccode_5, cstatus_6, final_ctu):
    data.find(cstatus_6, Iri('http://example.org/utils#hasCodeValue'), Literal('active', NS.xsd['string']), lambda s, p, o: rule_1_6(p_3, c_4, ccode_5, s, final_ctu))
    rule_3(cstatus_6, Literal('active', NS.xsd['string']), lambda r_11_m, c_12_m: rule_1_6(p_3, c_4, ccode_5, r_11_m, final_ctu))

def rule_1_6(p_3, c_4, ccode_5, cstatus_6, final_ctu):
    data.find(c_4, Iri('http://hl7.org/fhir/verificationStatus'), ANY, lambda s, p, o: rule_1_7(p_3, s, ccode_5, cstatus_6, o, final_ctu))

def rule_1_7(p_3, c_4, ccode_5, cstatus_6, vstatus_7, final_ctu):
    data.find(vstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string']), lambda s, p, o: final_ctu(p_3))
    rule_3(vstatus_7, Literal('confirmed', NS.xsd['string']), lambda r_11_m, c_12_m: final_ctu(p_3))

def rule_2(p_8, r_9, final_ctu):
    data.find(p_8, Iri('http://hl7.org/fhir/id'), ANY, lambda s, p, o: rule_2_1(s, r_9, o, final_ctu))

def rule_2_1(p_8, r_9, id_10, final_ctu):
    data.find(r_9, Iri('http://hl7.org/fhir/subject'), id_10, lambda s, p, o: final_ctu(p_8, s))

def rule_3(r_11, c_12, final_ctu):
    data.find(r_11, Iri('http://hl7.org/fhir/coding'), ANY, lambda s, p, o: rule_3_1(s, c_12, o, final_ctu))

def rule_3_1(r_11, c_12, cod_13, final_ctu):
    data.find(cod_13, Iri('http://hl7.org/fhir/code'), c_12, lambda s, p, o: final_ctu(r_11, o))

def rule_4(p_14, c_15, final_ctu):
    data.find(p_14, Iri('http://example.org/utils#has'), c_15, lambda s, p, o: rule_4_1(s, o, final_ctu))
    rule_2(p_14, c_15, lambda p_8_m, r_9_m: rule_4_1(p_8_m, r_9_m, final_ctu))

def rule_4_1(p_14, c_15, final_ctu):
    data.find(c_15, NS.rdf['type'], Iri('http://hl7.org/fhir/Condition'), lambda s, p, o: final_ctu(p_14, s))

import time    
start_time = time.time()
query(ANY, lambda x_0: emit(Triple(Var('x_0'), Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean'])), {'x_0': x_0}))
end_time = time.time()    
print("elapsed:", (end_time - start_time))