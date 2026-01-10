#Задание 5. Дана строка. Необходимо найти все даты, которые описаны в виде "31 февраля 2007".
print("Задание 5")
import re
def find_dates(text):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

    months_pattern = '|'.join(months)
    pattern = fr'\b(\d{{1,2}})\s+({months_pattern})\s+(\d{{4}})\b'

    dates = re.findall(pattern, text)
    return dates

text = str(input("Введите строку: ", ))
dates = find_dates(text)
print("Найденные даты:")
for day, month, year in dates:
    print(f"{day} {month} {year}")