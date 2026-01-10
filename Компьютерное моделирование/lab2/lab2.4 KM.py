import numpy as np
import matplotlib.pyplot as plt

n = 3
A = 11 + n
B = 11 - n
N = 10000

def pk(ugol):
    return np.sqrt(A * np.cos(ugol)**2 + B * np.sin(ugol)**2)

max_r = 5
x_rand = np.random.uniform(-max_r, max_r, N)
y_rand = np.random.uniform(-max_r, max_r, N)

ugol_rand = np.arctan2(y_rand, x_rand)
rastoyanie_centre_point = np.sqrt(x_rand**2 + y_rand**2)

inside = rastoyanie_centre_point < pk(ugol_rand)
M = np.sum(inside)

S_rect = (max_r * 2) ** 2
S_mc = M / N * S_rect

print(f"Приближённая площадь фигуры: {S_mc:.4f}")

ugol_vals = np.linspace(0, 2*np.pi, 400)
r_vals = pk(ugol_vals)
x_curve = r_vals * np.cos(ugol_vals)
y_curve = r_vals * np.sin(ugol_vals)

plt.figure(figsize=(6,6))
plt.plot(x_curve, y_curve, 'r', label='Граница фигуры')
plt.scatter(x_rand[inside], y_rand[inside], color='blue', s=5, label='Внутри')
plt.scatter(x_rand[~inside], y_rand[~inside], color='grey', s=5, label='Снаружи')
plt.title("Площадь фигуры в полярных координатах")
plt.axis('equal')
plt.legend()
plt.grid(True)
plt.show()