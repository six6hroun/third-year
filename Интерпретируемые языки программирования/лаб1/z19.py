#Задания 19. Для введенного списка построить два списка L1 и L2, где элементы
#L1 это неповторяющиеся элементы исходного списка, а элемент списка L2 с
#номером i показывает, сколько раз элемент списка L1 с таким номером
#повторяется в исходном.
print("Задание 19")
def new_lists(array):
    L1 = []
    L2 = []
    for i in array:
        if i not in L1:
            L1.append(i)
            L2.append(1)
        else:
            index = L1.index(i)
            L2[index] += 1
    return L1, L2

array = []
while True:
    element = input("Введите элементы массива. Для окончания ввода, введите пустую строку: " )
    if element == "":
        break
    array.append(int(element))

print ("Список L1 и список L2:", new_lists(array))