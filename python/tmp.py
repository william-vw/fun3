from n3.terms import Iri, Var, Literal

def rule_0(p, model, state, ctu):
    model.find(p, Iri('a'), Iri(':Person'), state, lambda t, state: rule_2(t.s, model, state, ctu))

def rule_1(p, model, state, ctu):
    model.find(p, Iri(':address'), a, state, lambda t, state: rule_3(t.s, t.o, model, state, ctu))

def rule_2(p, a, model, state, ctu):
    model.find(a, Iri(':country'), Literal('"CA"'), state, lambda t, state: ctu(p, state))