from enum import Enum
from n3.model import Model

class term_types(Enum):
    IRI = 0
    LITERAL = 1
    VAR = 2


class Iri:
    
    # label: debugging
    def __init__(self, iri, label=False):
        self.iri = iri
        self.label = label
        
    def type(self):
        return term_types.IRI
        
    def __eq__(self, other): 
        if not isinstance(other, Iri):
            return NotImplemented
        return self.iri == other.iri
        
    def __str__(self):
        return f"<{self.iri}>" if not self.label else self.iri
    def __repr__(self):
        return self.__str__()
        
class Literal:
    
    def __init__(self, value):
        self.value = value
        
    def type(self):
        return term_types.LITERAL
        
    def __eq__(self, other): 
        if not isinstance(other, Literal):
            return NotImplemented
        return self.value == other.value
        
    def __str__(self):
        return self.value
    def __repr__(self):
        return self.__str__()


class var_types(Enum):
    UNIVERSAL = 0
    EXISTENTIAL = 1

class Var:
    
    def __init__(self, type, name):
        self.type = type
        self.name = name
        
    def type(self):
        return term_types.VAR
        
    def __eq__(self, other): 
        if not isinstance(other, Var):
            return NotImplemented
        return self.name == other.name
        
    def __str__(self):
        match self.type:
            case var_types.UNIVERSAL:
                return f"?{self.name}"
            case _:
                return f"_:{self.name}"
    def __repr__(self):
        return self.__str__()
    

class Triple:
    
    # s, p, o
    
    def __init__(self, s=None, p=None, o=None):
        self.s = s
        self.p = p
        self.o = o
        
    def __iter__(self):
        return TripleIt(self)
    
    def __str__(self):
        return f"{self.s} {self.p} {self.o} ."
    def __repr__(self):
        return self.__str__()
    
    
class TripleIt:
    
    def __init__(self, t):
        self.__t = t
        self.__cnt = 0
        
    def __iter__(self):
        return self

    def __next__(self):
        cnt = self.__cnt
        self.__cnt += 1
        
        match cnt:
            case 0: return self.__t.s
            case 1: return self.__t.p
            case 2: return self.__t.o
            case _: raise StopIteration
    
class GraphTerm:
    
    def __init__(self, model=None):
        self.model = model if model is not None else Model()
        
    def __str__(self):
        return "{"  + "".join([ str(t) for t in self.model.triples() ]) + "}"
    def __repr__(self):
        return self.__str__()