:- [z1].

grand_da(X, Y) :-
    woman(X),
    parent(Z, X),
    parent(Y, Z).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grand_da2(X, Y) :- woman(X), grandparent(Y, X).

grand_dats(X) :-
    findall(Y, (woman(Y), parent(Z, Y), parent(X, Z)), List),
    write(List).

grand_dats2(X) :-
    findall(Y, grand_da2(Y, X), List),
    write(List).

grand_pa_and_da(X, Y) :-
    man(X), woman(Y), parent(Z, Y), parent(X, Z).
grand_pa_and_da(X, Y) :-
    man(Y), woman(X), parent(Z, X), parent(Y, Z).

grand_pa_and_da2(X, Y) :-
    grand_da2(Y, X), man(X), woman(Y).
grand_pa_and_da2(X, Y) :-
    grand_da2(X, Y), man(Y), woman(X).

aunt(X, Y) :-
    woman(X),
    parent(GP, X),
    parent(GP, P),
    parent(P, Y),
    X \= P.

sibling(X, Y) :- X \= Y, parent(P, X), parent(P, Y).
aunt2(X, Y) :- woman(X), sibling(X, P), parent(P, Y).

aunts(X) :-
    findall(A, (woman(A), parent(GP, A), parent(GP, P), parent(P, X), A \= P), List),
    write(List).

aunts2(X) :-
    findall(A, aunt2(A, X), List),
    write(List).