from ast import dump, unparse, parse
from n3.parse import parse_n3
from n3.objects import ANY
from n3.fun.gen import gen_py, InputData, QueryFn
from n3.fun.utils import unique_sorted

def run_py(query_str, rules_str, data_str, print_code=False):
    #print(query_str, "\n", rules_str, "\n", data_str)
    query = parse_n3(query_str).data.triple_at(0)
    rules = parse_n3(rules_str).rules
    
    mod = gen_py(rules, query, InputData(data_str=data_str), call_query=False)
    if print_code:
        print(unparse(mod) + "\n\n")
    
    exec_ret = __get_exec(mod, InputData(data_str=data_str))
    return __exec_query(exec_ret, query)
       
def save_py(query_str, rules_str, data_str, out_path, print_code=False):
    #print(query_str, "\n", rules_str, "\n", data_str)
    query = parse_n3(query_str).data.triple_at(0)
    rules = parse_n3(rules_str).rules
    
    mod = gen_py(rules, query, InputData(data_str=data_str))
    unparsed = unparse(mod)
    if print_code:
        print(unparsed)
    
    with open(out_path, 'w') as fh:
        fh.write(unparsed)
       
def __get_exec(mod, in_data):
    mod_code = compile(mod, "<fun3>", "exec")
    
    global data
    data = parse_n3(in_data.data_str).data
    
    new_refs = {}
    exec(mod_code, globals(), new_refs)
    
    for name, code in new_refs.items():
        globals()[name] = code
        
    return new_refs

# def __unparse_with_lineno(ast):
#     code = unparse(ast)
#     return "\n".join([ f"{i+1}. {line}" for i, line in enumerate(code.split("\n")) ])

def __exec_query(exec_ret, query):
    fn_name = QueryFn.fn_name()
    variables = unique_sorted(query.recur_vars())
    
    query_fn = exec_ret[fn_name]
    
    out = []
    query_fn(*[ANY for _ in variables], lambda *args: out.append(str(query.instantiate({ var: args[idx] for idx, var in enumerate(variables) }))))
    
    return "\n".join(out)