class State : 
    
    def __init__(self, stop):
        self.stop = stop

class Store :

    def __init__(self, triples):
        self.triples = triples
        
    def find(self, s, p, o, state, ctu):
        for t in self.triples:
            if state.stop:
                return
            
            if (s == None or t.s == s) and (p == None or t.p == p) and (o == None or t.o == o):
                ctu(t, state)
        
class Triple :
    
    def __init__(self, s, p, o):
        self.s = s
        self.p = p
        self.o = o
        
    def __str__(self):
        return f"{self.s} {self.p} {self.o}"

# # - ex 1

# def result(p, a, state):
#     print(f"solution: {p} {a}")
#     # state.stop = True
    
# # (?p, type, Person) :-
# #   (?p, ability, think) .

# def r1(p, store, state, ctu):
#     store.find(p, "ability", "think", state, lambda t, state: ctu(t.s, state) )
    
# # (?p, type, Person) :-
# #   (?p, name, "Socrates") .

# def r2(p, store, state, ctu):
#     store.find(p, "name", "\"Socrates\"", state, lambda t, state: ctu(t.s, state))
    
# # (?p, type, :Canadian) :-
# #   (?p, type, Person), (?p, address, ?a), (?a, country, "CA")

# def r3(p, store, state, ctu):
#     store.find(p, "type", "Person", state, lambda t, state: r3_cl2(t.s, store, state, ctu))
#     if not state.stop:
#         r1(p, store, state, lambda p, state: r3_cl2(p, store, state, ctu))
#     if not state.stop:
#         r2(p, store, state, lambda p, state: r3_cl2(p, store, state, ctu))

# def r3_cl2(p, store, state, ctu):
#     store.find(p, "address", None, state, lambda t, state: r3_cl3(p, t.o, store, state, ctu))

# def r3_cl3(p, a, store, state, ctu):
#     store.find(a, "country", "\"CA\"", state, lambda _, state: ctu(p, a, state))
    
    
# - ex 2

def result(desc, anc, state):
    print(f"solution: {desc} {anc}")
    # state.stop = true

# (?desc ancestor ?anc) :-
#     (?desc parent ?parent)
#     (?parent ancestor ?anc)

# (?desc ancestor ?desc) :- cut .

# (c parent b)
# (b parent a)

def r1(desc_0, anc_0, desc, anc, store, state, ctu):
    print(f"r1 {desc_0} {anc_0} {desc} {anc}")
    store.find(desc, "parent", None, state, lambda t, state: r1_cl2((desc_0 if desc_0 != None else t.s), anc_0, t.o, anc, store, state, ctu))

def r1_cl2(desc_0, anc_0, parent, anc, store, state, ctu):
    print("r1_cl2 {desc_0} {anc_0} {parent} {anc}")
    
    r1(desc_0, anc_0, parent, anc, store, state, ctu)
    
    if not state.stop:
        if anc_0 != None:
            if parent == anc_0:
                ctu(desc_0, parent, state)
                # return # cut
        else:
            ctu(desc_0, parent, state)

def main():
    state = State(False)
    
    # # - ex1
    
    # store = Store([ 
    #     Triple( s="ed", p="type", o="Person" ),
    #     Triple( s="will", p="ability", o="think" ),
    #     Triple( s="soc", p="name", o="\"Socrates\"" ),
    
    #     Triple( s="ed", p="address", o="addr1" ),
    #     Triple( s="will", p="address", o="addr2" ),
    #     Triple( s="soc", p="address", o="addr3" ),
    
    #     Triple( s="addr1", p="country", o="\"BE\"" ),
    #     Triple( s="addr2", p="country", o="\"CA\"" ),
    #     Triple( s="addr3", p="country", o="\"CA\"" )
    # ])
    
    # # r3(None, store, state, result)
    # r3("will", store, state, result)
    
    # - ex 2
    
    store = Store([
        Triple( s="c", p="parent", o="b" ),
        Triple( s="b", p="parent", o="a" ),
    ])
    
    # r1("c", "a", "c", "a", store, state, result)
    r1(None, None, None, None, store, state, result)

if __name__ == "__main__":
    main()
