#Находит три числа в массиве, где расстояние между любыми двумя числами ≥ k, и их произведение максимально.
def sort(file):
    with open(file, 'r') as f:
        n, k = map(int, f.readline().split())
        arr = [int(f.readline()) for _ in range(n)]

    left_max = [0] * n
    for i in range(n):
        if i >= k:
            left_max[i] = max(left_max[i-1], arr[i-k])
        else:
            left_max[i] = 0

    right_max = [0] * n
    for i in range(n-1, -1, -1):
        if i <= n-1-k:
            if i == n-1:
                right_max[i] = arr[i+k]
            else:
                right_max[i] = max(right_max[i+1], arr[i+k])
        else:
            right_max[i] = 0

    max_product = 0
    for j in range(k, n - k):
        left_val = left_max[j]
        right_val = right_max[j]
        if left_val > 0 and right_val > 0:
            product = left_val * arr[j] * right_val
            if product > max_product:
                max_product = product

    return max_product % (10**6 + 1) if max_product > 0 else 0


result_A = sort(r'C:\учеба\Интерпретируемые языки программирования\путь\27-168a.txt')
result_B = sort(r'C:\учеба\Интерпретируемые языки программирования\путь\27-168b.txt')
print(f"Результаты: {result_A} {result_B}")