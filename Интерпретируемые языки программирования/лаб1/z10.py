#Задание 10. Дан список строк с клавиатуры. Упорядочить по количеству слов в строке.
print("Задание 10")
lines = []
while True:
    line = input("Введите строку. Для завершения введите пустую строку: ").strip()
    if line == "":
        break
    lines.append(line)

sorted_strings = sorted(lines, key=lambda s: len(s.split()))
print("Упорядоченные строки")
for i, string in enumerate(sorted_strings, 1):
    print(f"{i}. '{string}' (слов: {len(string.split())})")