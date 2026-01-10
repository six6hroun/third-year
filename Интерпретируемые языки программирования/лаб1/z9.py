#Задание 9. Прочитать список строк с клавиатуры. Упорядочить по длине строки.
print("Задание 9")
lines = []
while True:
    line = input("Введите строку. Для завершения введите пустую строку: ").strip()
    if line == "":
        break
    lines.append(line)

sorted_lines = sorted(lines, key=len)
print("Задание 9. Упорядоченный список строк: ", sorted_lines)