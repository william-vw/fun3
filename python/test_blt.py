from n3.fun.builtins.utils import divide_buckets

lst = [1, 2, 3, 4]
# buckets = [None]
# buckets = [None, None]
# buckets = [None, None, None]
buckets = [None, None, None, None]
# buckets = [[1,2,3], None]
# buckets = [None, None, [1,2,3], None]
# buckets = [[1,2,3], None, None, None]

result = divide_buckets(lst, buckets)
print("\n".join([ str(bucket) for bucket in result ]))