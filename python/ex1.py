from n3.parse import parse_n3
from n3.terms import Iri, Var, Literal

class State : 
    def __init__(self, stop):
        self.stop = stop

def result_fn(*args):
    print(f"solution: { [ a for a in args[:-1] ] }")
    # state.stop = True

def rule_0(p, data, state, ctu):
    data.find(p, Iri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), Iri('http://example.org/Person'), state, lambda t, state: rule_0_1(t.s, data, state, ctu))
    rule_1(p, data, state, lambda p, state: rule_0_1(p, data, state, ctu))

def rule_0_1(p, data, state, ctu):
    data.find(p, Iri('http://example.org/address'), None, state, lambda t, state: rule_0_2(t.s, t.o, data, state, ctu))

def rule_0_2(p, a, data, state, ctu):
    data.find(a, Iri('http://example.org/country'), Literal('"CA"'), state, lambda t, state: ctu(p, state))

def rule_1(pe, data, state, ctu):
    data.find(pe, Iri('http://example.org/ability'), Iri('http://example.org/think'), state, lambda t, state: ctu(t.s, state))

def rule_2(pe, data, state, ctu):
    data.find(pe, Iri('http://example.org/ability'), Iri('http://example.org/drink'), state, lambda t, state: ctu(t.s, state))
    
def main():
    data = """@prefix : <http://example.org/> . 
:will a :Person ; :address :addr1 . :addr1 :country "CA" .
:ed :ability :think ; :address :addr1 ; :describedAs :Person .
:el :ability :drink ; :address :addr1 ; :describedAs :Belgian .
:dor :ability :think ; :address :addr2 ; :describedAs :German .
:soc :name "Socrates" ; :address :addr1 .
"""
    
    data = parse_n3(data).model
    print("data:\n", data, "\n")
    
    state = State(False)
    
    rule_0(None, data, state, result_fn)
    
if __name__ == "__main__":
    main()