from n3.fun.builtins.utils import divide_buckets
from n3.terms import Var, Collection, Literal
from n3.ns import xsdNs

lst = Collection([Literal(1,xsdNs['int']), Literal(2,xsdNs['int']), Literal(3,xsdNs['int']), Literal(4,xsdNs['int'])])
# buckets = Collection([Var("x")])
# buckets = Collection([Var("x"), Var("y")])
# buckets = Collection([Var("x"), Var("y"), Var("z")])
# buckets = Collection([Var("x"), Var("y"), Var("z"), Var("a")])
# buckets = Collection([Collection([Literal(1,xsdNs['int']),Literal(2,xsdNs['int']),Literal(3,xsdNs['int'])]), Var("x")])
# buckets = Collection([Var("x"), Var("y"), Collection([Literal(1,xsdNs['int']),Literal(2,xsdNs['int']),Literal(3,xsdNs['int'])]), Var("z")])
buckets = Collection([Collection([Literal(1,xsdNs['int']),Literal(2,xsdNs['int']),Literal(3,xsdNs['int'])]), Var("x"), Var("y"), Var("z")])

result = divide_buckets(lst, buckets)
print("\n".join([ str(bucket) for bucket in result ]))