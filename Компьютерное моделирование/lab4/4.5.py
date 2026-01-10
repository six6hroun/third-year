import math
import random
import matplotlib.pyplot as plt
import numpy as np
def generate_uniform(a, b, n):
    return [a + (b - a) * random.random() for _ in range(n)]

def generate_exponential(lambd, n):
    return [-math.log(random.random()) / lambd for _ in range(n)]

def generate_normal(mu, sigma, n):
    numbers = []
    for _ in range(n):
        s = sum(random.random() for _ in range(12))
        z = s - 6
        x = mu + sigma * z
        numbers.append(x)
    return numbers

a = 1
b = 6
lambd = 1
mu = 0
sigma = 3
N = 1000

uniform_sample = generate_uniform(a, b, N)
exponential_sample = generate_exponential(lambd, N)
normal_sample = generate_normal(mu, sigma, N)

fig1, axes1 = plt.subplots(1, 3, figsize=(15, 5))
fig1.suptitle('Диаграммы накопленных частот (Эмпирические функции распределения)', fontsize=14)

sorted_uniform = np.sort(uniform_sample)
y_uniform = np.arange(1, N + 1) / N
axes1[0].step(sorted_uniform, y_uniform, where='post', color='blue')
axes1[0].set_title(f'Равномерное U({a},{b})', fontsize=12)
axes1[0].set_xlabel('x')
axes1[0].set_ylabel('F(x)')
axes1[0].grid(True, alpha=0.3)

sorted_exp = np.sort(exponential_sample)
y_exp = np.arange(1, N + 1) / N
axes1[1].step(sorted_exp, y_exp, where='post', color='green')
axes1[1].set_title(f'Экспоненциальное Exp(λ={lambd})', fontsize=12)
axes1[1].set_xlabel('x')
axes1[1].set_ylabel('F(x)')
axes1[1].grid(True, alpha=0.3)

sorted_normal = np.sort(normal_sample)
y_normal = np.arange(1, N + 1) / N
axes1[2].step(sorted_normal, y_normal, where='post', color='red')
axes1[2].set_title(f'Нормальное N({mu},{sigma})', fontsize=12)
axes1[2].set_xlabel('x')
axes1[2].set_ylabel('F(x)')
axes1[2].grid(True, alpha=0.3)

fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle('Гистограммы распределений', fontsize=14)


# Функция для расчета количества интервалов по формуле из задания
def calculate_intervals(n):
    K = 1 + 3.2 * math.log10(n)
    return int(round(K))

K_uniform = calculate_intervals(N)
K_exp = calculate_intervals(N)
K_normal = calculate_intervals(N)

print(f"Количество интервалов для гистограмм: K = {K_uniform}")

axes2[0].hist(uniform_sample, bins=K_uniform, density=True, alpha=0.7, color='blue', edgecolor='black')
axes2[0].set_title(f'Равномерное U({a},{b}), K={K_uniform}', fontsize=12)
axes2[0].set_xlabel('x')
axes2[0].set_ylabel('Плотность')
axes2[0].grid(True, alpha=0.3)

axes2[1].hist(exponential_sample, bins=K_exp, density=True, alpha=0.7, color='green', edgecolor='black')
axes2[1].set_title(f'Экспоненциальное Exp(λ={lambd}), K={K_exp}', fontsize=12)
axes2[1].set_xlabel('x')
axes2[1].set_ylabel('Плотность')
axes2[1].grid(True, alpha=0.3)

axes2[2].hist(normal_sample, bins=K_normal, density=True, alpha=0.7, color='red', edgecolor='black')
axes2[2].set_title(f'Нормальное N({mu},{sigma}), K={K_normal}', fontsize=12)
axes2[2].set_xlabel('x')
axes2[2].set_ylabel('Плотность')
axes2[2].grid(True, alpha=0.3)
plt.show()