import pandas as pd

class Model:
    
    def __init__(self):
        self.__triples = []
        
    def add(self, triple):
        self.__triples.append(triple)
        
    def done(self):
        self.df = pd.DataFrame([ [ t[0].idx_val(), t[1].idx_val(), t[2].idx_val(), t ] for t in self.__triples if not t.has_graph() ], columns=list("spot"))
        # self.__triples = None
        
    def __len__(self):
        return len(self.__triples)
    
    def triple_at(self, i):
        return self.__triples[i]
    
    def triples(self):
        return self.__triples
    
    def find(self, s, p, o, ctu):
        # print("find - ", s, p, o)
        
        # for t in self.__triples:
        #     if state.stop: break
        #     if (s == None or t.s == s) and (p == None or t.p == p) and (o == None or t.o == o):
        #         # print("t -", t)
        #         ctu(t, state)
        
        needle = pd.Series([ True ] * len(self.df))
        if s is not None:
            needle &= self.df['s']==s.idx_val()
        if p is not None:
            needle &= self.df['p']==p.idx_val()
        if o is not None:
            needle &= self.df['o']==o.idx_val()
        
        # print("needle:", needle)
        for t in self.df.loc[needle, 't']:
            # if state.stop: break
            # print("t -", t)
            ctu(t.s, t.p, t.o)
        
    def __str__(self):
        return "\n".join([ str(t) for t in self.__triples ])
    def __repr__(self):
        return self.__str__()