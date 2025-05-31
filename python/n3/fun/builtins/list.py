from functools import reduce
from n3.terms import Collection
from n3.ns import xsd

def list_append(s, o, ctu):
    if not isinstance(s, Collection):
        return
    
    var_s = False # any vars in collection?
    for s_i in s:
        if s_i.is_concrete():
            if not isinstance(s_i, Collection):
                return
        else:
             var_s = True
        
    if not var_s: # if no vars, append the constituent coll's
        result = reduce(lambda s_i, s_j: s_i + s_j, s)
        
    if o.is_concrete():
        if not isinstance(o, Collection):
            return
        if not var_s:
            if result == o:
                ctu() # s is grounded, o is concrete, s and o are same
        else: 
            args = []; collect = []
            for s_i in s:
                if s_i.is_concrete():
                    collect.append(s_i)
                else:
                    if len(collect) > 0:
                        args.append(Collection(collect))
                        collect = []
            ctu(*args) # s is not grounded, o is concrete
            
    else:
        # cannot have vars in s if o cannot be deconstructed 
        # (i.e., o is a var)
        if var_s: 
            return
        ctu(result) # s is grounded, o is variable
        
        
def list_iterate(s, o, ctu):
    if not isinstance(s, Collection):
        return
        
    if o.is_concrete(): # o (coll) is concrete
        if not (isinstance(o, Collection) and len(o) == 2):
            return
        
        index = None; value = None
        if o[0].is_concrete():
            if not (isinstance(o[0], Literal) and (o[0].dt == xsd['decimal'] or o[0].dt == xsd['double'] or o[0] == xsd['float'])):
                return
            index = o[0].value
            if index > len(s):
                return
        if o[1].is_concrete():
            value = o[1].value            
        
        if index is not None:
            if value is not None:
                if s[index] == value:
                    ctu() # o_1 (index), o_2 (value) are concrete
                    return
            else:
                value = s[index]
                ctu(value) # o_1 (index) is concrete, o_2 (value) is variable
                return
        else:
            if value is not None:
                for index, s_i in enumerate(s):
                    if s_i == value:
                        ctu(index) # o_1 (index) is variable, o_2 (value) is concrete
                        return
    
    for index, s_i in enumerate(s):
        if o.is_concrete(): # o (coll) is concrete but not grounded
            ctu(index, s_i)
        else:
            ctu(Collection(index, s_i)) # o (coll) is variable