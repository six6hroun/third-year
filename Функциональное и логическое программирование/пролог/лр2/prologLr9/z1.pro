max(X, Y, U, Z) :- Z is max(max(X, Y), U).

fact_up(0, 1).
fact_up(N, X) :- N > 0, N1 is N - 1, fact_up(N1, X1), X is N * X1.

fact_down(N, X) :- fact_down(N, 1, X).
fact_down(0, Acc, Acc).
fact_down(N, Acc, X) :- N > 0, N1 is N - 1, Acc1 is N * Acc, fact_down(N1, Acc1, X).

sum_digits_up(0, 0).
sum_digits_up(N, S) :- N > 0, N1 is N // 10, sum_digits_up(N1, S1), S is S1 + (N mod 10).

sum_digits_down(N, S) :- sum_digits_down(N, 0, S).
sum_digits_down(0, Acc, Acc).
sum_digits_down(N, Acc, S) :- N > 0, N1 is N // 10, Acc1 is Acc + (N mod 10), sum_digits_down(N1, Acc1, S).

square_free(N) :- N >= 0, \+ has_square_factor(N, 2).
has_square_factor(N, D) :- D * D =< N, N mod (D * D) =:= 0.
has_square_factor(N, D) :- D * D =< N, D1 is D + 1, has_square_factor(N, D1).

read_list(L) :- write('Введите список (например, [1,2,3]): '), read(L).
print_list([]).
print_list([H|T]) :- write(H), write(' '), print_list(T).

sum_list_down(List, Sum) :- sum_list_down(List, 0, Sum).
sum_list_down([], Acc, Acc).
sum_list_down([H|T], Acc, Sum) :- Acc1 is Acc + H, sum_list_down(T, Acc1, Sum).

sum_list_up([], 0).
sum_list_up([H|T], Sum) :- sum_list_up(T, Sum1), Sum is H + Sum1.

sum_program :-
    read_list(List),
    sum_list_down(List, Sum),
    write('Сумма: '), write(Sum), nl.

remove_by_digit_sum([], _, []).
remove_by_digit_sum([H|T], N, [H|R]) :-
    sum_digits_down(H, S),
    S \= N,
    remove_by_digit_sum(T, N, R).
remove_by_digit_sum([H|T], N, R) :-
    sum_digits_down(H, S),
    S =:= N,
    remove_by_digit_sum(T, N, R).