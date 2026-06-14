man(gurgen).
man(artem).
man(bogdan).
man(nikita).
man(artemi).
man(alexey).

woman(maria).
woman(olga).
woman(anna).
woman(ekaterina).
woman(natalia).
woman(elena).

parent(gurgen, artem).
parent(maria, artem).
parent(gurgen, bogdan).
parent(maria, bogdan).
parent(artem, nikita).
parent(olga, nikita).
parent(artem, artemi).
parent(olga, artemi).
parent(bogdan, alexey).
parent(anna, alexey).
parent(bogdan, elena).
parent(anna, elena).

married(gurgen, maria).
married(artem, olga).
married(bogdan, anna).

men :- 
    write('Список мужчин:'), nl,
    findall(X, man(X), List),
    print_list(List).


women :- 
    write('Список женщин:'), nl,
    findall(X, woman(X), List),
    print_list(List).

print_list([]).
print_list([H|T]) :-
    write(H), nl,
    print_list(T).


children(X) :-
    write('Дети '), write(X), write(':'), nl,
    findall(Y, parent(X, Y), List),
    print_list(List).

mother(X, Y) :-
    woman(X),
    parent(X, Y).

mother(X) :-
    parent(M, X),
    woman(M),
    write('Мама '), write(X), write(' - '), write(M), nl.

brother(X, Y) :-
    man(X),
    X \= Y,
    parent(P, X),
    parent(P, Y).

brothers(X) :-
    write('Братья '), write(X), write(':'), nl,
    findall(B, brother(B, X), List),
    print_list(List).

b_s(X, Y) :-
    X \= Y,
    parent(P, X),
    parent(P, Y).


b_s(X) :-
    write('Братья и сестры '), write(X), write(':'), nl,
    findall(Y, b_s(X, Y), List),
    print_list(List).