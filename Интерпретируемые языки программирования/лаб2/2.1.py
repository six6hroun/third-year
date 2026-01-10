#Даны два списка чисел. Найдите все числа, которые входят как в первый,
#так и во второй список и выведите их в порядке возрастания.
from numpy.ma.core import append

l1 = []
g = 1
print("Введите элементы массива L1 (для завершения ввода ничего не вводите и нажмите enter)")
while True:
    element = input(f"Элемент {g} - ")
    if element == "":
        break
    l1.append(element)
    g += 1

l2 = []
k = 1
print("Введите элементы массива L2 (для завершения ввода ничего не вводите и нажмите enter)")
while True:
    element = input(f"Элемент {k} - ")
    if element == "":
        break
    l2.append(element)
    k += 1

l3 = []
for i in l1:
    for j in l2:
        if i == j:
            l3.append(i)
print ("Элементы массива в порядке возрастания", sorted(l3))