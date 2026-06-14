solve(Culprit) :-
    brothers = [андрей, витя, дима, юра, коля],
    member(Culprit, brothers),

    (Culprit = витя ; Culprit = коля) -> A = true ; A = false,

    (Culprit \= витя, Culprit \= юра) -> V = true ; V = false,

    (A xor V) -> D = true ; D = false,

    (D = false) -> Y = true ; Y = false,

    Truths = [A, V, D, Y],
    count_true(Truths, Count),
    Count >= 3.

xor(true, false, true).
xor(false, true, true).
xor(_, _, false).

count_true([], 0).
count_true([true|T], C) :- count_true(T, C1), C is C1 + 1.
count_true([false|T], C) :- count_true(T, C).

task7 :-
    solve(Culprit),
    write('Окно разбил: '), write(Culprit), nl.