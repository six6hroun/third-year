import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def solve_graphical():
    def line1(x1): return (2 * x1 + 10) / 5
    def line2(x1): return (40 - 4 * x1) / 5
    def line3(x1): return (5 - x1) / 5
    vertices = []
    vertices.append((5, 4))
    vertices.append((0, line1(0)))
    vertices.append((0, line3(0)))
    vertices.append((10, 0))
    vertices.append((5, 0))

    def check_point(x1, x2):
        return (2 * x1 - 5 * x2 >= -10 - 1e-9 and
                4 * x1 + 5 * x2 <= 40 + 1e-9 and
                x1 + 5 * x2 >= 5 - 1e-9 and
                x1 >= 0 - 1e-9 and
                x2 >= 0 - 1e-9)

    feasible_vertices = [v for v in vertices if check_point(v[0], v[1])]

    z_values = [x1 + 2 * x2 for (x1, x2) in feasible_vertices]

    max_z = max(z_values)
    min_z = min(z_values)
    max_point = feasible_vertices[z_values.index(max_z)]
    min_point = feasible_vertices[z_values.index(min_z)]

    print("Задача 1 (графический метод):")
    print(f"  Допустимые вершины: {feasible_vertices}")
    print(f"  Значения z: {z_values}")
    print(f"  Максимум: z = {max_z} в точке {max_point}")
    print(f"  Минимум: z = {min_z} в точке {min_point}")

    x1_vals = np.linspace(0, 12, 400)

    plt.figure(figsize=(10, 8))
    plt.plot(x1_vals, line1(x1_vals), 'r-', label='2x1 - 5x2 = -10')
    plt.plot(x1_vals, line2(x1_vals), 'g-', label='4x1 + 5x2 ≤ 40')
    plt.plot(x1_vals, line3(x1_vals), 'b-', label='x1 + 5x2 ≥ 5')
    plt.axvline(x=0, color='k', linestyle='--', label='x1 ≥ 0')
    plt.axhline(y=0, color='k', linestyle='--', label='x2 ≥ 0')

    x1_grid, x2_grid = np.meshgrid(np.linspace(0, 12, 200), np.linspace(0, 10, 200))
    feasible = ((2 * x1_grid - 5 * x2_grid >= -10) &
                (4 * x1_grid + 5 * x2_grid <= 40) &
                (x1_grid + 5 * x2_grid >= 5) &
                (x1_grid >= 0) &
                (x2_grid >= 0))

    plt.imshow(feasible, extent=[0, 12, 0, 10], origin='lower', alpha=0.3, cmap='Greens')

    for v in feasible_vertices:
        plt.plot(v[0], v[1], 'ro', markersize=8)

    plt.plot(max_point[0], max_point[1], 'm*', markersize=15, label=f'Max z={max_z} at {max_point}')
    plt.plot(min_point[0], min_point[1], 'c*', markersize=15, label=f'Min z={min_z} at {min_point}')

    plt.xlim(-1, 12)
    plt.ylim(-1, 10)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Графический метод (задача 1)')
    plt.legend()
    plt.grid(True)
    plt.show()

    return max_z, min_z, max_point, min_point


def simplex_method():
    print("\nЗадача 2 (симплекс-метод):")
    table = np.array([
        [1, 2, 1, 1, 0, 0, 10],
        [2, 1, 2, 0, 1, 0, 6],
        [3, 1, 2, 0, 0, 1, 12],
        [3, -4, 1, 0, 0, 0, 0]
    ], dtype=float)

    basis = [3, 4, 5]
    n_vars = 6

    iter_count = 0
    while True:
        iter_count += 1
        if iter_count > 10:
            print("Превышено максимальное количество итераций!")
            break

        print(f"\n  Итерация {iter_count}")
        print("  Таблица:")
        for i in range(len(table)):
            if i < 3:
                print(f"  x{basis[i] + 1}: {table[i]}")
            else:
                print(f"  z: {table[i]}")

        z_row = table[-1, :-1]
        if np.all(z_row >= -1e-9):
            print("  Решение оптимально!")
            break
        col = np.argmin(z_row)

        ratios = []
        for i in range(len(table) - 1):
            if table[i, col] > 1e-9:
                ratios.append(table[i, -1] / table[i, col])
            else:
                ratios.append(np.inf)

        if all(r == np.inf for r in ratios):
            print("  Задача неограниченна!")
            break

        row = np.argmin(ratios)

        print(f"  Разрешающий столбец: x{col + 1}")
        print(f"  Разрешающая строка: строка {row + 1} (x{basis[row] + 1})")
        print(f"  Разрешающий элемент: {table[row, col]}")

        pivot = table[row, col]
        table[row, :] /= pivot

        for i in range(len(table)):
            if i != row:
                factor = table[i, col]
                table[i, :] -= factor * table[row, :]

        basis[row] = col

    solution = np.zeros(n_vars)
    for i, var_idx in enumerate(basis):
        if var_idx < n_vars:
            solution[var_idx] = table[i, -1]

    x1, x2, x3 = solution[0], solution[1], solution[2]
    z_max = -table[-1, -1]

    print(f"\n  Решение: x1 = {x1:.6f}, x2 = {x2:.6f}, x3 = {x3:.6f}")
    print(f"  Максимальное значение: z = {z_max:.6f}")

    return x1, x2, x3, z_max


