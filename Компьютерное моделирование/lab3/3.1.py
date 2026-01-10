print("Метод серединных квадратов Неймана\n")

def neumann(r_0, n):
    results = []
    current = r_0
    print(f"Начальное значение: R0 = {current}")
    print(f"Количество чисел: N = {n}")
    print("\nПроцесс генерации:")
    print("i\tRᵢ\t\t(Rᵢ)²\t\tСредние цифры\tRᵢ₊₁")
    print("-" * 45)

    for i in range(n + 1):
        if i < n:
            squared = current ** 2
            squared_str = f"{squared:.8f}"[2:]
            while len(squared_str) < 8:
                squared_str += '0'
            middle = squared_str[2:6]
            next_val = float('0.' + middle)
            print(f"{i}\t{current:.3f}\t{squared:.6f}\t{middle}\t\t\t{next_val:.3f}")
            results.append(current)
            current = next_val
        else:
            results.append(current)
            print(f"{i}\t{current:.3f}\t\t\t\t\t")

    return results

R_0 = 0.583
n = 10
result = neumann(R_0, n)
print(f"\nИтоговая последовательность ({len(result)} чисел):")
for i, val in enumerate(result):
    print(f"R{i} = {val:.3f}")