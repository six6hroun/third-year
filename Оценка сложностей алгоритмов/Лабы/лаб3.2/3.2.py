import random

def generate_graph(n, density=0.5):
    graph = {i: [] for i in range(n)}

    for i in range(n):
        for j in range(n):
            if i != j and random.random() < density:
                graph[i].append(j)

    return graph


def longest_path_dfs(graph, start, end):
    max_path = []

    def dfs(node, visited, path):
        nonlocal max_path

        if node == end:
            if len(path) > len(max_path):
                max_path = path[:]
            return

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)

                dfs(neighbor, visited, path)

                path.pop()
                visited.remove(neighbor)

    dfs(start, {start}, [start])
    return max_path


def greedy_path(graph, start, end):
    current = start
    visited = {start}
    path = [start]

    while current != end:
        neighbors = [n for n in graph[current] if n not in visited]
        if not neighbors:
            return []

        next_node = random.choice(neighbors)
        path.append(next_node)
        visited.add(next_node)
        current = next_node

    return path


def random_path(graph, start, end):
    current = start
    visited = {start}
    path = [start]

    while current != end:
        neighbors = graph[current]
        if not neighbors:
            return []

        next_node = random.choice(neighbors)

        if next_node in visited:
            return []

        path.append(next_node)
        visited.add(next_node)
        current = next_node

    return path


def improve_path(graph, path, end):
    if not path or path[-1] != end:
        return path

    best = path[:]

    for i in range(len(path)):
        node = path[i]

        for neighbor in graph[node]:
            if neighbor not in best:
                new_path = path[:i+1] + [neighbor]

                if neighbor == end and len(new_path) > len(best):
                    best = new_path

    return best


def test():
    n = 8
    graph = generate_graph(n)
    start = 0
    end = n - 1

    print("Граф:")
    for k, v in graph.items():
        print(k, "->", v)

    print("\nТочный:")
    exact = longest_path_dfs(graph, start, end)
    print(exact, "Длина пути =", len(exact))

    print("\nЖадный:")
    g = greedy_path(graph, start, end)
    print(g, "Длина пути =", len(g))

    print("\nСлучайный:")
    r = random_path(graph, start, end)
    print(r, "Длина пути =", len(r))

    print("\nУлучшенный:")
    imp = improve_path(graph, g, end)
    print(imp, "Длина пути =", len(imp))


if __name__ == "__main__":
    test()