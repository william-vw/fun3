class Model:
    
    def __init__(self):
        self.triples = []
        
    def add(self, triple):
        self.triples.append(triple)
        
    def __str__(self):
        return "\n".join([ str(t) for t in self.triples ])
    def __repr__(self):
        return self.__str__()