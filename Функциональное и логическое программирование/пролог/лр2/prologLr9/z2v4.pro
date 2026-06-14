prod_digits_up(0, 1).
prod_digits_up(N, Prod) :-
    N > 0,
    N1 is N // 10,
    prod_digits_up(N1, Prod1),
    Digit is N mod 10,
    Prod is Prod1 * Digit.

prod_digits_down(N, Prod) :- prod_digits_down(N, 1, Prod).
prod_digits_down(0, Acc, Acc).
prod_digits_down(N, Acc, Prod) :-
    N > 0,
    N1 is N // 10,
    Digit is N mod 10,
    Acc1 is Acc * Digit,
    prod_digits_down(N1, Acc1, Prod).



max_digit_not_div3_up(0, -1).
max_digit_not_div3_up(N, Max) :-
    N > 0,
    N1 is N // 10,
    max_digit_not_div3_up(N1, Max1),
    Digit is N mod 10,
    (Digit mod 3 =\= 0 ->
        Max is max(Max1, Digit)
    ;
        Max is Max1
    ).

max_digit_not_div3_down(N, Max) :- max_digit_not_div3_down(N, -1, Max).
max_digit_not_div3_down(0, Acc, Acc).
max_digit_not_div3_down(N, Acc, Max) :-
    N > 0,
    N1 is N // 10,
    Digit is N mod 10,
    (Digit mod 3 =\= 0 ->
        Acc1 is max(Acc, Digit)
    ;
        Acc1 is Acc
    ),
    max_digit_not_div3_down(N1, Acc1, Max).



count_divisors_up(N, Count) :- count_divisors_up(N, 1, 0, Count).
count_divisors_up(N, D, Acc, Count) :-
    D * D < N,
    (N mod D =:= 0 ->
        Acc1 is Acc + 2
    ;
        Acc1 is Acc
    ),
    D1 is D + 1,
    count_divisors_up(N, D1, Acc1, Count).
count_divisors_up(N, D, Acc, Count) :-
    D * D =:= N,
    Count is Acc + 1.
count_divisors_up(N, D, Acc, Count) :-
    D * D > N,
    Count is Acc.

count_divisors_down(N, Count) :- count_divisors_down(N, 1, Count).
count_divisors_down(N, D, Count) :-
    D * D < N,
    (N mod D =:= 0 ->
        D1 is D + 1,
        count_divisors_down(N, D1, Count1),
        Count is Count1 + 2
    ;
        D1 is D + 1,
        count_divisors_down(N, D1, Count)
    ).
count_divisors_down(N, D, 1) :- D * D =:= N.
count_divisors_down(N, D, 0) :- D * D > N.