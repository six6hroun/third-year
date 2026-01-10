#Задание 13. Отсортировать строки в порядке увеличения разницы между количеством сочетаний
#«гласная-согласная» и «согласная-гласная» в строке.
print("Задание 13")
glasnie = "аеёиоуыэюя"
soglasnie = "бвгджзйклмнпрстфхцчшщ"
lines = []
print("Введите строки (пустая строка - конец):")
while True:
    s = input().lower()
    if s == "":
        break
    lines.append(s)

def count_difference(s):
    gs = 0
    sg = 0

    for i in range(len(s) - 1):
        first = s[i]
        second = s[i + 1]

        if first in glasnie and second in soglasnie:
            gs += 1
        elif first in soglasnie and second in glasnie:
            sg += 1

    return abs(gs - sg)

result = sorted(lines, key=count_difference)
print("\nРезультат:")
for s in result:
    raz = count_difference(s)
    print(f"{s} (разница: {raz})")