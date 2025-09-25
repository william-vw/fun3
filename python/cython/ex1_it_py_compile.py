import cython

class Term:
    
    def __init__(self, typ, value, tag1, tag2):
        self.typ = typ
        self.value = value
        self.tag1 = tag1
        self.tag2 = tag2

class Triple:
    
    def __init__(self, s, p, o):
        self.s = s
        self.p = p
        self.o = o

def find(s, p, o):
    for i in range(100):
        yield Triple(Term(1, b"http://example.org", "", ""), Term(2, b"_:b0", "", ""), Term(3, b"abc", "string", "en"))

def main():
    array = find(1, 1, 1)

    results = []
    for t in array:
        x = t.s
        for t2 in array:
            y = t2.s
            results.extend([x, y])
            
# python -m timeit -s "from ex1_it_py_compile import main" "main()"
# 5000 loops, best of 5: 40.2 usec per loop