import sys
sys.path.insert(0, "../") # noqa
import sys
from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit, emitted

data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-bench/zika/data/gen100_pt2.n3').data

# rule_0 (id_1=x_0) > rule_1 (p_3=ANY) [RULE - ret: p_3_m=? ... s_2]
#   > (exec) data.find(p_3,rdf:type,fhir:Patient) (ret: s_1,p_1,o_1) > rule_1_1 (p_4=s_1) > (exec) data.find(p_4,fhir:hasCondition,ANY) (s_2,p_2,o_2; FINAL=s_2)
# > rule_0_1 (id_1=id_1,p_2=p_3_m) > (exec) data.find(p_2,fhir:id,id_1) (ret: s_3,p_3,o_3) > FINAL=o_3

# for s_1,p_1,o_1 in data.find(ANY,rdf:type,fhir:Patient):
#   for s_2, p_2, o_2 in data.find(s_1,fhir:hasCondition,ANY):
#       for s_3, p_3, o_3 in data.find(s_2,fhir:id,x_0):
#           yield o_3

def query(x_0, final_ctu):
    rule_0(x_0, lambda id_1_m: final_ctu(id_1_m))

def rule_0(id_1, final_ctu):
    # data.find(ANY, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s1, p1, o1: rule_0_1(id_1, s1, final_ctu))
    rule_1(ANY, lambda p_3_m: rule_0_1(id_1, p_3_m, final_ctu))

def rule_0_1(id_1, p_2, final_ctu):
    data.find(p_2, Iri('http://hl7.org/fhir/id'), id_1, lambda s2, p2, o2: final_ctu(o2))

def rule_1(p_3, final_ctu):
    # data.find(p_3, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s3, p3, o3: final_ctu(s3))
    data.find(p_3, NS.rdf['type'], Iri('http://hl7.org/fhir/Patient'), lambda s3, p3, o3: rule_1_1(s3, final_ctu))

def rule_1_1(p_4, final_ctu):
    data.find(p_4, Iri('http://example.org/utils#hasCondition'), ANY, lambda s4, p4, o4: final_ctu(s4))

query(ANY, lambda x_0: emit(Triple(Var('x_0'), Iri('http://example.org/zika#testForZika'), Literal(True, NS.xsd['boolean'])), {'x_0': x_0}))

for t in emitted:
    print(t)