def transport_problem():
    print("\nЗадача 3 (транспортная задача):")

    a = np.array([15, 15, 15, 15])
    b = np.array([11, 11, 11, 11, 16])
    C = np.array([
        [17, 20, 29, 26, 25],
        [3, 4, 5, 15, 24],
        [19, 2, 22, 4, 13],
        [20, 27, 1, 17, 19]
    ])

    print(f"  Сумма запасов: {a.sum()}, сумма потребностей: {b.sum()}")
    if a.sum() != b.sum():
        print("  Задача несбалансированна!")
        return None

    m, n = C.shape

    print("\n  Построение начального плана методом наименьшей стоимости:")
    X = np.array([
        [0, 0, 0, 0, 15],
        [11, 0, 0, 4, 0],
        [0, 11, 0, 4, 0],
        [0, 0, 11, 3, 1]
    ])

    print("  Начальный план:")
    print(X)

    print(f"  Сумма по строкам (запасы): {X.sum(axis=1)}")
    print(f"  Сумма по столбцам (потребности): {X.sum(axis=0)}")
    def calculate_potentials(X, C):
        m, n = X.shape
        u = np.full(m, np.nan)
        v = np.full(n, np.nan)

        u[0] = 0

        changed = True
        while changed:
            changed = False

            for i in range(m):
                if not np.isnan(u[i]):
                    for j in range(n):
                        if X[i, j] > 0 and np.isnan(v[j]):
                            v[j] = C[i, j] - u[i]
                            changed = True

            for j in range(n):
                if not np.isnan(v[j]):
                    for i in range(m):
                        if X[i, j] > 0 and np.isnan(u[i]):
                            u[i] = C[i, j] - v[j]
                            changed = True

        return u, v

    def check_optimality(X, C):
        u, v = calculate_potentials(X, C)
        delta = np.zeros((m, n))
        min_delta = 0
        min_i, min_j = -1, -1

        for i in range(m):
            for j in range(n):
                if X[i, j] == 0:
                    delta[i, j] = C[i, j] - (u[i] + v[j])
                    if delta[i, j] < min_delta:
                        min_delta = delta[i, j]
                        min_i, min_j = i, j

        has_negative = min_delta < -1e-9
        return u, v, delta, has_negative, min_i, min_j, min_delta

    def find_cycle(X, start_i, start_j):
        m, n = X.shape
        queue = deque()
        queue.append((start_i, start_j, [(start_i, start_j)], True))
        queue.append((start_i, start_j, [(start_i, start_j)], False))

        visited_states = set()

        while queue:
            i, j, path, move_horizontal = queue.popleft()

            state = (i, j, move_horizontal)
            if state in visited_states:
                continue
            visited_states.add(state)

            if len(path) > 3 and (i, j) == (start_i, start_j):
                if len(path) % 2 == 1:
                    return path

            if move_horizontal:
                for nj in range(n):
                    if nj != j and X[i, nj] > 0:
                        new_path = path + [(i, nj)]
                        queue.append((i, nj, new_path, False))
            else:
                for ni in range(m):
                    if ni != i and X[ni, j] > 0:
                        new_path = path + [(ni, j)]
                        queue.append((ni, j, new_path, True))

        return None

    iteration = 0
    while True:
        iteration += 1
        print(f"\n  Итерация {iteration}:")

        u, v, delta, has_negative, i_min, j_min, delta_min = check_optimality(X, C)

        print(f"  Потенциалы u: {u}")
        print(f"  Потенциалы v: {v}")

        if not has_negative:
            print("  План оптимален!")
            break

        print(f"  Наибольшая отрицательная оценка: Δ[{i_min},{j_min}] = {delta_min:.2f}")
        print(f"  Клетка для ввода: A{i_min + 1}B{j_min + 1}")

        cycle = find_cycle(X, i_min, j_min)
        if cycle is None:
            print("  Цикл не найден!")
            break

        print(f"  Найден цикл: {cycle}")

        cycle_len = len(cycle)

        theta = np.inf
        for k in range(1, cycle_len, 2):
            i, j = cycle[k]
            if X[i, j] < theta:
                theta = X[i, j]

        print(f"  θ = {theta}")

        new_X = X.copy()
        for k in range(cycle_len - 1):
            i, j = cycle[k]
            if k % 2 == 0:
                new_X[i, j] += theta
            else:
                new_X[i, j] -= theta

        if np.any(new_X < -1e-9):
            print("  Ошибка: отрицательные значения после перераспределения!")
            break

        X = new_X

        print(f"  Новый план:")
        print(X)

    total_cost = np.sum(X * C)

    print(f"\n  Оптимальный план перевозок:")
    for i in range(m):
        for j in range(n):
            if X[i, j] > 0:
                print(f"    A{i + 1} → B{j + 1}: {X[i, j]} тонн (стоимость {C[i, j]} руб/тонн)")

    print(f"\n  Минимальная стоимость: {total_cost}")

    return X, total_cost


def main():
    print()
    print("Лабораторная работа №7: Оптимизация")
    print("Вариант 1")
    print()

    print("\n1. Графический метод:")
    max_z, min_z, max_point, min_point = solve_graphical()

    print("\n2. Симплекс-метод:")
    x1, x2, x3, z_max = simplex_method()

    print("\n3. Транспортная задача:")
    X_opt, total_cost = transport_problem()

    print()
    print("Итоговые результаты:")
    print(f"Задача 1:")
    print(f"  Максимум: z = {max_z} в точке {max_point}")
    print(f"  Минимум: z = {min_z} в точке {min_point}")
    print()
    print(f"Задача 2:")
    print(f"  Решение: x1 = {x1:.2f}, x2 = {x2:.2f}, x3 = {x3:.2f}")
    print(f"  Максимальное значение: z = {z_max:.2f}")
    print()
    print(f"Задача 3:")
    print(f"  Минимальная стоимость: {total_cost}")


if __name__ == "__main__":
    main()