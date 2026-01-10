import csv
from datetime import datetime

MONTHS = {
    'Январь': '01', 'Января': '01',
    'Февраль': '02', 'Февраля': '02',
    'Март': '03', 'Марта': '03',
    'Апрель': '04', 'Апреля': '04',
    'Май': '05', 'Мая': '05',
    'Июнь': '06', 'Июня': '06',
    'Июль': '07', 'Июля': '07',
    'Август': '08', 'Августа': '08',
    'Сентябрь': '09', 'Сентября': '09',
    'Октябрь': '10', 'Октября': '10',
    'Ноябрь': '11', 'Ноября': '11',
    'Декабрь': '12', 'Декабря': '12'
}

def parse_russian_datetime(date_str):
    if not date_str or not date_str.strip():
        return None

    parts = date_str.split()
    if len(parts) != 4:
        return None

    day, month_rus, year, time = parts
    month = MONTHS.get(month_rus)
    if not month:
        return None

    return datetime.strptime(
        f"{day}.{month}.{year} {time}",
        "%d.%m.%Y %H:%M"
    )

def get_score(row, column):
    value = row.get(column, '').strip()
    if not value:
        return 0.0
    return float(value.replace(',', '.'))

control_date = parse_russian_datetime("01 Май 2017 00:00")
wrong_law = 0
wrong_economic = 0

with open("131.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        test_start = parse_russian_datetime(row.get("Тест начат", ""))
        if test_start is None:
            continue
        if test_start > control_date:
            if get_score(row, "В. 1 /1,00") < 1:
                wrong_law += 1
            if get_score(row, "В. 2 /1,00") < 1:
                wrong_law += 1
            if get_score(row, "В. 3 /1,00") < 1:
                wrong_economic += 1

print("Количество неверных ответов по основам законодательства РФ в области образования:", wrong_law)
print("Количество неверных ответов по экономико-правовому регулированию педагогической деятельности:", wrong_economic)