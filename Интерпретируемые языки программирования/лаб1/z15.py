#Задания 15.  Дан целочисленный массив и натуральный индекс (число, меньшее
#размера массива). Необходимо определить является ли элемент по указанному
#индексу глобальным максимумом.
print("Задание 15")
def is_global_maximum(array, index):
    if index < 0 or index >= len(array):
        print(f"Индекс должен быть в диапазоне [0, {len(array)-1}]")
    global_max = max(array)
    return array[index] == global_max

array = []
while True:
    element = input("Введите элементы массива. Для окончания ввода, введите пустую строку: " )
    if element == "":
        break
    array.append(int(element))

i = int(input("Введите индекс, который необоходимо проверить на глобальный максимум в массиве - " ))
print (is_global_maximum(array, i))