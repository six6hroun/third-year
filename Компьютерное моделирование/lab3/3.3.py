print("Алгоритм Лемера\n")

def lemar(r_0, g, n):
    results = [r_0]
    current = r_0
    print(f"Начальное значение: R0 = {r_0}")
    print(f"Множитель: g = {g}")
    print(f"Количество чисел: N = {n}")
    print("\nПроцесс генерации:")
    print("i\tRᵢ\t\tg * Rᵢ\t\tДробная часть (Rᵢ₊₁)")
    print("-" * 45)

    for i in range(n):
        temp = g * current
        next_val = temp - int(temp)
        print(f"{i}\t{current:.3f}\t{temp:.3f}\t\t{next_val:.3f}")
        results.append(next_val)
        current = next_val

    return results

r_0 = 0.585
g = 927
n = 10
result = lemar(r_0, g, n)
print(f"\nИтоговая последовательность ({len(result)} чисел):")
for i, val in enumerate(result):
    print(f"R{i} = {val:.6f}")