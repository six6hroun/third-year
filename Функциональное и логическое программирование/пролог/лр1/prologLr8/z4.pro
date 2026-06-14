q(1, 'Это животное?').
q(2, 'Оно умеет летать?').
q(3, 'Оно живет в воде?').
q(4, 'У него есть шерсть?').

obj(собака, [yes, no, no, yes]).
obj(кошка, [yes, no, no, yes]).
obj(птица, [yes, yes, no, no]).
obj(рыба, [yes, no, yes, no]).

obj(хомяк, [yes, no, no, yes]).
obj(крокодил, [yes, no, yes, no]).
obj(пингвин, [yes, no, yes, no]).
obj(летучая_мышь, [yes, yes, no, yes]).

q(5, 'Это персонаж?').
q(6, 'У него есть суперсила?').

obj(бэтмен, [no, no, no, no, yes, no]).
obj(супермен, [no, yes, no, no, yes, yes]).
obj(человек_паук, [no, no, no, no, yes, yes]).
obj(железный_человек, [no, yes, no, no, yes, no]).