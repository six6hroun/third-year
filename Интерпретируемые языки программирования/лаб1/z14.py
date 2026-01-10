#Задание 14. Отсортировать строки в порядке увеличение квадратичного отклонения частоты
#встречаемости самого распространенного символа в наборе строк от частоты
#его встречаемости в данной строке.
print("Задание 14")
lines = []
print("Введите строки (пустая строка - конец):")
while True:
    s = input()
    if s == "":
        break
    lines.append(s)

all_chars = "".join(lines)
sam_chast_char = max(set(all_chars), key=all_chars.count)
chastota_v_nabore = all_chars.count(sam_chast_char) / len(all_chars)

def sort(s):
    char_chastota_string = s.count(sam_chast_char) / len(s)
    return (char_chastota_string - chastota_v_nabore) ** 2

lines.sort(key=sort)
print(f"\nСамый частый символ: '{sam_chast_char}'")
print(f"Его общая частота: {chastota_v_nabore:.3f}")
print("\nОтсортированные строки:")
for s in lines:
    if sam_chast_char in s:
        freq_in_s = s.count(sam_chast_char) / len(s)
        dev = (freq_in_s - chastota_v_nabore) ** 2
        print(f"{s} (отклонение: {dev:.4f})")
    else:
        print(f"{s} (символ отсутствует)")