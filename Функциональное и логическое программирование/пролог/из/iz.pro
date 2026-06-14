% ============================================
% ИНДИВИДУАЛЬНОЕ ЗАДАНИЕ №2
% ВАРИАНТ 32
% Построить все графы из 9 вершин, 
% которые можно раскрасить в 3 цвета
% ============================================

% === Генерация всех графов на 9 вершинах ===

% Все возможные рёбра для 9 вершин (всего C(9,2) = 36 рёбер)
all_edges(9, Edges) :-
    findall(E, (between(1,9,U), between(1,9,V), U < V, E = [U,V]), Edges).

% Генерация графа по битовой маске (0/1 для каждого ребра)
generate_graph(Edges, Mask, Graph) :-
    generate_graph(Edges, Mask, 0, Graph).

generate_graph([], [], _, []).
generate_graph([E|ER], [0|MR], Pos, Graph) :-
    Pos1 is Pos + 1,
    generate_graph(ER, MR, Pos1, Graph).
generate_graph([E|ER], [1|MR], Pos, [E|Graph]) :-
    Pos1 is Pos + 1,
    generate_graph(ER, MR, Pos1, Graph).

% Генерация всех графов (2^36 вариантов - слишком много, используем ограничения)
% Для 9 вершин 2^36 = 68 млрд - нереально.
% Поэтому генерируем только связные графы с разумным количеством рёбер


% === Проверка раскраски в 3 цвета ===

% Раскраска: список [вершина-цвет], цвета 1,2,3
color(1). color(2). color(3).

% Проверка корректности раскраски
valid_coloring(_, []).
valid_coloring(Graph, [V-C|Rest]) :-
    valid_coloring(Graph, Rest),
    \+ (member([V,Adj], Graph), member([Adj,V], Graph); member([Adj,V], Graph)),
    member([V,Adj], Graph),
    member(Adj-C, Rest),
    fail.
valid_coloring(Graph, [V-C|Rest]) :-
    valid_coloring(Graph, Rest),
    \+ (member([V,Adj], Graph), member([Adj,V], Graph); member([Adj,V], Graph)),
    member([Adj,V], Graph),
    member(Adj-C, Rest),
    fail.
valid_coloring(_, _).

% Упрощённая проверка
is_valid_coloring(Graph, Coloring) :-
    forall(member([U,V], Graph),
           (member(U-C1, Coloring), member(V-C2, Coloring), C1 \= C2)).

% Поиск раскраски в 3 цвета
colorable_3(Graph, Coloring) :-
    findall(V, (member([U,_], Graph); member([_,V], Graph)), Vertices0),
    sort(Vertices0, Vertices),
    coloring_attempt(Vertices, Graph, Coloring).

coloring_attempt([], _, []).
coloring_attempt([V|T], Graph, [V-C|Rest]) :-
    color(C),
    coloring_attempt(T, Graph, Rest),
    is_valid_coloring(Graph, [V-C|Rest]).


% === Генерация всех графов с ограничением на рёбра ===

% Количество рёбер от 0 до 36 (но для 9 вершин и 3-цветности нужно минимум 0, максимум ~?)
% Ограничимся связными графами с 8-20 рёбрами для практичности

generate_all_colorable_graphs(N, MinEdges, MaxEdges, Result) :-
    all_edges(N, Edges),
    length(Edges, TotalEdges),
    between(MinEdges, MaxEdges, ECount),
    findall(Graph, (generate_graph_with_edges(Edges, ECount, Graph), colorable_3(Graph, _)), Result).

generate_graph_with_edges(Edges, ECount, Graph) :-
    length(Edges, Len),
    ECount =< Len,
    findall(E, (between(1, Len, I), select_edge(Edges, I, E)), Graph),
    length(Graph, ECount).

select_edge(Edges, I, E) :-
    nth1(I, Edges, E).

% Альтернативный подход: перебор подмножеств рёбер
graph_from_mask(Edges, Mask, Graph) :-
    findall(E, (nth0(I, Edges, E), nth0(I, Mask, 1)), Graph).

all_masks(Len, Mask) :-
    length(Mask, Len),
    maplist([X]>>(member(X, [0,1])), Mask).

generate_all_graphs(N, Graph) :-
    all_edges(N, Edges),
    length(Edges, Len),
    all_masks(Len, Mask),
    graph_from_mask(Edges, Mask, Graph).

% Оптимизированная генерация только 3-цветных графов
generate_3colorable_graphs(N, MaxGraphs, Graphs) :-
    all_edges(N, Edges),
    length(Edges, Len),
    findall(Graph, (
        between(0, min(20, Len), ECount),
        random_mask(ECount, Len, Mask),
        graph_from_mask(Edges, Mask, Graph),
        colorable_3(Graph, _)
    ), Graphs0),
    sort(Graphs0, Graphs),
    length(Graphs, L),
    (L >= MaxGraphs -> true ; generate_3colorable_graphs(N, MaxGraphs, Graphs)).

random_mask(0, _, []).
random_mask(N, Len, [1|T]) :-
    N > 0,
    random(0, Len, R),
    R < Len,
    N1 is N - 1,
    Len1 is Len - 1,
    random_mask(N1, Len1, T).
random_mask(N, Len, [0|T]) :-
    Len > 0,
    Len1 is Len - 1,
    random_mask(N, Len1, T).


% === Вывод в файл ===

write_graphs_to_file(Graphs, Filename) :-
    open(Filename, write, Stream),
    write(Stream, '%% Графы из 9 вершин, раскрашиваемые в 3 цвета'), nl(Stream),
    write(Stream, '%% Всего: '), write(Stream, Graphs), nl(Stream),
    write_graphs(Stream, Graphs),
    close(Stream).

write_graphs(_, []).
write_graphs(Stream, [G|T]) :-
    write(Stream, G), nl(Stream),
    write_graphs(Stream, T).


% === Проверка конкретного графа ===

test_graph(Graph) :-
    (colorable_3(Graph, Coloring) ->
        write('Граф: '), write(Graph), nl,
        write('Раскраска: '), write(Coloring), nl
    ;
        write('Граф не 3-цветный'), nl
    ).


% === Примеры графов ===

% Пустой граф (9 изолированных вершин) - 3-цветный
empty_graph(9, []).

% Полный граф K9 - не 3-цветный (требует 9 цветов)
complete_graph(9, Edges) :-
    findall([U,V], (between(1,9,U), between(U,9,V), U < V), Edges).

% Цикл C9 - 3-цветный (нечётный цикл требует 3 цвета)
cycle_graph(9, Edges) :-
    findall([U,V], (between(1,8,U), V is U+1), Edges1),
    Edges = [[1,9]|Edges1].

% Двудольный граф K4,5 - 2-цветный (значит и 3-цветный)
bipartite_graph(Edges) :-
    findall([U,V], (between(1,4,U), between(5,9,V)), Edges).


% === Запуск ===

run :-
    write('Построение 3-цветных графов из 9 вершин...'), nl,
    cycle_graph(9, G1),
    bipartite_graph(G2),
    test_graph(G1),
    test_graph(G2),
    complete_graph(9, G3),
    test_graph(G3).