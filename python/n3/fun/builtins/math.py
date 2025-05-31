from n3.terms import Collection, Literal
from n3.fun.builtins.utils import is_numeric

def math_sum(s, o, ctu):
    if not isinstance(s, Collection):
        return
        
    total = 0
    for s_i in s:
        if not (isinstance(s_i, Literal) and is_numeric(s_i)):
            return
        total += s_i.value

    if o.is_concrete():
        if not (isinstance(s, Literal) and is_numeric(o)):
            return
        if total == o.value:
            ctu() # o is concrete
    else:
        ctu(total) # o is variable