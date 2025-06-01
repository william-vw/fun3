from n3.ns import xsd

def is_numeric(lit):
    if lit.dt.ns == xsd.iri:
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

def divide_buckets(lst, num_buck, buck_no, start_idx, result):
    if buck_no == num_buck-1:
        result = result + [ lst[start_idx:len(lst)] ]
        yield result
        return
    buck_left = num_buck - (buck_no+1)
    for next_idx in range(start_idx+1, len(lst)-buck_left+1):
        yield from divide_buckets(lst, num_buck, buck_no+1, next_idx, result[:] + [ lst[start_idx:next_idx] ])