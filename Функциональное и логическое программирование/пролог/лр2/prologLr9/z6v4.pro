read_list(L) :- write('Введите список: '), read(L).

read_num(N) :- write('Введите число: '), read(N).

print_list([]).
print_list([H|T]) :- write(H), write(' '), print_list(T).

is_prime(2).
is_prime(3).
is_prime(P) :-
    P > 3,
    P mod 2 =\= 0,
    \+ has_factor(P, 3).
has_factor(N, D) :- D * D =< N, N mod D =:= 0.
has_factor(N, D) :- D * D =< N, D1 is D + 2, has_factor(N, D1).


min_even([], -1).
min_even([H|T], Min) :-
    H mod 2 =:= 0,
    min_even(T, Min1),
    (Min1 =:= -1 -> Min is H ; Min is min(H, Min1)).
min_even([H|T], Min) :-
    H mod 2 =:= 1,
    min_even(T, Min).

task40 :-
    read_list(List),
    min_even(List, Min),
    write('Минимальный четный элемент: '), write(Min), nl.


prime_factors(N, Factors) :- prime_factors(N, 2, Factors).
prime_factors(1, _, []).
prime_factors(N, D, [D|R]) :-
    D * D =< N,
    N mod D =:= 0,
    is_prime(D),
    N1 is N // D,
    prime_factors(N1, D, R).
prime_factors(N, D, R) :-
    D * D =< N,
    N mod D =\= 0,
    D1 is D + 1,
    prime_factors(N, D1, R).
prime_factors(N, D, [N]) :-
    D * D > N,
    N > 1.

task52 :-
    read_num(N),
    prime_factors(N, Factors),
    write('Простые делители: '), print_list(Factors), nl.