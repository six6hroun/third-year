:- [z5].

akinator :-
    write('Загадайте персонажа'), nl,
    ask(1, Answers),
    find(Answers, Name),
    write('Вы загадали: '), write(Name), nl.

ask(7, []).
ask(N, [A|R]) :-
    q(N, Text),
    write(Text), write(' (yes/no): '),
    read(A),
    N1 is N + 1,
    ask(N1, R).

find(Answers, Name) :-
    obj(Name, Answers).

find(Answers, Name) :-
    findall(N, obj(N, A), All),
    check_all(All, Answers, Matches),
    Matches = [Name].

check_all([], _, []).
check_all([N|T], Answers, [N|R]) :-
    obj(N, A),
    A = Answers,
    check_all(T, Answers, R).
check_all([N|T], Answers, R) :-
    obj(N, A),
    A \= Answers,
    check_all(T, Answers, R).