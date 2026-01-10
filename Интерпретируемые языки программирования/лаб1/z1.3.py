#Найти НОД максимального нечетного непростого делителя числа и произведения цифр данного числа
def delitel (a):
    max = 1
    for i in range(1, a+1):
        if (a % i == 0 and i % 2 == 1):
            cnt=0
            for j in range(1, i+1):
                if (i % j == 0):
                    cnt += 1
            if (cnt != 2):
                if (i > max):
                    max = i
    return max

def proizved (a):
    s = 1
    un = a
    while (un > 0):
        first = un % 10
        s *= first
        un = un // 10
    return s

def del_chisl (a,b):
    max = 1
    if (a < b):
        for i in range(1, a+1):
            if (a % i == 0 and b % i == 0):
                if (i > max): max = i
    else:
        for i in range(1, b+1):
            if (a % i == 0 and b % i == 0):
                if (i > max): max = i
    return max
t = int(input('Введите число - ', ))
print(del_chisl(delitel(t), proizved(t)))
print('\n')