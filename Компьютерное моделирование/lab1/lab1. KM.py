import numpy as np
import matplotlib.pyplot as plt

x = np.array([3, 5, 7, 9, 11, 13])
y = np.array([26, 76, 150, 240, 360, 500])
n = len(x)
Sxy = np.sum(x * y)
Sx = np.sum(x)
Sy = np.sum(y)
Sxx = np.sum(x ** 2)
al = (n * Sxy - Sx * Sy) / (n * Sxx - Sx * Sx)
bl = 1/n * Sy - al * 1/n * Sx
print ("Значения а, b линейной функции")
print (f"{al:.2f}, {bl:.2f}")


Slnx = np.sum(np.log(x))
Slny = np.sum(np.log(y))
Slnxy = np.sum(np.log(x) * np.log(y))
Slnxx = np.sum(np.log(x) ** 2)
ast = (n * Slnxy - Slnx * Slny) / (n * Slnxx - Slnx * Slnx)
lnb = 1/n * Slny - ast * 1/n * Slnx
bst = np.exp(lnb)
print("Значения а, b степенной функции")
print(f"{ast:.2f}, {bst:.2f}")

Sxlny = np.sum(x * np.log(y))
Sx = np.sum(x)
Slny = np.sum(np.log(y))
Sxx = np.sum(x ** 2)
ap = (n * Sxlny - Sx * Slny) / (n * Sxx - Sx * Sx)
lnb = 1/n * Slny - ap * 1/n * Sx
bp = np.exp(lnb)
print("Значения а, b показательной функции")
print(f"{ap:.2f}, {bp:.2f}")

Sx4 = np.sum(x ** 4)
Sx3 = np.sum(x ** 3)
Sx2 = np.sum(x ** 2)
Sx1 = np.sum(x)
Sx2y = np.sum(x ** 2 * y)
Sx1y = np.sum(x * y)
Sy1 = np.sum(y)

matr = np.array ([
    [Sx4, Sx3, Sx2],
    [Sx3, Sx2, Sx1],
    [Sx2, Sx1, n]])
headopred = np.linalg.det(matr)
print("Основной определитель")
print(headopred)

matr1 = np.array ([
    [Sx2y, Sx3, Sx2],
    [Sx1y, Sx2, Sx1],
    [Sy1, Sx1, n]])
headopred1 = np.linalg.det(matr1)
print("Вспомогательный определитель")
print(headopred1)

matr2 = np.array ([
    [Sx4, Sx2y, Sx2],
    [Sx3, Sx1y, Sx1],
    [Sx2, Sy1, n]])
headopred2 = np.linalg.det(matr2)
print("Вспомогательный определитель")
print(headopred2)

matr3 = np.array ([
    [Sx4, Sx3, Sx2y],
    [Sx3, Sx2, Sx1y],
    [Sx2, Sx1, Sy1]])
headopred3 = np.linalg.det(matr3)
print("Вспомогательный определитель")
print(headopred3)

aq = headopred1 / headopred
bq = headopred2 / headopred
cq = headopred3 / headopred

print("Значения а, b, c квадратичной функции")
print(f"{aq:.2f}, {bq:.2f}, {cq:.2f}")


def linenaya(x):
    return al*x + bl
def stepennaya(x):
    return bst * np.pow(x, ast)
def pokazatelnaya(x):
    return bp * np.exp(ap*x)
def quadratichnaya(x):
    return aq*x**2 + bq*x + cq

pogr1 = 0
pogr2 = 0
pogr3 = 0
pogr4 = 0
for i in range(0, 6):
    pogr1 += (y[i] - linenaya(x[i]))**2
    pogr2 += (y[i] - stepennaya(x[i]))**2
    pogr3 += (y[i] - pokazatelnaya(x[i]))**2
    pogr4 += (y[i] - quadratichnaya(x[i]))**2

print("\nпогрешность линейной функции =",round(pogr1, 4),
      "\nпогрешность степенной функции =",round(pogr2, 4),
      "\nпогрешность показательной функции =",round(pogr3, 4),
      "\nпогрешность квадратичной функции =",round(pogr4, 4),)

xx = np.linspace(min(x), max(x), 200)
plt.scatter(x, y, c='black', label="Экспериментальные точки")
plt.plot(xx, linenaya(xx), label="Линейная")
plt.plot(xx, stepennaya(xx), label="Степенная")
plt.plot(xx, pokazatelnaya(xx), label="Показательная")
plt.plot(xx, quadratichnaya(xx), label="Квадратичная")
plt.legend()
plt.grid(True)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Аппроксимация МНК")
plt.show()