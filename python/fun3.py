from ast import dump, unparse
import ast
from types import CodeType, FunctionType

from n3.parse import parse_n3
from n3.fun.gen import gen_py

from n3.terms import Iri, Literal, Var
from n3.model import Model

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
    
    # # test
    
    # state = State(False)
    
    # rule_fn(None, model, state, result)
    
    
def unparse_with_lineno(ast):
    code = unparse(ast)
    return "\n".join([ f"{i+1}. {line}" for i, line in enumerate(code.split("\n")) ])

def compile_py(mod):    
    mod_code = compile(mod, "<fun3>", "exec")
    
    exec(mod_code)
    
    # return first function or whatever
    for c in mod_code.co_consts:
        if isinstance(c, CodeType) and c.co_name == "rule_0":
            return FunctionType(c, {})

    
def print_ast():
    mod_code = """
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
        print("find", s, p, o)
        
        for t in self.__triples:
            print(t.s, t.p, t.o)
            
            if state.stop: # TODO
                return
            
            if (s == None or t.s == s) and (p == None or t.p == p) and (o == None or t.o == o):
                print("found", t)
                ctu(t, state)"""
    
    print(dump(ast.parse(mod_code), indent=4))
    

if __name__ == "__main__":
    fun3()
    # print_ast()