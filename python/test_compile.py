# class Node:
#     def __init__(self, str):
#         self.str = str

from test_node import Node
from types import CodeType, FunctionType

def main():
    str = """
class Node:
    def __init__(self, str):
        self.str = str
        
def fn(input):
    n = Node(input)
    print(n)

# Node("abc") # works with embedded Node class
fn("abc") # works with definition / import in outer file

"""    
    mod = compile(str, "testing", 'exec')
    exec(mod)
    
    # get function to be called
    for c in mod.co_consts:
        if isinstance(c, CodeType) and c.co_name == "fn":
            fn = FunctionType(c, {})

    # call function
    fn("abc") # doesn't work at all

if __name__ == "__main__":
    main()