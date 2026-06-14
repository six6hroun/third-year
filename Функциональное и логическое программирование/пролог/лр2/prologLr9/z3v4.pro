read_list(L) :- write('Введите список: '), read(L).

print_list([]).
print_list([H|T]) :- write(H), write(' '), print_list(T).

first_index([H|_], H, 0).
first_index([_|T], X, I) :- first_index(T, X, I1), I is I1 + 1.

last_index(List, X, I) :- last_index(List, X, 0, -1, I).
last_index([], _, _, Best, Best).
last_index([H|T], X, Pos, Best, I) :-
    H =:= X,
    Pos1 is Pos + 1,
    last_index(T, X, Pos1, Pos, I).
last_index([_|T], X, Pos, Best, I) :-
    Pos1 is Pos + 1,
    last_index(T, X, Pos1, Best, I).

all_indices([], _, []).
all_indices([H|T], X, [0|R]) :- H =:= X, all_indices(T, X, R1), R is R1 + 1.
all_indices([_|T], X, R) :- all_indices(T, X, R1), R is R1 + 1.

list_max_val([H|T], Max) :- list_max_val(T, H, Max).
list_max_val([], Max, Max).
list_max_val([H|T], Acc, Max) :- H > Acc, list_max_val(T, H, Max).
list_max_val([H|T], Acc, Max) :- H =< Acc, list_max_val(T, Acc, Max).

max_indices(List, Indices) :-
    list_max_val(List, Max),
    findall(I, nth0(I, List, Max), Indices).

sublist_between(List, I, J, Sub) :-
    I < J,
    Len is J - I - 1,
    drop(List, I + 1, Temp),
    take(Temp, Len, Sub).

drop([_|T], N, R) :- N > 0, N1 is N - 1, drop(T, N1, R).
drop(L, 0, L).

take(_, 0, []).
take([H|T], N, [H|R]) :- N > 0, N1 is N - 1, take(T, N1, R).



decreasing_indices(List, Indices) :-
    findall(I, (nth0(I, List, Val1), is_decreasing_from(List, I)), Indices).

is_decreasing_from(List, I) :-
    nth0(I, List, Val),
    I1 is I + 1,
    nth0(I1, List, Val1),
    Val > Val1.

decreasing_indices([], []).

task4 :-
    read_list(List),
    decreasing_indices(List, Indices),
    write('Индексы убывания: '), print_list(Indices), nl.



between_first_second_max(List, Result) :-
    max_indices(List, [I1, I2|_]),
    I1 < I2,
    sublist_between(List, I1, I2, Result).

task16 :-
    read_list(List),
    between_first_second_max(List, Result),
    write('Элементы между 1м и 2м максимумами: '), print_list(Result), nl.



between_first_last_max(List, Result) :-
    max_indices(List, Indices),
    Indices = [I1|_],
    last_index(List, list_max_val(List, _), ILast),
    I1 < ILast,
    sublist_between(List, I1, ILast, Result).

task28 :-
    read_list(List),
    between_first_last_max(List, Result),
    write('Элементы между первым и последним максимумами: '), print_list(Result), nl.