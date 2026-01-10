#Задания 18. Дан целочисленный массив. Необходимо вывести вначале его
#элементы с четными индексами, а затем – с нечетными.
print("Задание 18")
array = []
while True:
    element = input("Введите элементы массива. Для окончания ввода, введите пустую строку: " )
    if element == "":
        break
    array.append(int(element))

chet = []
nechet = []
for i in range(0, len(array)):
    if i % 2 == 0:
        chet.append(array[i])
    else:
        nechet.append(array[i])
print ("Элементы с четными индексами: ",  chet)
print ("Элементы с нечетными индексами: ",  nechet)