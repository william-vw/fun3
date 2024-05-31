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