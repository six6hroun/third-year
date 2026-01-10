#Задание 7. Дана строка. Необходимо найти все используемые в ней строчные символы латиницы
print("Задание 7")
import re
text = str(input("Введите строку: ", ))
def chet(text):
    return len(re.findall(r'[a-z]', text))
print('№7',chet(text))