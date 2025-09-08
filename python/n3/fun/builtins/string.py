from n3.objects import Collection, Literal
from n3.fun.builtins.utils import is_numeric, xsd_num_type, is_string
from n3.ns import xsdNs

# TODO
# generalize with __math_op

def string_concatenation(s, o, ctu):
    if not isinstance(s, Collection):
        return
        
    total = ""
    for s_i in s:
        if not (isinstance(s_i, Literal) and is_string(s_i)):
            return
        total += s_i.value

    if o.is_concrete():
        if not (isinstance(o, Literal) and is_string(o)):
            return
        if total == o.value:
            ctu(s, o) # o is concrete
    else:
        ctu(s, Literal(total, xsdNs['string'])) # o is variable