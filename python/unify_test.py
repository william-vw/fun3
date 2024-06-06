# fn(vars, idx, unbound, body)
#     for i = idx; i < len(vars); i++:
#         + if vars[i] not-none - body=body
#         if idx > 0 && idx % 2 != 0:
#             + if vars[idx-1] == vars[i] - body=body
#         if idx < len(vars):
#             fn(vars, i+1, unbound.copy, body)
#         else:
#             + ctu; + pass vars[i] as unbound
#         unbound += vars[i]

#         + else
#         + ctu; + pass vars[i] as unbound

def unify(vars, idx, bound, unbound, body):
    var = vars[idx]; inc = 0
    print(f"{' '*body}if {var} is not None:"); inc += 4
    if len(bound) > 0:
        print(f"{' '*(body+inc)}if {bound[-1]} == {var}:"); inc += 4
    bound.append(var)
    if idx+1 < len(vars):
        unify(vars, idx+1, bound[:], unbound[:], body+inc)
    else:
        print(f"{' '*(body+inc)}ctu({use_bound(vars, bound, unbound)})");
    
    bound.pop()
    unbound.append(var)
    if idx+1 < len(vars):
        print(f"{' '*(body)}else:");
        unify(vars, idx+1, bound[:], unbound[:], body+inc)
    elif len(bound) > 0:
        print(f"{' '*(body)}else:");
        print(f"{' '*(body+inc)}ctu({use_bound(vars, bound, unbound)})");

def use_bound(vars, bound, unbound):
    return ", ".join([ var if var in bound else bound[0] for var in vars ])# + f" - unbound:{unbound}"

def main():
    unify(['desc1', 'desc2'], 0, [], [], 0)

if __name__ == "__main__":
    main()