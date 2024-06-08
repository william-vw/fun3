from n3.terms import Iri, Var, Literal

def rule_0(desc, anc, data, state, ctu):
    data.find(desc, Iri('http://www.w3.org/2000/10/swap/log#notEqualTo'), anc, state, lambda t, state: rule_0_1(t.s, t.o, data, state, ctu))

def rule_0_1(desc, anc, data, state, ctu):
    data.find(desc, Iri('http://example.org/parent'), None, state, lambda t, state: rule_0_2(t.s, anc, t.o, data, state, ctu))

def rule_0_2(desc, anc, parent, data, state, ctu):
    data.find(parent, Iri('http://example.org/ancestor'), anc, state, lambda t, state: ctu(desc, t.o, state))
    rule_0(parent, anc, data, state, lambda parent, anc, state: ctu(desc, anc, state))
    rule_1(parent, anc, data, state, lambda parent, anc, state: ctu(desc, anc, state))

def rule_1(desc0, desc1, data, state, ctu):
    if desc0 is not None:
        if desc1 is not None:
            if desc0 == desc1:ctu(desc0, desc1)
            else:ctu(desc0, desc0)
    elif desc1 is not None:ctu(desc1, desc1)
