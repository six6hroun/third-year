#Задание 12. Отсортировать строки в порядке увеличения квадратичного отклонения частоты
#встречаемости самого часто встречаемого в строке символа от частоты его встречаемости в текстах на этом алфавите.
print("Задание 12")
slovar = {
    'о': 0.090, 'е': 0.072, 'а': 0.062, 'и': 0.062, 'н': 0.053,
    'т': 0.053, 'с': 0.045, 'р': 0.040, 'в': 0.038, 'л': 0.035,
    'к': 0.028, 'м': 0.026, 'д': 0.025, 'п': 0.023, 'у': 0.021,
    'я': 0.018, 'ы': 0.016, 'ь': 0.014, 'г': 0.013, 'з': 0.012,
    'б': 0.012, 'ч': 0.010, 'й': 0.010, 'х': 0.009, 'ж': 0.007,
    'ш': 0.006, 'ю': 0.006, 'ц': 0.004, 'щ': 0.003, 'э': 0.003,
    'ф': 0.002, 'ъ': 0.001, 'ё': 0.001
}

lines = []
print("Введите строки (пустая строка - конец):")
while True:
    s = input()
    if s == "":
        break
    lines.append(s)

result = []
for s in lines:
    letters = [c for c in s.lower() if c in slovar]

    char_slovar = {}
    for letter in letters:
        char_slovar[letter] = char_slovar.get(letter, 0) + 1

    most_char = max(char_slovar.items(), key=lambda x: x[1])
    letter, count = most_char

    chastota = count / len(letters)
    chastota_slovar = slovar[letter]
    deviation = (chastota - chastota_slovar) ** 2
    result.append((s, deviation))

result.sort(key=lambda x: x[1])
print("\nРезультат:")
for s, dev in result:
    print(f"{s} (отклонение: {dev:.6f})")