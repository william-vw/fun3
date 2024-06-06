from n3.terms import Iri

class NS:
    
    # iri
    
    def __init__(self, iri):
        self.iri = iri
        
    def __getitem__(self, key):
        return Iri(self.iri + key)
    
swapNs = NS("http://www.w3.org/2000/10/swap/")
n3Log = NS("http://www.w3.org/2000/10/swap/log#")
rdf = NS("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
owl = NS("http://www.w3.org/2002/07/owl#")