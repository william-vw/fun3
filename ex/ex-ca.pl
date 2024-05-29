type(P, person) :- ability(P, think) .
type(P, person) :- name(P, 'Socrates') .
type(P, canadian) :- type(P, person), address(P, A), country(A, 'CA') .

type(ed, person) .
ability(will, think) .
name(soc, 'Socrates') .
address(ed, addr1) .
address(will, addr2) .
address(soc, addr3) .
country(addr1, 'BE') .
country(addr2, 'CA') .
country(addr3, 'CA') .