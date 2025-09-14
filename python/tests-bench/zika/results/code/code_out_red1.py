import sys
sys.path.insert(0, "../../../..") # noqa
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
from n3.fun.builtins.list import list_in
from n3.fun.builtins.list import list_in
from timeit import default_timer as timer

start = timer()
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-bench/zika/data/gen5000_pt5.n3').data
end = timer()
print("load:", end-start)

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
    data.find(p_2, Iri('http://example.org/zika#possibleZikaExposure'), Literal(True, NS.xsd['boolean']), lambda s, p, o: rule_0_3(id_1, s, symptom_3, final_ctu))
    rule_3(p_2, lambda p_15_m: rule_0_3(id_1, p_15_m, symptom_3, final_ctu))
    rule_4(p_2, lambda p_16_m: rule_0_3(id_1, p_16_m, symptom_3, final_ctu))

def rule_0_3(id_1, p_2, symptom_3, final_ctu):
    data.find(p_2, Iri('http://hl7.org/fhir/id'), id_1, lambda s, p, o: final_ctu(o))

def rule_1(p_4, final_ctu):
    data.find(p_4, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s, p, o: rule_1_1(s, final_ctu))

def rule_1_1(p_4, final_ctu):
    data.find(p_4, Iri('http://example.org/utils#hasCondition'), ANY, lambda s, p, o: rule_1_2(s, o, final_ctu))
    rule_13(p_4, ANY, lambda p_37_m, c_38_m: rule_1_2(p_37_m, c_38_m, final_ctu))

def rule_1_2(p_4, c_5, final_ctu):
    data.find(c_5, Iri('http://hl7.org/fhir/code'), ANY, lambda s, p, o: rule_1_3(p_4, s, o, final_ctu))

def rule_1_3(p_4, c_5, ccode_6, final_ctu):
    data.find(ccode_6, Iri('http://example.org/utils#hasCodeValue'), Literal(77386006, NS.xsd['int']), lambda s, p, o: rule_1_4(p_4, c_5, s, final_ctu))
    rule_12(ccode_6, Literal(77386006, NS.xsd['int']), lambda r_34_m, c_35_m: rule_1_4(p_4, c_5, r_34_m, final_ctu))

def rule_1_4(p_4, c_5, ccode_6, final_ctu):
    data.find(c_5, Iri('http://hl7.org/fhir/clinicalStatus'), ANY, lambda s, p, o: rule_1_5(p_4, s, ccode_6, o, final_ctu))

def rule_1_5(p_4, c_5, ccode_6, cstatus_7, final_ctu):
    data.find(cstatus_7, Iri('http://example.org/utils#hasCodeValue'), Literal('active', NS.xsd['string']), lambda s, p, o: rule_1_6(p_4, c_5, ccode_6, s, final_ctu))
    rule_12(cstatus_7, Literal('active', NS.xsd['string']), lambda r_34_m, c_35_m: rule_1_6(p_4, c_5, ccode_6, r_34_m, final_ctu))

def rule_1_6(p_4, c_5, ccode_6, cstatus_7, final_ctu):
    data.find(c_5, Iri('http://hl7.org/fhir/verificationStatus'), ANY, lambda s, p, o: rule_1_7(p_4, s, ccode_6, cstatus_7, o, final_ctu))

