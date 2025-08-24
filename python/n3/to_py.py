import sys
sys.path.insert(0, "../")
sys.path.insert(0, "../../")
from pathlib import Path
import time
from ast import dump, unparse, parse
from lib.utils import Settings
from n3.parse import parse_n3
from n3.objects import ANY
from n3.fun.gen import gen_py, InputData, QueryFn
from n3.fun.utils import unique_sorted

def __proc_inputs(query, rules, data):
    query_str = query.open('r').read() if isinstance(query, Path) else query
    query = parse_n3(query_str, has_vars=True).data.triple_at(0)
    
    rules_str = rules.open('r').read() if isinstance(rules, Path) else rules
    rules = parse_n3(rules_str, has_vars=True).rules
    
    data = InputData(path=data) if isinstance(data, Path) else InputData(data_str=data)    
    
    # print(query); print(rules); print(data)
    return (query, rules, data)

# params:
# { 'print': { 'code: <bool>, 'all': <bool>, 'gen': <GenPython.params> } }
def run_py(query, rules, data, save_to=None, params=None):
    params = Settings(params)
    
    start = time.perf_counter()
    query, rules, data = __proc_inputs(query, rules, data)
    netw_time = round((time.perf_counter() - start)*1000,0)
    
    start = time.perf_counter()
    mod = gen_py(rules, query, data, params['gen'])
    gen_time = round((time.perf_counter() - start)*1000,0)
    
    if not params['print'].enabled('all') and params['print'].enabled('code'):
        print(unparse(mod) + "\n\n")
    
    start = time.perf_counter()
    exec_ret = __get_exec(mod)
    output = __exec_query(exec_ret, query)
    exec_time = round((time.perf_counter() - start)*1000,0)
    
    reas_time = gen_time + exec_time
    
    if params['print'].enabled('all'):
        print(output)
        print("-- START CODE --")
        print(unparse(mod))

    else:
        if save_to is None:
            return output
        else:
            start = time.perf_counter()
            with open(save_to, 'w') as fh:
                fh.write(output)
            netw_time += round((time.perf_counter() - start)*1000,0)
        
    return (netw_time, gen_time, exec_time, reas_time)
       
# params:
# { 'print': { 'code: <bool> }, 'tracing': <bool>, 'code_dir': <string>, 'gen': <GenPython.params> }
def save_py(query, rules, data, out_path, params=None):
    params = Settings(params)
    
    query, rules, data = __proc_inputs(query, rules, data)
    
    mod = gen_py(rules, query, data, params['gen'])
    unparsed = unparse(mod)
    if params['print'].enabled('code'):
        print(unparsed)
    
    imports = []
        
    if params.has('code_dir'):
        unparsed = __use_code_dir(unparsed, imports, params.get('code_dir'))
    
    if params.has('tracing'):
        unparsed = __add_tracing(unparsed, imports, params.get('tracing'))
    
    if len(imports) > 0:
        unparsed = "\n".join(dict.fromkeys(imports)) + "\n" + unparsed
    
    with open(out_path, 'w') as fh:
        fh.write(unparsed)
       
def __get_exec(mod):
    mod_code = compile(mod, "<fun3>", "exec")
    
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
    
    out = set()
    query_fn(*[ANY for _ in variables], lambda *args: out.add(str(query.instantiate({ var: args[idx] for idx, var in enumerate(variables) }))))
    
    return "\n".join(out)

def __use_code_dir(code, imports, parent_dir):
    imports.append("import sys")
    
    return f"""sys.path.insert(0, "{parent_dir}") # noqa\n""" + code

# assumed that code_dir will point to folder with "lib/trace"
def __add_tracing(code, imports, tracing):
    imports.append("import sys")
    
    trace_imports = [ tracing ]
    ret =  f"""sys.settrace({tracing}) # noqa\n""" + code
    
    if tracing == 'count_calls':
        trace_imports.append("print_call_counts")
        ret += "\n\nprint_call_counts()"

    imports.append(f"from lib.trace import {", ".join(trace_imports)}")
    
    return ret
