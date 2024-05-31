from ast import dump, unparse
import ast
from types import CodeType, FunctionType

from n3.terms import Iri, Literal, Var
from n3.parse import parse_n3
from n3.fun.gen import gen_py

class State : 
    def __init__(self, stop):
        self.stop = stop

def result(p, state):
    print(f"solution: {p}")
    # state.stop = True


def fun3():    
    # (?x, a, Cool) :- (?x, name, "will")
    # rules =  """@prefix : <http://example.org/> . 
# { ?x a :Cool } <= { ?x :name \"will\" } . """
    
    # (?p, type, Canadian) :-
    #   (?p, type, Person), (?p, address, ?a), (?a, country, "CA")
    rules =  """@prefix : <http://example.org/> . 
{ ?p a :Canadian } <= { ?p a :Person . ?p :address ?a . ?a :country "CA" } . """
    
    data = """@prefix : <http://example.org/> . 
:will a :Person . :will :address :addr1 . :addr1 :country "CA" ."""
    
    # parse
    
    result = parse_n3(rules)
    # print(result.model)
    print(result.rules)
    
    model = parse_n3(data).model
    print(model)
    
    print()
    
    # generate
    
    mod = gen_py(result.rules)
    # print(dump(mod, indent=4))
    print(unparse_with_lineno(mod))
    
    print()
    
    # compile
    
    rule_fn = compile_py(mod)
    print(rule_fn)
    
    print()
    
    # test
    
    state = State(False)
    
    rule_fn(None, model, state, result)
    
    
def unparse_with_lineno(ast):
    code = unparse(ast)
    return "\n".join([ f"{i+1}. {line}" for i, line in enumerate(code.split("\n")) ])

def compile_py(mod):    
    mod_code = compile(mod, "<fun3>", "exec")
    
    # return first function or whatever
    for c in mod_code.co_consts:
        if isinstance(c, CodeType) and c.co_name == "rule_0":
            return FunctionType(c, {})

if __name__ == "__main__":
    fun3()
    # print_ast()


    
def print_ast():
    
    mod_code = """class Iri:
    
    # label: debugging
    def __init__(self, iri, label=False):
        self.iri = iri
        self.label = label
        
    def type(self):
        return term_types.IRI
        
    def __str__(self):
        return f"<{self.iri}>" if not self.label else self.iri
    def __repr__(self):
        return self.__str__()
        
class Literal:
    
    def __init__(self, value):
        self.value = value
        
    def type(self):
        return term_types.LITERAL
        
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
        
    def __str__(self):
        match self.type:
            case var_types.UNIVERSAL:
                return f"?{self.name}"
            case _:
                return f"_:{self.name}"
    
    def __repr__(self):
        return self.__str__()"""
    
    print(dump(ast.parse(mod_code), indent=4))