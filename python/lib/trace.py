from collections import defaultdict

indent_level = 0
def trace_calls(frame, event, arg):
    global indent_level
    if "rule" in frame.f_code.co_name:
        if event == 'call':
            call_args = { var_name: frame.f_locals[var_name] for var_name in frame.f_code.co_varnames[:frame.f_code.co_argcount] 
                         if var_name in frame.f_locals and var_name != 'final_ctu' }
            print('  ' * indent_level + f"Callin: {frame.f_code.co_name} {call_args}")
            indent_level += 1
        elif event == 'return':
            indent_level -= 1
            print('  ' * indent_level + f"Return: {frame.f_code.co_name} (Returned: {arg})")
    return trace_calls

call_counts = defaultdict(lambda : defaultdict(int))
def count_calls(frame, event, arg):
    global call_counts
    fn_name = frame.f_code.co_name
    if "rule" in fn_name:
        if event == 'call':
            call_args = { var_name: frame.f_locals[var_name] for var_name in frame.f_code.co_varnames[:frame.f_code.co_argcount] 
                         if var_name in frame.f_locals and var_name != 'final_ctu' }
            call_args = tuple(call_args.items())
            
            calls = call_counts[fn_name]
            calls[call_args] += 1
            
    return count_calls

def print_call_counts():
    total_all = 0
    print("\ncall counts:")
    for fn_name, call_dict in call_counts.items():
        total_fn = sum(call_dict.values())
        total_all += total_fn
        print(f"- {fn_name}: #{total_fn}")
        
        counts = sorted(call_dict.items(), key=lambda i: i[1], reverse=True)
        for call_args, count in counts:
            print(f"{call_args}: #{count}")
 
    print(f"all: #{total_all}")