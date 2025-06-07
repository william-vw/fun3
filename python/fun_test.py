from ast import dump, unparse, parse
from collections import Counter
from multidict import MultiDict

from n3.parse import parse_n3
from n3.fun.gen import gen_py, InputData, QueryFn
from n3.objects import Triple, Iri, Collection, ANY, Literal
from n3.model import Model
from n3.ns import xsdNs
from python.n3.to_py import run_py, save_py
  
  
def fun3():
    
# - input

    rules_str = """@prefix : <http://example.org/> . 
..."""

    query_str = """@prefix : <http://example.org/> .
...
"""

    data_str = """@prefix : <http://example.org/> . 
...
"""

    # # 1/ save code
    save_py(query_str, rules_str, data_str, "code_out.py")
    
    # 2/ run a rule fn
    # print(run_py(query_str, rules_str, data_str))
    
    
def test_ast():
    print(dump(parse("""a = 'abc'""")))
    
if __name__ == "__main__":
    fun3()
    # test_ast()