from n3.objects import Collection, Literal
from n3.fun.builtins.utils import is_numeric, xsd_num_type

def math_greaterThan(s, o, ctu):
    if not (isinstance(s, Literal) and is_numeric(s)) or \
        not (isinstance(o, Literal) and is_numeric(o)):
        return
    
    if s.value > o.value:
        ctu(s, o)
        
def math_lessThan(s, o, ctu):
    math_greaterThan(o, s, ctu)

def __math_op(s, o, op, ctu):
    if not isinstance(s, Collection):
        return
        
    total = None
    for s_i in s:
        if not (isinstance(s_i, Literal) and is_numeric(s_i)):
            return
        total = s_i.value if total is None else op(total, s_i.value)

    if o.is_concrete():
        if not (isinstance(o, Literal) and is_numeric(o)):
            return
        if total == o.value:
            ctu(s, o) # o is concrete
    else:
        # TODO proper type juggling
        ctu(s, Literal(total, xsd_num_type(total))) # o is variable
    
def math_sum(s, o, ctu):
    __math_op(s, o, lambda total, x: total + x, ctu)
    
def math_difference(s, o, ctu):
    __math_op(s, o, lambda total, x: total - x, ctu)
    
def math_product(s, o, ctu):
    __math_op(s, o, lambda total, x: total * x, ctu)
    
def math_quotient(s, o, ctu):
    __math_op(s, o, lambda total, x: total / x, ctu)