read_num(N) :- write('Введите число: '), read(N).

gcd(A, 0, A) :- A > 0.
gcd(A, B, G) :- B > 0, R is A mod B, gcd(B, R, G).

coprime(A, B) :- gcd(A, B, G), G =:= 1.

min_divisor(N, D) :- N > 1, min_divisor(N, 2, D).
min_divisor(N, D, D) :- N mod D =:= 0.
min_divisor(N, D, Res) :- N mod D =\= 0, D1 is D + 1, min_divisor(N, D1, Res).

sum_digits(N, S) :- sum_digits(N, 0, S).
sum_digits(0, Acc, Acc).
sum_digits(N, Acc, S) :- N > 0, N1 is N // 10, Acc1 is Acc + (N mod 10), sum_digits(N1, Acc1, S).


count_not_coprime_even(N, Count) :-
    findall(X, (between(1, N, X), X mod 2 =:= 0, \+ coprime(N, X)), List),
    length(List, Count).

task5_1 :-
    read_num(N),
    count_not_coprime_even(N, Count),
    write('Количество четных чисел, не взаимно простых с '), write(N), write(': '), write(Count), nl.


max_not_coprime_not_div_by(N, MinDiv, Max) :-
    findall(X, (between(1, N, X), \+ coprime(N, X), X mod MinDiv =\= 0), List),
    max_list(List, Max).

sum_digits_lt5(N, S) :-
    sum_digits_lt5(N, 0, S).
sum_digits_lt5(0, Acc, Acc).
sum_digits_lt5(N, Acc, S) :-
    N > 0,
    N1 is N // 10,
    Digit is N mod 10,
    (Digit < 5 -> Acc1 is Acc + Digit ; Acc1 is Acc),
    sum_digits_lt5(N1, Acc1, S).

task5_2 :-
    read_num(N),
    min_divisor(N, MinDiv),
    max_not_coprime_not_div_by(N, MinDiv, MaxNum),
    sum_digits_lt5(N, SumDigits),
    Result is MaxNum * SumDigits,
    write('Максимальное число: '), write(MaxNum), nl,
    write('Сумма цифр <5: '), write(SumDigits), nl,
    write('Произведение: '), write(Result), nl.


task5 :-
    task5_1,
    nl,
    task5_2.