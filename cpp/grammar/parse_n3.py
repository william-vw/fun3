import n3Parser

def cb(msg):
    print("cb:", msg)

n3Parser.parse("/Users/wvw/git/n3/fun3/python/tests-bench/zika/data/gen20000_pt2.n3", cb)