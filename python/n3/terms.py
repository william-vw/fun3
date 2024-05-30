from enum import Enum
from .model import Model

class term_types(Enum):
    IRI = 0
    LITERAL = 1
    VAR = 2


class Iri:
    
    # pname: debugging
    def __init__(self, iri, label=False):
        self.iri = iri
        self.label = label
        
    def __str__(self):
        return f"<{self.iri}>" if not self.label else self.iri
    def __repr__(self):
        return self.__str__()
        
class Literal:
    
    def __init__(self, value):
        self.value = value
        
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
        
    def __str__(self):
        match self.type:
            case var_types.UNIVERSAL:
                return f"?{self.name}"
            case _:
                return f"_:{self.name}"             
        return self.name
    def __repr__(self):
        return self.__str__()
    

class Triple:
    
    # s, p, o
    
    def __init__(self, s=None, p=None, o=None):
        self.s = s
        self.p = p
        self.o = o
        
        self.__cnt = 0
        
    def __iter__(self):
        return self

    def __next__(self):
        cnt = self.__cnt
        self.__cnt += 1
        
        match cnt:
            case 0: return self.s
            case 1: return self.p
            case 2: return self.o
            case _: raise StopIteration
        
    def __str__(self):
        return f"{self.s} {self.p} {self.o} ."
    def __repr__(self):
        return self.__str__()
    
    
class GraphTerm:
    
    def __init__(self, model=None):
        self.model = model if model is not None else Model()
        
    def __str__(self):
        return "{"  + "".join([ str(t) for t in self.model.triples ]) + "}"
    def __repr__(self):
        return self.__str__()