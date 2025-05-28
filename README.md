# fun3
Stands for **fun**ctional programming for **N3**, or, alternatively, **fun** with **N3**.

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
Within the function, the parameter arguments will be used to find data matches and matching rule functions.
Hence, they drive the assignment aspect of unification (see below).

For the first function, the parameters will include the variables found in the rule head. So, when resolving a tp using the rule - calling its corresponding function - arguments will be passed for these parameters ("Any" may also be passed, which represents any value).
For subsequent functions, these parameters will be expanded to include the variables from the prior btps. For instance, for the second function, the parameters will include the rule head variables, and the variables of the first btp. This way, we always pass on any variable values that may have been collected until that point. (Note: it is possible that the subsequent btp's won't need these variable values, i.e., they don't occur there. This simplifies matters.)

There is an extra parameter for "internal" use:
. "final_ctu", which is the function that will finally be called when all "btp" functions were successful, which passes arguments for the head variables. This final_ctu fn is either a top-level continuation (ctu) (e.g., which prints the rule results); or a ctu passed by another function, which used this function to resolve one of its btp's.
Whenever we refer to parameters, we mean those representing variables (so, not this internal one), unless explicitly stated.

A function will try to resolve a tp by finding matches in the data, and finding matching function rules (using the aforementioned predicate map).
For that purpose, it will call data.find and matching rule functions, respectively.
The latter functions, after finding a succesful match, will call (the ctu that itself calls) the function for the next btp, with arguments for its parameters.
These arguments are from a matching data triple, or the matching rule's htp.
If the tp is the last in the body, the function will call the aforementioned "final_ctu" function.

## Unification

When considering unification as part comparison, and part assignment, we (a) compare constants with each other at compile time, and, at runtime, comparing them with variables (comparison); and (b) passing arguments for parameters at runtime (assignment).

Regarding (b), data search and rule functions are called with arguments for their parameters; they themselves call a continuation function with arguments for the continuation's parameters.
The former are both referred to as match functions. We say that arguments are "passed" to them; and the latter "return" arguments (although they technically also pass arguments to the continuation).

Unification commences by comparing terms from the the btp ("clause") and htp ("match") in a pair-wise way.
For data searches, the following htp is assumed: ?s ?p ?o.

- If both terms are concrete (literals/iri's), we compare them at compile time: if they are unequal, we won't call the match function.  

- If the match term is a variable, then its match function will have a parameter for it.
By passing an argument for that parameter, we ensure that the argument will be used by the match function.
Hence, we unified something (whatever was passed) with the match variable (assignment).

    - If the clause term is concrete, we simply pass it.
    - If the clause term is a variable, we similarly pass it.
But, in the latter case, it is possible that the clause variable's value is "any". So, no unification will happen by passing it.
In that case, we need to use the argument returned by the matching function. 
In turn, we use it as an argument for the clause variable's parameter, passing it to the next function call (albeit belonging to the next btp or the final_ctu).
Hence, we again unified something (whatever was returned) with the clause variable (assignment).

- If the clause term is a variable, and the match term is concrete, we add a runtime comparison between the clause and match term.
But, as before, it is possible that the clause variable's value is "any", so the comparison will always be true.
In that case, we use the concrete match term, and pass it to the next function call (idem above).

### Ungrounded collections
TODO

TODO: also unify multiple occurrences of same variable in same triple