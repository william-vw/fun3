use std::fmt;

struct State {
    stop: bool
}

struct Store {
    triples: [ Triple; 9 ] // ex 1
    // triples: [ Triple; 2 ]
}

impl Store {
    fn find<F>(&self, s: Option<&str>, p: Option<&str>, o: Option<&str>, state: &mut State, ctu: &F) 
        where F: Fn(&Triple, &mut State)
    {
        for t in &self.triples {
            if state.stop {
                return;
            }

            if let Some(sv) = s {
                if sv != &t.s { continue; }
            }

            if let Some(pv) = p {
                if pv != &t.p { continue; }
            }

            if let Some(ov) = o {
                if ov != &t.o { continue; }
            }

            ctu(&t, state);
        }
    }
}

struct Triple {
    s: String,
    p: String,
    o: String
}

impl fmt::Display for Triple {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} {} {}", self.s, self.p, self.o)
    }
}

// - ex 1

fn result(p: &String, a: &String, state: &mut State) {
    println!("solution: {p} {a}");
    // state.stop = true;
}

// (?p, type, Person) :-
//	(?p, ability, think) .

fn r1<F>(p: Option<&String>, store: &Store, state: &mut State, ctu: &F)
    where F: Fn(&String, &mut State)
{
    store.find(p.map(|s| &s[..]), Some("ability"), Some("think"), state, &|t, state| ctu(&t.s, state));
}

// (?p, type, Person) :-
// 	(?p, name, "Socrates") .

fn r2<F>(p: Option<&String>, store: &Store, state: &mut State, ctu: &F) 
    where F: Fn(&String, &mut State)
{
    store.find(p.map(|s| &s[..]), Some("name"), Some("\"Socrates\""), state, &|t, state| ctu(&t.s, state));
}

// (?p, type, Canadian) :-
// 	(?p, type, Person), (?p, address, ?a), (?a, country, "CA")

fn r3<F>(p: Option<&String>, store: &Store, state: &mut State, ctu: &F) 
    where F: Fn(&String, &String, &mut State)
{
    // cfr. trying different clauses after backtracking
    // (no co-routining here, clearly)
    store.find(p.map(|s| &s[..]), Some("type"), Some("Person"), state, &|t, state| r3_cl2(&t.s, store, state, ctu));
    if !state.stop {
        r1(p, store, state, &|p, state| r3_cl2(p, store, state, ctu));
    }
    if !state.stop {
        r2(p, store, state, &|p, state| r3_cl2(p, store, state, ctu));
    }
}

fn r3_cl2<F>(p: &String, store: &Store, state: &mut State, ctu: &F)
    where F: Fn(&String, &String, &mut State)
{
    // println!("r3_cl2 {p}");
    store.find(Some(&p[..]), Some("address"), None, state, &|t, state| r3_cl3(p, &t.o, store, state, ctu));
}

fn r3_cl3<F>(p: &String, a: &String, store: &Store, state: &mut State, ctu: &F) 
    where F: Fn(&String, &String, &mut State) {
    // println!("r3_cl3 {p} {a}");
    store.find(Some(&a[..]), Some("country"), Some("\"CA\""), state, &|_, state| ctu(p, a, state));
}

// // - ex 2

// fn result(desc: &String, anc: &String, state: &mut State) {
//     println!("solution: {desc} {anc}");
//     // state.stop = true;
// }

// // (?desc ancestor ?anc) :-
// //      (?desc parent ?parent)
// //      (?parent ancestor ?anc)

// // (?desc ancestor ?desc) :- cut .

// // (d parent c)
// // (c parent b)
// // (b parent a)

// // (absolutely no idea what's going on with the ctu type; 
// // when not using &F, we pass ref of fn, ref of ref of fn, ...?)
// // solution based on
// // https://stackoverflow.com/questions/31196422/what-does-overflow-evaluating-the-requirement-mean-and-how-can-i-fix-it

// fn r1<F>(desc_0: Option<&String>, anc_0: Option<&String>, desc: Option<&String>, anc: Option<&String>, store: &Store, state: &mut State, ctu: &F) 
//     where F: Fn(&String, &String, &mut State)
// {
//     println!("r1 {:?} {:?} {:?} {:?}", desc_0, anc_0, desc, anc);

//     store.find(desc.map(|s| &s[..]), Some("parent"), None, state, 
//         &|t, state| { 
//             let desc_0v = desc_0.unwrap_or(&t.s);
//             r1_cl2(desc_0v, anc_0, &t.o, anc, store, state, ctu);
//         });
// }

// fn r1_cl2<F>(desc_0: &String, anc_0: Option<&String>, parent: &String, anc: Option<&String>, store: &Store, state: &mut State, ctu: &F) 
//     where F: Fn(&String, &String, &mut State)
// {
//     println!("r1_cl2 {:?} {:?} {:?} {:?}", desc_0, anc_0, parent, anc);
//     r1(Some(desc_0), anc_0, Some(parent), anc, store, state, ctu);
//     if !state.stop {
//         if let Some(anc_s) = anc {
//             if parent == anc_s {
//                 ctu(desc_0, parent, state);
//                 // return; // cut
//             }
//         } else {
//             ctu(desc_0, parent, state);
//         }
//     }
// }


fn main() {
    let mut state = State { stop: false };
    
    // - ex1

    let store = Store {
        triples: [ 
            Triple { s: "ed".to_string(), p: "type".to_string(), o: "Person".to_string() },
            Triple { s: "will".to_string(), p: "ability".to_string(), o: "think".to_string() },
            Triple { s: "soc".to_string(), p: "name".to_string(), o: "\"Socrates\"".to_string() },
    
            Triple { s: "ed".to_string(), p: "address".to_string(), o: "addr1".to_string() },
            Triple { s: "will".to_string(), p: "address".to_string(), o: "addr2".to_string() },
            Triple { s: "soc".to_string(), p: "address".to_string(), o: "addr3".to_string() },
    
            Triple { s: "addr1".to_string(), p: "country".to_string(), o: "\"BE\"".to_string() },
            Triple { s: "addr2".to_string(), p: "country".to_string(), o: "\"CA\"".to_string() },
            Triple { s: "addr3".to_string(), p: "country".to_string(), o: "\"CA\"".to_string() }
        ]
    };

    r3(None, &store, &mut state, &result);
    // r3(Some(&"will".to_string()), &store, &mut state, &result);

    // // - ex2

    // let store = Store {
    //     triples: [ 
    //         Triple { s: "c".to_string(), p: "parent".to_string(), o: "b".to_string() },
    //         Triple { s: "b".to_string(), p: "parent".to_string(), o: "a".to_string() }
    //     ]
    // };

    // // r1(Some(&"c".to_string()), Some(&"a".to_string()), Some(&"c".to_string()), Some(&"a".to_string()), &store, &mut state, &result);
    // r1(None, None, None, None, &store, &mut state, &result);

}