def rule_1_7(p_4, c_5, ccode_6, cstatus_7, vstatus_8, final_ctu):
    data.find(vstatus_8, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string']), lambda s, p, o: final_ctu(p_4))
    rule_12(vstatus_8, Literal('confirmed', NS.xsd['string']), lambda r_34_m, c_35_m: final_ctu(p_4))

def rule_2(p_9, c_10, final_ctu):
    data.find(p_9, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s, p, o: rule_2_1(s, c_10, final_ctu))

def rule_2_1(p_9, c_10, final_ctu):
    data.find(p_9, Iri('http://example.org/utils#hasCondition'), c_10, lambda s, p, o: rule_2_2(s, o, final_ctu))
    rule_13(p_9, c_10, lambda p_37_m, c_38_m: rule_2_2(p_37_m, c_38_m, final_ctu))

def rule_2_2(p_9, c_10, final_ctu):
    data.find(c_10, Iri('http://hl7.org/fhir/clinicalStatus'), ANY, lambda s, p, o: rule_2_3(p_9, s, o, final_ctu))

def rule_2_3(p_9, c_10, cstatus_11, final_ctu):
    data.find(cstatus_11, Iri('http://example.org/utils#hasCodeValue'), Literal('active', NS.xsd['string']), lambda s, p, o: rule_2_4(p_9, c_10, s, final_ctu))
    rule_12(cstatus_11, Literal('active', NS.xsd['string']), lambda r_34_m, c_35_m: rule_2_4(p_9, c_10, r_34_m, final_ctu))

def rule_2_4(p_9, c_10, cstatus_11, final_ctu):
    data.find(c_10, Iri('http://hl7.org/fhir/verificationStatus'), ANY, lambda s, p, o: rule_2_5(p_9, s, cstatus_11, o, final_ctu))

def rule_2_5(p_9, c_10, cstatus_11, vstatus_12, final_ctu):
    data.find(vstatus_12, Iri('http://example.org/utils#hasCodeValue'), Literal('confirmed', NS.xsd['string']), lambda s, p, o: rule_2_6(p_9, c_10, cstatus_11, s, final_ctu))
    rule_12(vstatus_12, Literal('confirmed', NS.xsd['string']), lambda r_34_m, c_35_m: rule_2_6(p_9, c_10, cstatus_11, r_34_m, final_ctu))

def rule_2_6(p_9, c_10, cstatus_11, vstatus_12, final_ctu):
    data.find(c_10, Iri('http://hl7.org/fhir/code'), ANY, lambda s, p, o: rule_2_7(p_9, s, cstatus_11, vstatus_12, o, final_ctu))

def rule_2_7(p_9, c_10, cstatus_11, vstatus_12, ccode_13, final_ctu):
    data.find(ccode_13, Iri('http://example.org/utils#hasCodeValue'), ANY, lambda s, p, o: rule_2_8(p_9, c_10, cstatus_11, vstatus_12, s, o, final_ctu))
    rule_12(ccode_13, ANY, lambda r_34_m, c_35_m: rule_2_8(p_9, c_10, cstatus_11, vstatus_12, r_34_m, c_35_m, final_ctu))

def rule_2_8(p_9, c_10, cstatus_11, vstatus_12, ccode_13, code_14, final_ctu):
    list_in(code_14, Collection([Literal(84387000, NS.xsd['int']), Literal(271749004, NS.xsd['int']), Literal(47725002, NS.xsd['int']), Literal(57676002, NS.xsd['int']), Literal(9826008, NS.xsd['int']), Literal(68962001, NS.xsd['int']), Literal(25064002, NS.xsd['int'])]), lambda s, o: final_ctu(p_9, c_10))

def rule_3(p_15, final_ctu):
    data.find(p_15, Iri('http://example.org/zika#recentTravelToZikaArea'), Literal(True, NS.xsd['boolean']), lambda s, p, o: final_ctu(s))
    rule_5(p_15, lambda p_17_m: final_ctu(p_17_m))

def rule_4(p_16, final_ctu):
    data.find(p_16, Iri('http://example.org/zika#recentSexualEncounterWithZikaResidentOrTraveler'), Literal(True, NS.xsd['boolean']), lambda s, p, o: final_ctu(s))
    rule_10(p_16, lambda p_27_m: final_ctu(p_27_m))

def rule_5(p_17, final_ctu):
    data.find(p_17, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s, p, o: rule_5_1(s, final_ctu))

def rule_5_1(p_17, final_ctu):
    data.find(p_17, Iri('http://example.org/utils#hasObservation'), ANY, lambda s, p, o: rule_5_2(s, o, final_ctu))
    rule_14(p_17, ANY, lambda p_39_m, o_40_m: rule_5_2(p_39_m, o_40_m, final_ctu))

def rule_5_2(p_17, o_18, final_ctu):
    data.find(o_18, Iri('http://hl7.org/fhir/code'), ANY, lambda s, p, o: rule_5_3(p_17, s, o, final_ctu))

def rule_5_3(p_17, o_18, oc_19, final_ctu):
    data.find(oc_19, Iri('http://example.org/utils#hasCodeValue'), Literal(420008001, NS.xsd['int']), lambda s, p, o: rule_5_4(p_17, o_18, s, final_ctu))
    rule_12(oc_19, Literal(420008001, NS.xsd['int']), lambda r_34_m, c_35_m: rule_5_4(p_17, o_18, r_34_m, final_ctu))

def rule_5_4(p_17, o_18, oc_19, final_ctu):
    data.find(o_18, Iri('http://hl7.org/fhir/country'), ANY, lambda s, p, o: rule_5_5(p_17, s, oc_19, o, final_ctu))

def rule_5_5(p_17, o_18, oc_19, country_20, final_ctu):
    data.find(Iri('http://example.org/zika#world'), Iri('http://example.org/zika#hasZikaArea'), country_20, lambda s, p, o: final_ctu(p_17))
    rule_6(country_20, lambda country_21_m: final_ctu(p_17))

def rule_6(country_21, final_ctu):
    list_in(country_21, Collection([Literal('American Samoa', NS.xsd['string']), Literal('Angola', NS.xsd['string']), Literal('Anguilla', NS.xsd['string']), Literal('Antigua and Barbuda', NS.xsd['string']), Literal('Argentina', NS.xsd['string']), Literal('Aruba', NS.xsd['string']), Literal('Bahamas', NS.xsd['string']), Literal('Bangladesh', NS.xsd['string']), Literal('Barbados', NS.xsd['string']), Literal('Belize', NS.xsd['string']), Literal('Bolivia', NS.xsd['string']), Literal('Bonaire', NS.xsd['string']), Literal('Brazil', NS.xsd['string']), Literal('British Virgin Islands', NS.xsd['string']), Literal('Burkina Faso', NS.xsd['string']), Literal('Burma', NS.xsd['string']), Literal('Burundi', NS.xsd['string']), Literal('Cambodia', NS.xsd['string']), Literal('Cameroon', NS.xsd['string']), Literal('Cape Verde', NS.xsd['string']), Literal('Cayman Islands', NS.xsd['string']), Literal('Central African Republic', NS.xsd['string']), Literal('Colombia', NS.xsd['string']), Literal('Cook Islands', NS.xsd['string']), Literal('Costa Rica', NS.xsd['string']), Literal('Cuba', NS.xsd['string']), Literal('Curacao', NS.xsd['string']), Literal('Dominica', NS.xsd['string']), Literal('Dominican Republic', NS.xsd['string']), Literal('Easter Island', NS.xsd['string']), Literal('Ecuador', NS.xsd['string']), Literal('El Salvador', NS.xsd['string']), Literal('Ethiopia', NS.xsd['string']), Literal('Federated States of Micronesia', NS.xsd['string']), Literal('Fiji', NS.xsd['string']), Literal('France', NS.xsd['string']), Literal('French Guiana', NS.xsd['string']), Literal('French Polynesia', NS.xsd['string']), Literal('Gabon', NS.xsd['string']), Literal('Grenada', NS.xsd['string']), Literal('Guadeloupe', NS.xsd['string']), Literal('Guatemala', NS.xsd['string']), Literal('Guinea-Bissau', NS.xsd['string']), Literal('Guyana', NS.xsd['string']), Literal('Haiti', NS.xsd['string']), Literal('Honduras', NS.xsd['string']), Literal('India', NS.xsd['string']), Literal('Indonesia', NS.xsd['string']), Literal('Ivory Coast', NS.xsd['string']), Literal('Jamaica', NS.xsd['string']), Literal('Kenya', NS.xsd['string']), Literal('Kiribati', NS.xsd['string']), Literal('Laos', NS.xsd['string']), Literal('Malaysia', NS.xsd['string']), Literal('Maldives', NS.xsd['string']), Literal('Marshall Islands', NS.xsd['string']), Literal('Martinique', NS.xsd['string']), Literal('Mexico', NS.xsd['string']), Literal('Montserrat', NS.xsd['string']), Literal('New Caledonia', NS.xsd['string']), Literal('Nicaragua', NS.xsd['string']), Literal('Nigeria', NS.xsd['string']), Literal('Palau', NS.xsd['string']), Literal('Panama', NS.xsd['string']), Literal('Papua New Guinea', NS.xsd['string']), Literal('Paraguay', NS.xsd['string']), Literal('Peru', NS.xsd['string']), Literal('Philippines', NS.xsd['string']), Literal('Puerto Rico', NS.xsd['string']), Literal('Saba', NS.xsd['string']), Literal('Saint Barthelemy', NS.xsd['string']), Literal('Saint Kitts and Nevis', NS.xsd['string']), Literal('Saint Lucia', NS.xsd['string']), Literal('Saint Martin', NS.xsd['string']), Literal('Saint Vincent and the Grenadines', NS.xsd['string']), Literal('Samoa', NS.xsd['string']), Literal('Senegal', NS.xsd['string']), Literal('Singapore', NS.xsd['string']), Literal('Sint Eustatius', NS.xsd['string']), Literal('Sint Maarten', NS.xsd['string']), Literal('Solomon Islands', NS.xsd['string']), Literal('Suriname', NS.xsd['string']), Literal('Thailand', NS.xsd['string']), Literal('Tonga', NS.xsd['string']), Literal('Trinidad and Tobago', NS.xsd['string']), Literal('Turks and Caicos', NS.xsd['string']), Literal('Uganda', NS.xsd['string']), Literal('United States (Continental US)', NS.xsd['string']), Literal('United States Virgin Islands', NS.xsd['string']), Literal('Vanuatu', NS.xsd['string']), Literal('Venezuela', NS.xsd['string']), Literal('Vietnam', NS.xsd['string'])]), lambda s, o: final_ctu(s))

def rule_7(p_22, final_ctu):
    data.find(p_22, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s, p, o: rule_7_1(s, final_ctu))

def rule_7_1(p_22, final_ctu):
    data.find(p_22, Iri('http://hl7.org/fhir/address'), ANY, lambda s, p, o: rule_7_2(s, o, final_ctu))

def rule_7_2(p_22, pa_23, final_ctu):
    data.find(pa_23, Iri('http://hl7.org/fhir/country'), ANY, lambda s, p, o: rule_7_3(p_22, s, o, final_ctu))

def rule_7_3(p_22, pa_23, country_24, final_ctu):
    data.find(Iri('http://example.org/zika#world'), Iri('http://example.org/zika#hasZikaArea'), country_24, lambda s, p, o: final_ctu(p_22))
    rule_6(country_24, lambda country_21_m: final_ctu(p_22))

def rule_8(p_25, final_ctu):
    data.find(p_25, Iri('http://example.org/zika#recentTravelToZikaArea'), Literal(True, NS.xsd['boolean']), lambda s, p, o: final_ctu(s))
    rule_5(p_25, lambda p_17_m: final_ctu(p_17_m))

def rule_9(p_26, final_ctu):
    data.find(p_26, Iri('http://example.org/zika#residentOfZikaArea'), Literal(True, NS.xsd['boolean']), lambda s, p, o: final_ctu(s))
    rule_7(p_26, lambda p_22_m: final_ctu(p_22_m))

def rule_10(p_27, final_ctu):
    data.find(p_27, Iri('http://example.org/utils#hasObservation'), ANY, lambda s, p, o: rule_10_1(s, o, final_ctu))
    rule_14(p_27, ANY, lambda p_39_m, o_40_m: rule_10_1(p_39_m, o_40_m, final_ctu))

def rule_10_1(p_27, o_28, final_ctu):
    data.find(o_28, Iri('http://hl7.org/fhir/code'), ANY, lambda s, p, o: rule_10_2(p_27, s, o, final_ctu))

def rule_10_2(p_27, o_28, ocode_29, final_ctu):
    data.find(ocode_29, Iri('http://example.org/utils#hasCodeValue'), Literal(225517006, NS.xsd['int']), lambda s, p, o: rule_10_3(p_27, o_28, s, final_ctu))
    rule_12(ocode_29, Literal(225517006, NS.xsd['int']), lambda r_34_m, c_35_m: rule_10_3(p_27, o_28, r_34_m, final_ctu))

def rule_10_3(p_27, o_28, ocode_29, final_ctu):
    data.find(ANY, Iri('http://example.org/utils#referredBy'), o_28, lambda s, p, o: rule_10_4(p_27, o, ocode_29, s, final_ctu))
    rule_15(ANY, o_28, lambda p_41_m, r_42_m: rule_10_4(p_27, r_42_m, ocode_29, p_41_m, final_ctu))

def rule_10_4(p_27, o_28, ocode_29, p2_30, final_ctu):
    data.find(p2_30, Iri('http://example.org/zika#atZikaRiskDueToGeography'), Literal(True, NS.xsd['boolean']), lambda s, p, o: final_ctu(p_27))
    rule_8(p2_30, lambda p_25_m: final_ctu(p_27))
    rule_9(p2_30, lambda p_26_m: final_ctu(p_27))

def rule_11(p_31, r_32, final_ctu):
    data.find(p_31, Iri('http://hl7.org/fhir/id'), ANY, lambda s, p, o: rule_11_1(s, r_32, o, final_ctu))

def rule_11_1(p_31, r_32, id_33, final_ctu):
    data.find(r_32, Iri('http://hl7.org/fhir/subject'), id_33, lambda s, p, o: final_ctu(p_31, s))

def rule_12(r_34, c_35, final_ctu):
    data.find(r_34, Iri('http://hl7.org/fhir/coding'), ANY, lambda s, p, o: rule_12_1(s, c_35, o, final_ctu))

def rule_12_1(r_34, c_35, cod_36, final_ctu):
    data.find(cod_36, Iri('http://hl7.org/fhir/code'), c_35, lambda s, p, o: final_ctu(r_34, o))

def rule_13(p_37, c_38, final_ctu):
    data.find(p_37, Iri('http://example.org/utils#has'), c_38, lambda s, p, o: rule_13_1(s, o, final_ctu))
    rule_11(p_37, c_38, lambda p_31_m, r_32_m: rule_13_1(p_31_m, r_32_m, final_ctu))

def rule_13_1(p_37, c_38, final_ctu):
    data.find(c_38, NS.rdf['type'], Iri('http://hl7.org/fhir/Condition'), lambda s, p, o: final_ctu(p_37, s))

def rule_14(p_39, o_40, final_ctu):
    data.find(p_39, Iri('http://example.org/utils#has'), o_40, lambda s, p, o: rule_14_1(s, o, final_ctu))
    rule_11(p_39, o_40, lambda p_31_m, r_32_m: rule_14_1(p_31_m, r_32_m, final_ctu))

def rule_14_1(p_39, o_40, final_ctu):
    data.find(o_40, NS.rdf['type'], Iri('http://hl7.org/fhir/Observation'), lambda s, p, o: final_ctu(p_39, s))

def rule_15(p_41, r_42, final_ctu):
    data.find(p_41, Iri('http://hl7.org/fhir/id'), ANY, lambda s, p, o: rule_15_1(s, r_42, o, final_ctu))

def rule_15_1(p_41, r_42, id_43, final_ctu):
    data.find(r_42, Iri('http://hl7.org/fhir/value'), id_43, lambda s, p, o: final_ctu(p_41, s))
    
start = timer()
query(ANY, lambda x_0: emit(Triple(Var('x_0'), Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean'])), {'x_0': x_0}))
end = timer()
print("reason:", end-start)