import numpy as np
import matplotlib.pyplot as plt
n = 3
def f(x):
    if x <= n:
        return (10 * x) / n
    else:
        return 10 * (x - 20) / (n - 20)

a, b = 0, 20
N = 1000

x_point = np.random.uniform(a, b, N)
y_point = np.random.uniform(0, 10, N)

f_vals = np.array([f(x) for x in x_point])
inside = y_point <= f_vals
M = np.sum(inside)

S_prymougol = 10 * 20

pribl_s = M / N * S_prymougol
S = 10 * 20 / 2
absolute_pogr = abs(pribl_s - S)
otnos_pogr = absolute_pogr / S

print(f"Приближённая площадь: {pribl_s:.4f}")
print(f"Точная площадь: {S:.4f}")
print(f"Абсолютная погрешность: {absolute_pogr:.4f}")
print(f"Относительная погрешность: {otnos_pogr:.4%}")

x_vals = np.linspace(a, b, 200)
y_vals = [f(x) for x in x_vals]

plt.figure(figsize=(7,5))
plt.plot(x_vals, y_vals, 'r-', label='y = f(x)')
plt.scatter(x_point[inside], y_point[inside], color='blue',s = 5, label='Внутри')
plt.scatter(x_point[~inside], y_point[~inside], color='grey', s=5, label='Снаружи')
plt.title("Площадь треугольника методом Монте-Карло")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()