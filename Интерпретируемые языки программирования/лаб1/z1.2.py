#Найти произведение цифр числа не делящихся на 5
def proiz_c_ch (a):
    b = 1
    while a > 0:
        d = a % 10
        if d % 5 != 0:
            b *= d
        a //= 10
    return b
t = int(input('Введите число - ', ))
print (proiz_c_ch(t))