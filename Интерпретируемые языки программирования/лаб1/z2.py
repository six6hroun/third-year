#Задание 2.Дана строка в которой слова записаны через пробел. Необходимо
#перемешать все слова этой строки в случайном порядке.
import random
print("Задание 2")
text = str(input("Введите строку через пробел: ", ))
def stroka(text):
    word = text.split()
    random.shuffle(word)
    return ' '.join(word)
print('№2',stroka(text))