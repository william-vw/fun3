from n3.parse import parse_n3
from n3.terms import Iri, Var, Literal, Collection, ANY, term_types
data = parse_n3('@prefix : <http://example.org/> . \n:robocop :hasParts ( :man :man ).\n:man :label "man" . :machine :label "machine" .\n').data

def rule_0(a_0, x_1, xl_2, final_ctu):
    data.find(a_0, Iri('http://example.org/parts'), Collection([x_1, x_1]), lambda s, p, o: rule_0_1(s, o[1], xl_2, final_ctu) if o[0] == o[1] else False)
    rule_1(a_0, x_1, x_1, lambda q_3, k_4, l_5: rule_0_1(q_3, l_5, xl_2, final_ctu) if k_4 == l_5 else False)

def rule_0_1(a_0, x_1, xl_2, final_ctu):
    data.find(x_1, Iri('http://example.org/label'), xl_2, lambda s, p, o: final_ctu(a_0, s, o))

def rule_1(q_3, k_4, l_5, final_ctu):
    data.find(q_3, Iri('http://example.org/hasParts'), Collection([k_4, l_5]), lambda s, p, o: final_ctu(s, o[0], o[1]))
rule_0(ANY, ANY, ANY, lambda a0, a1, a2: print(a0, a1, a2))