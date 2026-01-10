import random
def random_number():
    N = 20
    filename = r'C:\учеба\Интерпретируемые языки программирования\test.txt'
    with open(filename, 'w') as f:
        for _ in range(N):
            num = random.randint(-10, 10)
            f.write(f"{num}\n")

    with open(filename, 'r') as f:
        numbers = [int(line.strip()) for line in f]

    count = 0
    seen = set()
    for num in numbers:
        if -num in seen:
            count += 1
        seen.add(num)

    print(f"Количество пар противоположных чисел: {count}")

random_number()