import sys
sys.path.insert(0, "../../python")
from n3.parse import n3ParseResult

from n3_creator import n3Creator as pyN3Creator
import n3Parser as cppN3Parser

# msgs = []
# def cb(msg):
#     # print("cb:", msg)
#     msgs.append(msg)

creator = pyN3Creator(has_vars=False)
path = "/Users/wvw/git/n3/fun3/python/tests-bench/zika/data/gen100_pt2.n3"
# path = "./test.n3"
cppN3Parser.parse(path, creator)

result = n3ParseResult(creator.state)
result.data.done()

print(creator.state.prefixes)
print(creator.state.base)