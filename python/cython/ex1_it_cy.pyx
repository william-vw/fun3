import cython

cdef struct Term:
    int type
    char* value
    char* tag1
    char* tag2

cdef struct Triple:
    Term s
    Term p
    Term o

cdef find(int s, int p, int o):
    cdef Triple array[100]
    
    for i in range(100):
        t: Triple = Triple(Term(1, b"http://example.org", "", ""), Term(2, b"_:b0", "", ""), Term(3, b"abc", "string", "en"))
        array[i] = t
    
    return array

def main():
    array: Triple[100] = find(1, 1, 1)

    i: cython.int
    j: cython.int
    ar_len: cython.int = len(array)
    # print("len:", ar_len)
    # for no python interaction:
    # array requires a declared length :-(
    # e.g., array: Triple[3]
    for i in range(ar_len):
        t: Triple = array[i]
        
        for j in range(ar_len):
            t2: Triple = array[j]

# python -m timeit -s "from ex1_it_cy import main" "main()"
# 200 loops, best of 5: 1.7 msec per loop

# with Triple[100] type annotation:
# 5000 loops, best of 5: 84.2 usec per loop