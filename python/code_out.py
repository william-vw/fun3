from n3.parse import parse_n3
from n3.objects import Iri, Var, Literal, Collection, ANY, Terms, Triple
from n3.ns import NS
data = parse_n3('@prefix : <http://example.org/> . \n:will a :Person ; :address :addr1 . :addr1 :country "CA" .\n:ed :ability :think ; :address :addr1 ; :describedAs :Person .\n:el :ability :drink ; :address :addr1 ; :describedAs :Belgian .\n:dor :ability :think ; :address :addr1 ; :describedAs :German .\n:soc :name "Socrates" ; :address :addr1 .\n').data

def query(x, final_ctu):
    data.find(x, NS.rdf['type'], Iri('http://example.org/Canadian'), lambda s, p, o: final_ctu(s))
    rule_0(x, lambda p_0: final_ctu(p_0))

def rule_0(p_0, final_ctu):
    data.find(p_0, NS.rdf['type'], Iri('http://example.org/Person'), lambda s, p, o: rule_0_1(s, final_ctu))
    rule_1(p_0, lambda p_1: rule_0_1(p_1, final_ctu))

def rule_0_1(p_0, final_ctu):
    data.find(p_0, Iri('http://example.org/address'), ANY, lambda s, p, o: rule_0_2(s, o, final_ctu))

def rule_0_2(p_0, a, final_ctu):
    data.find(a, Iri('http://example.org/country'), Literal('CA', NS.xsd['string']), lambda s, p, o: final_ctu(p_0))

def rule_1(p_1, final_ctu):
    data.find(p_1, Iri('http://example.org/ability'), Iri('http://example.org/think'), lambda s, p, o: final_ctu(s))
query(ANY, lambda x: print(Triple(Var('x'), NS.rdf['type'], Iri('http://example.org/Canadian')).instantiate({'x': x})))