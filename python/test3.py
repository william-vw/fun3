from n3.terms import Iri
from n3.model import Model
from n3.parse import parse_n3

class State : 
    def __init__(self, stop):
        self.stop = stop

def result_fn(d, a, state):
    print(f"solution: {d} {a}")
    # state.stop = True
            
from n3.terms import Iri, Var, Literal

def rule_0(desc, anc, data, state, ctu):
    # print("rule_0", desc, anc)
    data.find(desc, Iri('http://example.org/parent'), None, state, lambda t, state: rule_0_1(t.s, anc, t.o, data, state, ctu))

def rule_0_1(desc, anc, parent, data, state, ctu):
    # print("rule_0_1", desc, anc, parent)
    data.find(parent, Iri('http://example.org/ancestor'), anc, state, lambda t, state: ctu(desc, t.o, state))
    rule_0(parent, anc, data, state, lambda parent, anc, state: ctu(desc, anc, state))
    rule_1(parent, anc, data, state, lambda parent, anc, state: ctu(desc, anc, state))

def rule_1(desc0, desc1, data, state, ctu):
    # print("rule_1", desc0, desc1)
    if desc0 is not None:
        if desc1 is not None:
            if desc0 == desc1:ctu(desc0, desc1, state)
        else:ctu(desc0, desc0, state)
    elif desc1 is not None:ctu(desc1, desc1, state)

# def rule_1(desc0, desc1, data, state, ctu):
#     print("rule_1", desc0, desc1)

#     if desc0 is not None:
#         if desc1 is None:
#             ctu(desc0, desc0, state)
#     elif desc0 is None:
#         if desc1 is not None:
#             ctu(desc1, desc1, state)
#     elif desc0 is not None and desc1 is not None:
#         if desc0 == desc1:
#             ctu(desc0, desc1, state)
            
            
def main():
    data = """@prefix : <http://example.org/> . 
:c :parent :b . :b :parent :a .
"""
    data = parse_n3(data).model
    print("model:\n", data, "\n")
    
    rule_0(None, None, data, State(False), result_fn)
    

if __name__ == "__main__":
    main()