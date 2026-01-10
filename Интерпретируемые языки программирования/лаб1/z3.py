#Задание 3. Дана строка в которой записаны слова через пробел. Необходимо
#посчитать количество слов с четным количеством символов.
print("Задание 3")
text = str(input("Введите строку через пробел: ", ))
def chet(text):
    b = text.split()
    count = 0
    for a in b:
        if len(a) % 2 == 0: count +=1
    return count
print('№3', chet(text))