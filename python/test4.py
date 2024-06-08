from n3.terms import Iri
from n3.model import Model
from n3.parse import parse_n3

class State : 
    def __init__(self, stop):
        self.stop = stop

def result_fn(d, a, state):
    print(f"solution: {d} {a}")
    # state.stop = True
            
# { :will :aliasNames ( ?xn ?yn ) } <= { :wil :alias ( ?x ?y :elb ) . ?x :name ?xn . ?y :name ?yn } .

def rule_0_unify_lists(xn, yn, head_values, data_list, data, state, ctu):
    if head_values[0] == data_list[2].idx_val():
        (x, y, _) = data_list
        rule_0_1(xn, yn, x.idx_val(), y.idx_val(), data, state, ctu)

def rule_0(xn, yn, data, state, ctu):
    data.find('http://example.org/wil', 'http://example.org/alias', None, state, lambda t, state: rule_0_unify_lists(xn, yn, ('http://example.org/elb',), t.o.idx_val(), data, state, ctu))

def rule_0_1(xn, yn, x, y, data, state, ctu):
    data.find(x, 'http://example.org/name', xn, state, lambda t, state: rule_0_2(t.o.idx_val(), yn, t.s.idx_val(), y, data, state, ctu))

def rule_0_2(xn, yn, x, y, data, state, ctu):
    data.find(y, 'http://example.org/name', yn, state, lambda t, state: ctu(xn, t.o.idx_val(), state))

            
def main():
    data = """@prefix : <http://example.org/> . 
:wil :alias ( :wil :edw :elb ) . :wil :name "wil" . :edw :name "edward" . :elb :name "elbert" .
"""
    data = parse_n3(data).data
    print("model:\n", data, "\n")
    
    rule_0(None, None, data, State(False), result_fn)
    

if __name__ == "__main__":
    main()