print("Модифицированный метод Неймана\n")

def modified_neumann(r_0, r_1, n):
    results = [r_0, r_1]
    print(f"Начальные значения: R0 = {r_0}, R1 = {r_1}")
    print(f"Количество чисел: N = {n}")
    print("\nПроцесс генерации:")
    print("i\tRᵢ₋₁\tRᵢ\t\tTemp\t\tСредние цифры\tRᵢ₊₁")
    print("-" * 54)

    for i in range(1, n + 1):
        temp = results[i - 1] * results[i]
        temp_str = f"{temp:.8f}"[2:]
        while len(temp_str) < 8:
            temp_str += '0'
        middle = temp_str[2:6]
        next_val = float('0.' + middle)
        print(f"{i}\t{results[i - 1]:.4f}\t{results[i]:.4f}\t{temp:.8f}\t{middle}\t\t\t{next_val:.4f}")
        results.append(next_val)

    return results

r_0 = 0.5836
r_1 = 0.2176
n = 10
result = modified_neumann(r_0, r_1, n)
print(f"\nИтоговая последовательность ({len(result)} чисел):")
for i, val in enumerate(result):
    print(f"R{i} = {val:.4f}")