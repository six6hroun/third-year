import numpy as np
A = np.array([[0, 0, 0.3, 0, 0, 0.7],
              [0.1, 0, 0, 0, 0, 0.9],
              [0.1, 0, 0, 0, 0.2, 0.7],
              [0, 0, 0, 0.5, 0.5, 0],
              [0.1, 0.2, 0.2, 0, 0, 0.5],
              [0.1, 0, 0.3, 0, 0.2, 0.4]])
A2 = np.dot(A, A)
print("№1 Матрица перехода за 2 шага")
print(A2)
print()

print("№2 Распределение вероятностей по состояниям после 2-го шага")
v0 = np.array([0, 1, 0, 0, 0, 0])
v1 = v0 @ A
print(f"Распределение после 1 шага v(1): {v1}")
v2 = v1 @ A
print(f"Распределение после 2 шагов v(2): {v2}")

states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
print("Вероятности после 2 шагов:")
for i, state in enumerate(states):
    print(f"  P({state}) = {v2[i]:.3f}")
print(f"Сумма вероятностей: {sum(v2):.1f}")
print()

print ("№3 Стационарное распределение вероятностей по состояниям.")
print()

n = A.shape[0]
system_matrix = np.vstack([A.T - np.eye(n), np.ones(n)])
right_side = np.zeros(n + 1)
right_side[-1] = 1

pi, residuals, rank, s = np.linalg.lstsq(system_matrix, right_side, rcond=None)
pi = pi / np.sum(pi)

states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
print("Стационарные вероятности:")
for i, state in enumerate(states):
    print(f"  π({state}) = {pi[i]:.6f}")

print(f"\nСумма: {sum(pi):.6f}")