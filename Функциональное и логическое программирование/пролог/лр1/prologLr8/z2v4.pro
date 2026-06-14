:- [z1].

father(X, Y) :- man(X), parent(X, Y).

father(X) :- parent(F, X), man(F), write(F).

wife(X, Y) :- woman(X), married(Y, X).

wife(X) :- married(X, W), woman(W), write(W).