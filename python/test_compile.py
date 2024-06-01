# class Node:
#     def __init__(self, str):
#         self.str = str

# from test_node import Node
# from types import CodeType, FunctionType

# def fn_2():
#     print("got here")

def main():
    str = """
from test_node import Node
    
def fn_2(input):
    n = Node(input)
    print(n.str)
        
def fn(input):
    fn_2(input)
"""    

    mod_code = compile(str, "<fun3>", "exec")

    new_refs = {}
    exec(mod_code, globals(), new_refs)
    # print(new_refs)
    
    for name, code in new_refs.items():
        globals()[name] = code
        
    new_refs['fn']("abc")
            

if __name__ == "__main__":
    main()