from n3.parse import parse_n3
from n3.terms import Iri, Var, Literal, Collection, ANY, term_types
data = parse_n3('@prefix : <http://example.org/> . \n:will a :Person ; :address :addr1 . :addr1 :country "CA" .\n:ed :ability :think ; :address :addr1 ; :describedAs :Person .\n:el :ability :drink ; :address :addr1 ; :describedAs :Belgian .\n:dor :ability :think ; :address :addr1 ; :describedAs :German .\n:soc :name "Socrates" ; :address :addr1 .\n').data

def rule_0(p_0, final_ctu):
    data.find(p_0, Iri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), Iri('http://example.org/Person'), lambda s, p, o: rule_0_1(s, final_ctu))
    rule_1(p_0, lambda p_2: rule_0_1(p_2, final_ctu))

def rule_0_1(p_0, final_ctu):
    data.find(p_0, Iri('http://example.org/address'), ANY, lambda s, p, o: rule_0_2(s, o, final_ctu))

def rule_0_2(p_0, a_1, final_ctu):
    data.find(a_1, Iri('http://example.org/country'), Literal('CA'), lambda s, p, o: final_ctu(p_0))

def rule_1(p_2, final_ctu):
    data.find(p_2, Iri('http://example.org/ability'), Iri('http://example.org/think'), lambda s, p, o: final_ctu(s))

def rule_2(pe_3, final_ctu):
    data.find(pe_3, Iri('http://example.org/ability'), Iri('http://example.org/drink'), lambda s, p, o: final_ctu(s))
rule_0(ANY, lambda a0: print(a0))