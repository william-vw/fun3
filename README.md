# fun3
Stands for **fun**ctional programming for **N3**, or, alternatively, **fun** with **N3**.

# UnifyFlow

For a btp, 3 terms will need to be unified.
for find: 3 match terms (mterms) are variables
for fn: 3 mterms from htp

var either exists (param) or is new

if is_concrete:
   if mterm is concrete:
        return term == match term
    else:
        use myself to unify mterm

else if is_var:
        use mterm to unify myself
        use mterm to unify myself

use x to unify y
    ...


# General process

## Function map
Build a "function map" (technically, a multimap) from predicates to function names. E.g., for rules
{ ?p a :Canadian } <= { ... } .
{ ?p a :Canadian } <= { ... } .
{ :elbert ?x :will } <= { ... } .

We create a map:
    a -> [ rule_0, rule_1 ]
    'var' -> [ rule_2 ]
    'all' -> [ rule_0, rule_1, rule_2 ]

Where rule_0, rule_1 and rule_2 are functions each implementing one of the 3 rules.
If a concrete term is used as predicate, its function is added to the term's entry.
If a variable is used as predicate, its function is added to a 'var' entry.
All functions are added to an 'all' entry.

When a mapped predicate is encountered in a body triple pattern (btp), we will try to resolve the btp by calling the mapped functions.
E.g., if the predicate is 'a', then [ rule_0, rule_1, rule_2 ] are returned. (I.e., functions mapped to a variable predicate are always returned.)
E.g., if the predicate is 'label', then [ rule_2 ] are returned. (See above.)
E.g., if the predicate is a variable, then all entries [ rule_0, rule_1, rule_2 ] are always returned.

In each rule, we also rename all rule variables so they are unique across all rules. They will retain their original name, but with a unique counter attached to it. E.g., a variable ?p will be renamed ?p_0. This is greatly simplifies the ensuing process.

## Generate functions
Generate functions for all rules.
Per rule, we generate separate functions for each of their btps.
The first function name corresponds to the above mapped function name (e.g., rule_0). So, it will be called whenever the rule is used to resolve a tp.
The subsequent functions will be called rule_0_1, rule_0_2, etc.

These functions will have parameters, which are based on rule variables (e.g., ?p), and will be called with arguments.
For the first function, the parameters will include the variables found in the rule head. So, when resolving a tp using the rule - calling its corresponding function - arguments will be passed for these parameters (None ,may also be passed).
For subsequent functions, these parameters will be expanded to include the variables from the prior btps. For instance, for the second function, the parameters will include the rule head variables, and the variables of the first btp. This way, we always pass on any variable values that may have been collected until that point. (Note: it is possible that the subsequent btp's won't need these variable values, i.e., they don't occur there. This simplifies matters.)

There are extra parameters for "internal" use:
. "final_ctu", which is the function that will finally be called when all "btp" functions were successful, which passes arguments for the head variables. This final_ctu fn is either a top-level continuation (ctu) (e.g., which prints the rule results); or a ctu passed by another function, which used this function to resolve one of its btp's.
. "data", i.e., the data store.
. "state"; I forget what this is about.
Whenever we refer to parameters, we mean those representing variables (so, not these internal ones), unless explicitly stated.

A function will try to resolve a tp by finding matches in the data, and finding matching function rules (using the aforementioned predicate map).
After finding a succesful match, the function will call (the ctu that itself calls) the function for the next btp, with arguments for its parameters.
These arguments will be based on data from a matching data triple, or based on arguments passed by the matching function rule.
If the tp is the last in the body, the function will call the aforementioned "ctu" function.

### Finding data matches
Find data triples that can be used to resolve the tp.
The function "find" is called on the data store, passing concrete terms or arguments based on the tp s/p/o. 
If the term is concrete, it is simply passed.
It the term is a variable, and it was given as a parameter to this function, then pass the corresponding argument. (This is an example of unification; we ensure that the prior variable's value is used to search for matching data triples, and thus corresponds to the value for this btp's variable.)
It the term is a variable, and it was not given as a parameter, then pass None.

We pass a lambda to the "find" call with parameters "t" (a single matched data triple) and "state". 
This lambda then calls the aforementioned ctu function, which has its own set of parameters (i.e., head variables, and body variables encountered until now).
For each of those parameters, we need to pass an argument.
If the parameter corresponds to a variable in this btp (e.g., "?p"), then we pass the matched data triple's corresponding term (e.g., triple.s). (It is possible here that the above mentioned unification with a function parameter happened; in that case, we might as well have passed that parameter.)
Else, the parameter corresponds to a previously encountered variable, and we simply pass the argument for that parameter that this function was given.

### Finding rule matches
Using the previously generated "function map", find functions that can be used to resolve the btp.
For any found functions, we need to compare their head tp (htp) to the btp in more detail. We need to pair-wise compare each term between the tp's.
This will determine which arguments will be passed _to_ the function, and how arguments will be passed back _from_ the function.

Re the "passing back": we will pass a ctu to the matching function. If the matching function is successful, it will call this ctu with values for rule head variables. (So, even if we don't need these values, we still need our ctu to accept them.) This ctu will itself call either the next btp's function, or the final_ctu.

If the btp term is a variable: note that (btp.1) we need a value for it here, which will be given by the matching function, and (btp.2) it is possible that it was given as a function parameter.
If the htp term is a variable: note that we need to pass a value for it, and the matching function will pass a value back for it. If our btp term was also a variable, then we will need this value.

(Note: most of these are examples of unification.)
If both terms are concrete, we simply compare them; if they are not equal, we do not call the function.
If the btp term is a variable:
    If the htp term is also a variable: if the btp's variable was given as a function parameter (btp.1), then pass the corresponding argument; else, pass None. Also, the value passed back from the matching function is now a value for the btp variable (btp.2). 
    If the htp term is instead concrete: if the btp's variable was given as a function parameter (btp.1), then the corresponding argument has to be compared with the concrete htp term. A condition is added that performs this check (at runtime) before calling the function. Also, the concrete htp term is now a value for the btp variable (btp.2); if the btp variable is a parameter for this function's own ctu, then we pass this htp term as an argument for it.
If the btp term is instead concrete, but the htp term is a variable, then we simply pass the former as an argument. The matching function will still pass a value back for the variable, but we can ignore it (it will/should be the same as our concrete term that we passed).