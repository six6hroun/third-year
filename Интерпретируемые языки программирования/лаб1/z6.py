#Задание 6. Дана строка. Необходимо найти общее количество русских символов
import re
print('Задание 6')
text = str(input("Введите строку: ", ))
def chet(text):
    return len(re.findall(r'[А-Яа-яЁё]', text))
print('№6',chet(text))