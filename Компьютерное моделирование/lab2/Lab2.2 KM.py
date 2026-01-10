import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

n = 3
N = 1000
a, b = 0, 5

def f(x):
    return (11 - n * np.sin(x) ** 2) ** (1/2)

x_point = np.random.uniform(a, b, N)
y_point = np.random.uniform(0, n, N)
M = np.sum(y_point <= f(x_point))

f_value = np.array([f(x) for x in x_point])

pribl_znach = (b - a) * n * M / N

tochn_znach, _ = quad(f, a, b)
absolute_pogr = abs(pribl_znach - tochn_znach)
otnos_pogr = absolute_pogr / abs(tochn_znach)

print(f"Приближённое значение интеграла: {pribl_znach:.4f}")
print(f"Точное значение интеграла: {tochn_znach:.4f}")
print(f"Абсолютная погрешность: {absolute_pogr:.4f}")
print(f"Относительная погрешность: {otnos_pogr:.4%}")

x_vals = np.linspace(a, b, 400)
plt.plot(x_vals, f(x_vals), 'r', label='f(x)')
plt.scatter(x_point[y_point <= f(x_point)], y_point[y_point <= f(x_point)], s=5, color='blue', label='Под графиком')
plt.scatter(x_point[y_point > f(x_point)], y_point[y_point > f(x_point)], s=5, color='grey', label='Над графиком')
plt.title("Интеграл методом Монте-Карло")
plt.legend()
plt.grid(True)
plt.show()