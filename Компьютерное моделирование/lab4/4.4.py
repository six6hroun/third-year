import math
import random
import matplotlib.pyplot as plt
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

def calculate_mean(sample):
    return sum(sample) / len(sample)

def calculate_variance(sample):
    mean = calculate_mean(sample)
    n = len(sample)
    return sum((x - mean) ** 2 for x in sample) / (n - 1)

a = 1
b = 6
lambd = 1
mu = 0
sigma = 3

M_uniform = (a + b) / 2
D_uniform = ((b - a) ** 2) / 12
M_exp = 1 / lambd
D_exp = 1 / (lambd ** 2)
M_norm = mu
D_norm = sigma ** 2

print("Теоретические значения из задания 2:")
print(f"Равномерное: Mатематическое ожидание={M_uniform:.3f}, Дисперсия={D_uniform:.3f}")
print(f"Экспоненциальное: Mатематическое ожидание={M_exp:.3f}, Дисперсия={D_exp:.3f}")
print(f"Нормальное: Mатематическое ожидание={M_norm:.3f}, Дисперсия={D_norm:.3f}")

N_big = 1000
uniform_big = generate_uniform(a, b, N_big)
exp_big = generate_exponential(lambd, N_big)
norm_big = generate_normal(mu, sigma, N_big)
sizes = [10, 20, 50, 100, 1000]

uniform_means, uniform_vars = [], []
exp_means, exp_vars = [], []
norm_means, norm_vars = [], []

print("\nРавномерное распределение:")
for n in sizes:
    sample = uniform_big[:n]
    m = calculate_mean(sample)
    d = calculate_variance(sample)
    uniform_means.append(m)
    uniform_vars.append(d)
    err_m = abs(m - M_uniform) / M_uniform * 100
    err_d = abs(d - D_uniform) / D_uniform * 100
    print(f"N={n}: Mатематическое ожидание={m:.3f} (отличае от теоретического значения: {err_m:.1f}%), Дисперсия={d:.3f} ({err_d:.1f}%)")

print("\nЭкспоненциальное распределение:")
for n in sizes:
    sample = exp_big[:n]
    m = calculate_mean(sample)
    d = calculate_variance(sample)
    exp_means.append(m)
    exp_vars.append(d)

    err_m = abs(m - M_exp) / M_exp * 100
    err_d = abs(d - D_exp) / D_exp * 100
    print(f"N={n}: Mатематическое ожидание={m:.3f} (отличае от теоретического значения: {err_m:.1f}%), Дисперсия={d:.3f} ({err_d:.1f}%)")

# Нормальное распределение
print("\nНормальное распределение:")
for n in sizes:
    sample = norm_big[:n]
    m = calculate_mean(sample)
    d = calculate_variance(sample)
    norm_means.append(m)
    norm_vars.append(d)

    err_m = abs(m - M_norm)
    err_d = abs(d - D_norm) / D_norm * 100
    print(f"N={n}: Mатематическое ожидание={m:.3f} (отличае от теоретического значения: {err_m:.3f}), Дисперсия={d:.3f} ({err_d:.1f}%)")

plt.figure(figsize=(15, 10))
plt.subplot(2, 3, 1)
plt.plot(sizes, uniform_means, 'bo-')
plt.axhline(y=M_uniform, color='r', linestyle='--')
plt.title('Равномерное: мат.ожидание')
plt.xlabel('Объем выборки')
plt.ylabel('Оценка мат.ожидание')
plt.grid(True)
plt.xscale('log')

plt.subplot(2, 3, 2)
plt.plot(sizes, exp_means, 'go-')
plt.axhline(y=M_exp, color='r', linestyle='--')
plt.title('Экспоненциальное: мат.ожидание')
plt.xlabel('Объем выборки')
plt.ylabel('Оценка мат.ожидание')
plt.grid(True)
plt.xscale('log')

plt.subplot(2, 3, 3)
plt.plot(sizes, norm_means, 'ro-')
plt.axhline(y=M_norm, color='r', linestyle='--')
plt.title('Нормальное: мат.ожидание')
plt.xlabel('Объем выборки')
plt.ylabel('Оценка мат.ожидание')
plt.grid(True)
plt.xscale('log')

# График для дисперсий
plt.subplot(2, 3, 4)
plt.plot(sizes, uniform_vars, 'bs-')
plt.axhline(y=D_uniform, color='r', linestyle='--')
plt.title('Равномерное: дисперсия')
plt.xlabel('Объем выборки')
plt.ylabel('Оценка дисперсия')
plt.grid(True)
plt.xscale('log')

plt.subplot(2, 3, 5)
plt.plot(sizes, exp_vars, 'gs-')
plt.axhline(y=D_exp, color='r', linestyle='--')
plt.title('Экспоненциальное: дисперсия')
plt.xlabel('Объем выборки')
plt.ylabel('Оценка дисперсия')
plt.grid(True)
plt.xscale('log')

plt.subplot(2, 3, 6)
plt.plot(sizes, norm_vars, 'rs-')
plt.axhline(y=D_norm, color='r', linestyle='--')
plt.title('Нормальное: дисперсия')
plt.xlabel('Объем выборки')
plt.ylabel('Оценка дисперсия')
plt.grid(True)
plt.xscale('log')
plt.tight_layout()

print("\nОтносительные погрешности для нормального распределения (N=100):")
n_check = 100
sample_check = norm_big[:n_check]
m_check = calculate_mean(sample_check)
d_check = calculate_variance(sample_check)

print(f"\nОценки: Mатематическое ожидание={m_check:.3f}, Дисперсия={d_check:.3f}")
print(f"Теоретические: Mатематическое ожидание: {M_norm:.3f}, Дисперсия: {D_norm:.3f}")
print(f"Относительная погрешность дисперсии: {abs(d_check - D_norm) / D_norm * 100:.1f}%")
plt.show()