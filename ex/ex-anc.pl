ancestor(D, A) :- parent(D, P), ancestor(P, A).
ancestor(D, D) :- true .

parent(c, b) .
parent(b, a) .

# query:
# ancestor(D, A) .