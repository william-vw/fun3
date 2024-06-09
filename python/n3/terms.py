from enum import Enum
import string, random
from n3.model import Model

class term_types(Enum):
    IRI = 0
    LITERAL = 1
    COLLECTION = 2
    GRAPH = 3
    VAR = 4
    BNODE = 5


class Iri:

    # iri
    
    def __init__(self, iri):
        self.iri = iri
        
    def type(self):
        return term_types.IRI
    
    def is_concrete(self):
        return True
    
    def idx_val(self):
        return self.iri
    
    @staticmethod
    def get_ns(iri):
        return iri[0:Iri.__sep_idx(iri)+1]
    
    @staticmethod
    def get_ln(iri):
        return iri[Iri.__sep_idx(iri)+1:]
    
    @staticmethod
    def __sep_idx(iri):
        return iri.rfind('#') if '#' in iri else iri.rfind('/')
    
    def __getattr__(self, name):
        match name:
            case 'ns': return Iri.get_ns(self.iri)
            case 'ln': return Iri.get_ln(self.iri)
            case _: raise AttributeError(f"unknown attribute: {name}")
            
    def __eq__(self, other): 
        if not isinstance(other, Iri):
            return NotImplemented
        return self.iri == other.iri
        
    def __str__(self):
        return f"<{self.iri}>"
    def __repr__(self):
        return self.__str__()
        
        
class Literal:
    
    def __init__(self, value, dt=None, lng=None):
        self.value = value
        self.dt = dt
        self.lng = lng
        
    def type(self):
        return term_types.LITERAL
    
    def is_concrete(self):
        return True
    
    def idx_val(self):
        return self.value
        
    def __eq__(self, other): 
        if not isinstance(other, Literal):
            return NotImplemented
        return self.value == other.value
        
    def __str__(self):
        value = self.value; suffix = None
        if isinstance(self.value, str):
            quote = "\"" if "\n" not in self.value else "\"\"\""
            value = quote + value + quote
            if self.lng is not None:
                suffix = f"@{self.lng}"
            elif self.dt is not None:
                suffix = f"^^{self.dt}"
        return str(value) + (suffix if suffix is not None else "")
    def __repr__(self):
        return self.__str__()


class Collection:
    
    # __elements
    # __vars
    # __max_depth
    
    def __init__(self):
        self.__elements = []
        self.__vars = []
        self.__max_depth = 1
    
    def type(self):
        return term_types.COLLECTION
    
    def is_concrete(self):
        return True
    
    def idx_val(self):
        return self.__to_nested_tuples()
    
    def __to_nested_tuples(self):
        return tuple(e.__to_nested_tuples() if e.type() == term_types.COLLECTION else e for e in self.__elements)
    
    def _parsed_el(self, el):
        self.__elements.append(el)
        if el.type() == term_types.COLLECTION:
            self.__vars.extend(el.__vars)
            self.__max_depth += el.__max_depth
        
    def _parsed_var(self, var):
        self.__vars.append(var)
    
    def _vars(self):
        return self.__vars
    
    def _max_depth(self):
        return self.__max_depth
    
    def __iter__(self):
        return self.__elements.__iter__()
    
    def __eq__(self, other): 
        if not isinstance(other, Collection):
            return NotImplemented
        return self.__elements == other.__elements
        
    def __str__(self):
        return "( " + " ".join(str(e) for e in self.__elements) + " )"
    def __repr__(self):
        return self.__str__()


class Var:
    
    def __init__(self, name):
        self.name = name
        
    def type(self):
        return term_types.VAR
    
    def is_concrete(self):
        return False
    
    def idx_val(self):
        return self.name
        
    def __eq__(self, other): 
        if not isinstance(other, Var):
            return NotImplemented
        return self.name == other.name
        
    def __str__(self):
        return f"?{self.name}"
    def __repr__(self):
        return self.__str__()
    

class BlankNode:
        
    def __init__(self, label=None):
        if label is None:
            self.label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        else:
            self.label = label
        
    def type(self):
        return term_types.BNODE
    
    def is_concrete(self):
        return False
    
    def idx_val(self):
        return self.label
        
    def __eq__(self, other): 
        if not isinstance(other, BlankNode):
            return NotImplemented
        return self.label == other.label
        
    def __str__(self):
        return f"_:{self.label}"
    def __repr__(self):
        return self.__str__()
    

class Triple:
    
    # s, p, o
    
    def __init__(self, s=None, p=None, o=None):
        self.s = s
        self.p = p
        self.o = o
        
    def clone(self):
        return Triple(self.s, self.p, self.o)
    
    def has_graph(self):
        return any(r.type() == term_types.GRAPH for r in self)
    
    def __iter__(self):
        return TripleIt(self)
    
    def __getitem__(self, key):
        match key:
            case 0: return self.s
            case 1: return self.p
            case 2: return self.o
            case _: print("inconceivable!"); return None
    
    def __setitem__(self, key, value):
        match key:
            case 0: self.s = value
            case 1: self.p = value
            case 2: self.o = value
            case _: print("inconceivable!");
    
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
        
    def type(self):
        return term_types.GRAPH
        
    def __str__(self):
        return "{ "  + "".join([ str(t) for t in self.model.triples() ])[:-2] + " }"
    def __repr__(self):
        return self.__str__()