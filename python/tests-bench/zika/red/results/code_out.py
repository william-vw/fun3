import sys # noqa
sys.path.insert(0, "../../../..") # noqa
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.list import list_in
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-bench/zika/red/data_red_0pt2_mini.n3').data

def query(x_0, final_ctu):
    data.find(x_0, Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean']), lambda s, p, o: final_ctu(s))
    rule_0(x_0, lambda id_1_m: final_ctu(id_1_m))

def rule_0(id_1, final_ctu):
    data.find(ANY, Iri('http://example.org/zika#isPregnant'), Literal(True, NS.xsd['boolean']), lambda s, p, o: rule_0_1(id_1, s, final_ctu))
    rule_1(ANY, lambda p_4_m: rule_0_1(id_1, p_4_m, final_ctu))

def rule_0_1(id_1, p_2, final_ctu):
    data.find(p_2, Iri('http://example.org/zika#hasZikaSymptom'), ANY, lambda s, p, o: rule_0_2(id_1, s, o, final_ctu))
    rule_2(p_2, ANY, lambda p_9_m, c_10_m: rule_0_2(id_1, p_9_m, c_10_m, final_ctu))

def rule_0_2(id_1, p_2, symptom_3, final_ctu):
    data.find(p_2, Iri('http://hl7.org/fhir/id'), id_1, lambda s, p, o: final_ctu(o))

def rule_1(p_4, final_ctu):
    data.find(p_4, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s, p, o: rule_1_1(s, final_ctu))

def rule_1_1(p_4, final_ctu):
    data.find(p_4, Iri('http://example.org/utils#hasCondition'), ANY, lambda s, p, o: rule_1_2(s, o, final_ctu))
    rule_5(p_4, ANY, lambda p_21_m, c_22_m: rule_1_2(p_21_m, c_22_m, final_ctu))

def rule_1_2(p_4, c_5, final_ctu):
    data.find(c_5, Iri('http://hl7.org/fhir/code'), ANY, lambda s, p, o: rule_1_3(p_4, s, o, final_ctu))

def rule_1_3(p_4, c_5, ccode_6, final_ctu):
    data.find(ccode_6, Iri('http://example.org/utils#hasCodeValue'), Literal(77386006, NS.xsd['int']), lambda s, p, o: rule_1_4(p_4, c_5, s, final_ctu))
    rule_4(ccode_6, Literal(77386006, NS.xsd['int']), lambda r_18_m, c_19_m: rule_1_4(p_4, c_5, r_18_m, final_ctu))

def rule_1_4(p_4, c_5, ccode_6, final_ctu):
    data.find(c_5, Iri('http://hl7.org/fhir/clinicalStatus'), ANY, lambda s, p, o: rule_1_5(p_4, s, ccode_6, o, final_ctu))

def rule_1_5(p_4, c_5, ccode_6, cstatus_7, final_ctu):
    data.find(cstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('active', NS.xsd['string']), lambda s, p, o: rule_1_6(p_4, c_5, ccode_6, s, final_ctu))
    rule_4(cstatus_7, Literal('active', NS.xsd['string']), lambda r_18_m, c_19_m: rule_1_6(p_4, c_5, ccode_6, r_18_m, final_ctu))

def rule_1_6(p_4, c_5, ccode_6, cstatus_7, final_ctu):
    data.find(c_5, Iri('http://hl7.org/fhir/verificationStatus'), ANY, lambda s, p, o: rule_1_7(p_4, s, ccode_6, cstatus_7, o, final_ctu))

def rule_1_7(p_4, c_5, ccode_6, cstatus_7, vstatus_8, final_ctu):
    data.find(vstatus_8, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string']), lambda s, p, o: final_ctu(p_4))
    rule_4(vstatus_8, Literal('confirmed', NS.xsd['string']), lambda r_18_m, c_19_m: final_ctu(p_4))

def rule_2(p_9, c_10, final_ctu):
    data.find(p_9, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s, p, o: rule_2_1(s, c_10, final_ctu))

def rule_2_1(p_9, c_10, final_ctu):
    data.find(p_9, Iri('http://example.org/utils#hasCondition'), c_10, lambda s, p, o: rule_2_2(s, o, final_ctu))
    rule_5(p_9, c_10, lambda p_21_m, c_22_m: rule_2_2(p_21_m, c_22_m, final_ctu))

def rule_2_2(p_9, c_10, final_ctu):
    data.find(c_10, Iri('http://hl7.org/fhir/clinicalStatus'), ANY, lambda s, p, o: rule_2_3(p_9, s, o, final_ctu))

def rule_2_3(p_9, c_10, cstatus_11, final_ctu):
    data.find(cstatus_11, Iri('http://example.org/utils#hasCodeValue'), Literal('active', NS.xsd['string']), lambda s, p, o: rule_2_4(p_9, c_10, s, final_ctu))
    rule_4(cstatus_11, Literal('active', NS.xsd['string']), lambda r_18_m, c_19_m: rule_2_4(p_9, c_10, r_18_m, final_ctu))

def rule_2_4(p_9, c_10, cstatus_11, final_ctu):
    data.find(c_10, Iri('http://hl7.org/fhir/verificationStatus'), ANY, lambda s, p, o: rule_2_5(p_9, s, cstatus_11, o, final_ctu))

def rule_2_5(p_9, c_10, cstatus_11, vstatus_12, final_ctu):
    data.find(vstatus_12, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string']), lambda s, p, o: rule_2_6(p_9, c_10, cstatus_11, s, final_ctu))
    rule_4(vstatus_12, Literal('confirmed', NS.xsd['string']), lambda r_18_m, c_19_m: rule_2_6(p_9, c_10, cstatus_11, r_18_m, final_ctu))

def rule_2_6(p_9, c_10, cstatus_11, vstatus_12, final_ctu):
    data.find(c_10, Iri('http://hl7.org/fhir/code'), ANY, lambda s, p, o: rule_2_7(p_9, s, cstatus_11, vstatus_12, o, final_ctu))

def rule_2_7(p_9, c_10, cstatus_11, vstatus_12, ccode_13, final_ctu):
    data.find(ccode_13, Iri('http://example.org/utils#hasCodeValue'), ANY, lambda s, p, o: rule_2_8(p_9, c_10, cstatus_11, vstatus_12, s, o, final_ctu))
    rule_4(ccode_13, ANY, lambda r_18_m, c_19_m: rule_2_8(p_9, c_10, cstatus_11, vstatus_12, r_18_m, c_19_m, final_ctu))

def rule_2_8(p_9, c_10, cstatus_11, vstatus_12, ccode_13, code_14, final_ctu):
    list_in(code_14, Collection([Literal(84387000, NS.xsd['int']), Literal(271749004, NS.xsd['int']), Literal(47725002, NS.xsd['int']), Literal(57676002, NS.xsd['int']), Literal(9826008, NS.xsd['int']), Literal(68962001, NS.xsd['int']), Literal(25064002, NS.xsd['int'])]), lambda s, o: final_ctu(p_9, c_10))

def rule_3(p_15, r_16, final_ctu):
    data.find(p_15, Iri('http://hl7.org/fhir/id'), ANY, lambda s, p, o: rule_3_1(s, r_16, o, final_ctu))

def rule_3_1(p_15, r_16, id_17, final_ctu):
    data.find(r_16, Iri('http://hl7.org/fhir/subject'), id_17, lambda s, p, o: final_ctu(p_15, s))

def rule_4(r_18, c_19, final_ctu):
    data.find(r_18, Iri('http://hl7.org/fhir/coding'), ANY, lambda s, p, o: rule_4_1(s, c_19, o, final_ctu))

def rule_4_1(r_18, c_19, cod_20, final_ctu):
    data.find(cod_20, Iri('http://hl7.org/fhir/code'), c_19, lambda s, p, o: final_ctu(r_18, o))

def rule_5(p_21, c_22, final_ctu):
    data.find(p_21, Iri('http://example.org/utils#has'), c_22, lambda s, p, o: rule_5_1(s, o, final_ctu))
    rule_3(p_21, c_22, lambda p_15_m, r_16_m: rule_5_1(p_15_m, r_16_m, final_ctu))

def rule_5_1(p_21, c_22, final_ctu):
    data.find(c_22, NS.rdf['type'], Iri('http://hl7.org/fhir/Condition'), lambda s, p, o: final_ctu(p_21, s))
query(ANY, lambda x_0: emit(Triple(Var('x_0'), Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean'])), {'x_0': x_0}))