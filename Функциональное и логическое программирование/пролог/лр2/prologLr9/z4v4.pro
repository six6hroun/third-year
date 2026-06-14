solve(Solution) :-
    Vessels = [бутылка, стакан, кувшин, банка],
    Drinks = [молоко, лимонад, квас, вода],

    permutation(Drinks, [M, L, K, V]),

    M \= бутылка,
    V \= бутылка,

    L \= банка,
    V \= банка,

    ( (L = кувшин) ; (L = K) ),
    \+ (L = кувшин, K = L),

    neighbor(стакан, банка, Vessels),
    neighbor(стакан, M, Vessels).

neighbor(X, Y, [X, Y|_]).
neighbor(X, Y, [Y, X|_]).
neighbor(X, Y, [_|T]) :- neighbor(X, Y, T).

task4 :-
    solve([M, L, K, V]),
    write('Молоко: '), write(M), nl,
    write('Лимонад: '), write(L), nl,
    write('Квас: '), write(K), nl,
    write('Вода: '), write(V), nl.