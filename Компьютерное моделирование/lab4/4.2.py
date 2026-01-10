import math
import random
def generate_uniform(a, b, n):
    return [a + (b - a) * random.random() for _ in range(n)]

def generate_exponential(lambd, n):
    return [-math.log(random.random()) / lambd for _ in range(n)]

def generate_normal(mu, sigma, n):
    normal_numbers = []
    for _ in range(n):
        s = sum(random.random() for _ in range(12))
        z = s - 6  # ~N(0, 1)
        x = mu + sigma * z  # N(μ, σ)
        normal_numbers.append(x)
    return normal_numbers

def calculate_mean(sample): #выборочное среднее
    return sum(sample) / len(sample)

def calculate_variance(sample): #выборочная дисперсия
    mean = calculate_mean(sample)
    n = len(sample)
    return sum((x - mean) ** 2 for x in sample) / (n - 1)

a = 1
b = 6
lambd = 1
mu = 0
sigma = 3
N = 1000

uniform_sample = generate_uniform(a, b, N)
exponential_sample = generate_exponential(lambd, N)
normal_sample = generate_normal(mu, sigma, N)

print("Оценка")

M_uniform = calculate_mean(uniform_sample)
D_uniform = calculate_variance(uniform_sample)
print(f"\nРавномерное распределение U({a}, {b}):")
print(f"Математическое ожидание = {M_uniform:.4f}")
print(f"Дисперсия = {D_uniform:.4f}")

M_exponential = calculate_mean(exponential_sample)
D_exponential = calculate_variance(exponential_sample)
print(f"\nЭкспоненциальное распределение Exp(λ={lambd}):")
print(f"Математическое ожидание = {M_exponential:.4f}")
print(f"Дисперсия = {D_exponential:.4f}")

M_normal = calculate_mean(normal_sample)
D_normal = calculate_variance(normal_sample)
print(f"\nНормальное распределение N(μ={mu}, σ={sigma}):")
print(f"Математическое ожидание = {M_normal:.4f}")
print(f"Дисперсия = {D_normal:.4f}")

print('\nРезультат')
print(f"\nРавномерное:")
for i in range(5):
    print(f"x{i+1} = {uniform_sample[i]:.4f}")

print(f"\nЭкспоненциальное:")
for i in range(5):
    print(f"x{i+1} = {exponential_sample[i]:.4f}")

print(f"\nНормальное:")
for i in range(5):
    print(f"x{i+1} = {normal_sample[i]:.4f}")