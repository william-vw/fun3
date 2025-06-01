from n3.ns import xsdNs

def is_numeric(lit):
    if lit.dt.ns == xsdNs.iri:
        match (lit.dt.ln):
            case 'decimal':
                return True
            case 'integer':
                return True
            case 'long':
                return True
            case 'int':
                return True
            case 'short':
                return True
            case 'byte':
                return True
            case 'double':
                return True
            case 'float':
                return True
            # TODO: https://www.w3.org/TR/xmlschema-2/#built-in-datatypes
            
    return False

def divide_buckets(lst, num_buck, buck_no=1, start_idx=0, result=[]):
    if buck_no == num_buck:
        new_result = result + [ lst[start_idx:len(lst)] ]
        yield new_result
        return
    buck_left = num_buck - buck_no
    for next_idx in range(start_idx+1, len(lst)-buck_left+1):
        new_result = result[:] + [ lst[start_idx:next_idx] ]
        yield from divide_buckets(lst, num_buck, buck_no+1, next_idx, new_result)