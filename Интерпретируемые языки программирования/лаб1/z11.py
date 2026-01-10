#Задание 11. Отсортировать строки в порядке увеличения разницы между частотой наиболее часто
#встречаемого символа в строке и частотой его появления в алфавите.
print("Задание 11")
slovar = {
    'о': 0.090, 'е': 0.072, 'а': 0.062, 'и': 0.062, 'н': 0.053,
    'т': 0.053, 'с': 0.045, 'р': 0.040, 'в': 0.038, 'л': 0.035,
    'к': 0.028, 'м': 0.026, 'д': 0.025, 'п': 0.023, 'у': 0.021,
    'я': 0.018, 'ы': 0.016, 'ь': 0.014, 'г': 0.013, 'з': 0.012,
    'б': 0.012, 'ч': 0.010, 'й': 0.010, 'х': 0.009, 'ж': 0.007,
    'ш': 0.006, 'ю': 0.006, 'ц': 0.004, 'щ': 0.003, 'э': 0.003,
    'ф': 0.002, 'ъ': 0.001, 'ё': 0.001
}

print("Введите строки (для завершения введите пустую строку):")
lines = []
while True:
    s = input()
    if s == "":
        break
    lines.append(s)

def calculate(s):
    char_slovar = {}
    for char in s.lower():
        if char in slovar:
            char_slovar[char] = char_slovar.get(char, 0) + 1

    sam_chast_simvol = max(char_slovar.items(), key=lambda x: x[1])
    char, count = sam_chast_simvol

    chastota = count / len([c for c in s.lower() if c in slovar])
    chastota_slovar = slovar[char]
    difference = abs(chastota - chastota_slovar)
    return difference

sorted_strings = sorted(lines, key=calculate)
print("\nОтсортированные строки:")
for i, string in enumerate(sorted_strings, 1):
    print(f"{i}. {string}")