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