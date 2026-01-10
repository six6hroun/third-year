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

def uniform_pdf(x, a, b):
    return 1 / (b - a) if a <= x <= b else 0

def exponential_pdf(x, lambd):
    return lambd * math.exp(-lambd * x) if x >= 0 else 0

def normal_pdf(x, mu, sigma):
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)

def uniform_cdf(x, a, b):
    if x < a:
        return 0
    elif x > b:
        return 1
    else:
        return (x - a) / (b - a)

def exponential_cdf(x, lambd):
    return 1 - math.exp(-lambd * x) if x >= 0 else 0

def normal_cdf(x, mu, sigma):
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

a = 1
b = 6
lambd = 1
mu = 0
sigma = 3
N = 1000

uniform_sample = generate_uniform(a, b, N)
exponential_sample = generate_exponential(lambd, N)
normal_sample = generate_normal(mu, sigma, N)
K = int(round(1 + 3.2 * math.log10(N)))

fig, axes = plt.subplots(3, 2, figsize=(15, 12))
fig.suptitle('Сравнение эмпирических и теоретических распределений', fontsize=14)

# равномерное распределение
axes[0, 0].hist(uniform_sample, bins=K, density=True, alpha=0.6,
                color='lightblue', edgecolor='black', label='Гистограмма')

x_uniform = np.linspace(a - 0.5, b + 0.5, 1000)
y_uniform_pdf = [uniform_pdf(x, a, b) for x in x_uniform]
axes[0, 0].plot(x_uniform, y_uniform_pdf, 'r-', linewidth=2, label='Теоретическая PDF')

axes[0, 0].set_title(f'Равномерное U({a},{b})', fontsize=12)
axes[0, 0].set_xlabel('x')
axes[0, 0].set_ylabel('Плотность')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# ECDF + CDF
sorted_uniform = np.sort(uniform_sample)
y_uniform_ecdf = np.arange(1, N + 1) / N
axes[0, 1].step(sorted_uniform, y_uniform_ecdf, where='post',
                color='blue', linewidth=1.5, label='ECDF')

x_uniform_cdf = np.linspace(a - 0.5, b + 0.5, 1000)
y_uniform_cdf = [uniform_cdf(x, a, b) for x in x_uniform_cdf]
axes[0, 1].plot(x_uniform_cdf, y_uniform_cdf, 'r-', linewidth=2, label='Теоретическая CDF')

axes[0, 1].set_title(f'Равномерное U({a},{b})', fontsize=12)
axes[0, 1].set_xlabel('x')
axes[0, 1].set_ylabel('F(x)')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# экспон. распределение
axes[1, 0].hist(exponential_sample, bins=K, density=True, alpha=0.6,
                color='lightgreen', edgecolor='black', label='Гистограмма')

x_exp = np.linspace(0, max(exponential_sample), 1000)
y_exp_pdf = [exponential_pdf(x, lambd) for x in x_exp]
axes[1, 0].plot(x_exp, y_exp_pdf, 'r-', linewidth=2, label='Теоретическая PDF')

axes[1, 0].set_title(f'Экспоненциальное Exp(λ={lambd})', fontsize=12)
axes[1, 0].set_xlabel('x')
axes[1, 0].set_ylabel('Плотность')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# ECDF + CDF
sorted_exp = np.sort(exponential_sample)
y_exp_ecdf = np.arange(1, N + 1) / N
axes[1, 1].step(sorted_exp, y_exp_ecdf, where='post',
                color='green', linewidth=1.5, label='ECDF')

x_exp_cdf = np.linspace(0, max(exponential_sample), 1000)
y_exp_cdf = [exponential_cdf(x, lambd) for x in x_exp_cdf]
axes[1, 1].plot(x_exp_cdf, y_exp_cdf, 'r-', linewidth=2, label='Теоретическая CDF')

axes[1, 1].set_title(f'Экспоненциальное Exp(λ={lambd})', fontsize=12)
axes[1, 1].set_xlabel('x')
axes[1, 1].set_ylabel('F(x)')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# нормальное распределение
axes[2, 0].hist(normal_sample, bins=K, density=True, alpha=0.6,
                color='salmon', edgecolor='black', label='Гистограмма')

x_norm = np.linspace(min(normal_sample), max(normal_sample), 1000)
y_norm_pdf = [normal_pdf(x, mu, sigma) for x in x_norm]
axes[2, 0].plot(x_norm, y_norm_pdf, 'r-', linewidth=2, label='Теоретическая PDF')

axes[2, 0].set_title(f'Нормальное N({mu},{sigma})', fontsize=12)
axes[2, 0].set_xlabel('x')
axes[2, 0].set_ylabel('Плотность')
axes[2, 0].legend()
axes[2, 0].grid(True, alpha=0.3)

# ECDF + CDF
sorted_norm = np.sort(normal_sample)
y_norm_ecdf = np.arange(1, N + 1) / N
axes[2, 1].step(sorted_norm, y_norm_ecdf, where='post',
                color='red', linewidth=1.5, label='ECDF')

x_norm_cdf = np.linspace(min(normal_sample), max(normal_sample), 1000)
y_norm_cdf = [normal_cdf(x, mu, sigma) for x in x_norm_cdf]
axes[2, 1].plot(x_norm_cdf, y_norm_cdf, 'r-', linewidth=2, label='Теоретическая CDF')

axes[2, 1].set_title(f'Нормальное N({mu},{sigma})', fontsize=12)
axes[2, 1].set_xlabel('x')
axes[2, 1].set_ylabel('F(x)')
axes[2, 1].legend()
axes[2, 1].grid(True, alpha=0.3)
plt.show()