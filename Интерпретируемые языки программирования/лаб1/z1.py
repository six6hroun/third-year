#Задание 1. Составить 3 функции для работы с цифрами или делителями числа на основании варианта. Вариант 3.
#Максимальный простой делитель
print("Задание 1")
def simple(a):
    cnt = 0
    for i in range(1, a + 1):
        if a % i == 0:
            cnt += 1
    if cnt == 2:
        return True
    else:
        return False

def max(a):
    max_prime = 0
    for i in range(1, a + 1):
        if a % i == 0 and simple(i):
            if i > max_prime:
                max_prime = i
    return max_prime
t = int(input('Введите число - ', ))
print(max(t))