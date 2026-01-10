#Задание 8. Дана строка. Необходимо найти минимальное из имеющихся в ней целых чисел
print("Задание 8")
text = str(input("Введите строку через пробел: ", ))
array = text.split()
nums = []
for a in array:
    if (a.isdigit()): nums.append(int(a))
min = nums[0]
for a in nums:
    if (a < min):
        min = a

print('№8', min)