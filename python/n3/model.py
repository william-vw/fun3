class Model:
    
    def __init__(self):
        self.__triples = []
        
    def add(self, triple):
        self.__triples.append(triple)
        
    def len(self):
        return len(self.__triples)
    
    def triple_at(self, i):
        return self.__triples[i]
    
    def triples(self):
        return self.__triples
    
    def find(self, s, p, o, state, ctu):
        # print("find - ", s, p, o)
        
        for t in self.__triples:
            
            if state.stop: # TODO
                return
            
            if (s == None or t.s == s) and (p == None or t.p == p) and (o == None or t.o == o):
                # print("t -", t)
                ctu(t, state)
        
    def __str__(self):
        return "\n".join([ str(t) for t in self.__triples ])
    def __repr__(self):
        return self.__str__()