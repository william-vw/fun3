from ast import dump, parse

def print_ast():
    mod_code = """
None"""
    
    print(dump(parse(mod_code), indent=4))
    

if __name__ == "__main__":
    print_ast()