#Задания 16. Дан целочисленный массив и натуральный индекс (число, меньшее
#размера массива). Необходимо определить является ли элемент по указанному
#индексу локальным минимумом.
print("Задание 16")
def is_local_minimum(array, index):
    if index < 0 or index >= len(array):
        print(f"Индекс должен быть в диапазоне [0, {len(array)-1}]")
    if array[index] < array[index-1] and array[index] < array[index+1]:
        return True
    else:
        return False

array = []
while True:
    element = input("Введите элементы массива. Для окончания ввода, введите пустую строку: " )
    if element == "":
        break
    array.append(int(element))

i = int(input("Введите индекс, который необоходимо проверить на локальный минимум в массиве - " ))
print (is_local_minimum(array, i))