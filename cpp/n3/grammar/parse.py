import time
from bnd_n3_creator import bndN3Creator, n3ParseResult
import cppN3Parser

def parse_n3_file(path, has_vars=False, measure_time=False):
    start = time.time()
    creator = bndN3Creator(has_vars=has_vars)
    cpp_parse_time = cppN3Parser.parse(path, creator)

    result = n3ParseResult(creator.state)
    result.data.done()
    
    end = time.time()
    if measure_time:
        print("cpp time:", (end - start))
    
    return result