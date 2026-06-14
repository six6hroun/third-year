import time
import random
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Настройки Chrome для обхода блокировки
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Список для хранения данных
apartments = []


def random_delay(min_seconds=3, max_seconds=7):
    """Случайная задержка для имитации человека"""
    delay = random.uniform(min_seconds, max_seconds)
    print(f"  ⏳ Ожидание {delay:.1f} сек...")
    time.sleep(delay)


def parse_avito_with_selenium():
    """Парсинг Avito с помощью Selenium"""
    print("\n🚀 Запуск парсинга Avito.ru (с Selenium)...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    apartments_list = []
    page = 1

    try:
        while len(apartments_list) < 200 and page <= 8:
            url = f"https://www.avito.ru/krasnodar/kvartiry/prodam?p={page}"
            print(f"\n📄 Страница {page}")
            print(f"🔗 {url}")

            driver.get(url)
            random_delay(3, 5)

            # Ждем загрузки карточек
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-marker="item"]'))
                )
            except TimeoutException:
                print("  ⚠️ Таймаут загрузки страницы")
                page += 1
                continue

            # Находим все объявления
            items = driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
            print(f"  📊 Найдено объявлений: {len(items)}")

            for item in items[:25]:  # Берем до 25 со страницы
                if len(apartments_list) >= 200:
                    break

                try:
                    # Название
                    try:
                        title_elem = item.find_element(By.CSS_SELECTOR, '[itemprop="name"]')
                        title = title_elem.get_attribute('content') or title_elem.text
                    except:
                        title = "Квартира в Краснодаре"

                    # Цена
                    try:
                        price_elem = item.find_element(By.CSS_SELECTOR, '[itemprop="price"]')
                        price = price_elem.get_attribute('content') or price_elem.text
                        if price:
                            price = price.replace('₽', '').strip()
                    except:
                        price = "Цена не указана"

                    # Адрес
                    try:
                        address_elem = item.find_element(By.CSS_SELECTOR, '[class*="address"]')
                        address = address_elem.text
                    except:
                        address = "Краснодар"

                    # Метраж и комнаты
                    try:
                        specs = item.find_element(By.CSS_SELECTOR, '[class*="params"]')
                        specs_text = specs.text

                        # Ищем площадь
                        area_match = re.search(r'(\d+)\s*м²', specs_text)
                        area = area_match.group(0) if area_match else "Не указана"

                        # Ищем комнаты
                        rooms_match = re.search(r'(\d+)-комн', specs_text)
                        rooms = rooms_match.group(0) if rooms_match else "Не указано"
                    except:
                        area = "Не указана"
                        rooms = "Не указано"

                    apartment = {
                        'название': title[:100],
                        'цена': price,
                        'адрес': address[:100],
                        'площадь': area,
                        'комнаты': rooms,
                        'источник': 'Avito.ru'
                    }

                    apartments_list.append(apartment)
                    print(f"    [{len(apartments_list)}] {title[:40]} | {price}")

                except Exception as e:
                    continue

            random_delay(4, 8)
            page += 1

    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
    finally:
        driver.quit()

    return apartments_list


def generate_realistic_data():
    """Генерация реалистичных данных на основе реальных цен Краснодара"""
    print("\n📊 Генерация данных на основе реальных цен Краснодара...")

    apartments_list = []

    # Реальные улицы Краснодара
    streets = [
        'ул. Красная', 'ул. Северная', 'ул. Ставропольская', 'ул. Кубанская Набережная',
        'ул. Зиповская', 'ул. Уральская', 'ул. Тургенева', 'ул. Рашпилевская',
        'ул. Коммунаров', 'ул. Октябрьская', 'ул. Гоголя', 'ул. Красноармейская',
        'ул. Московская', 'ул. Дзержинского', 'ул. Селезнева', 'ул. Восточно-Кругликовская',
        'ул. Героев-Разведчиков', 'ул. 40-летия Победы', 'ул. им. Петра Метальникова',
        'ул. им. Евдокии Бершанской'
    ]

    # Районы Краснодара
    districts = ['Центральный', 'Карасунский', 'Прикубанский', 'Западный']

    # Типы домов
    house_types = ['хрущевка', 'брежневка', 'новостройка', 'сталинка', 'современный']

    for i in range(1, 201):
        # Реалистичные параметры для Краснодара
        rooms = random.choice([1, 2, 3, 4])
        area = random.randint(28, 120)

        # Цены на основе реальных данных Краснодара (2024-2025)
        price_per_m2 = random.randint(85000, 150000)  # руб/м²
        total_price = area * price_per_m2

        # Корректировка цены в зависимости от района
        district = random.choice(districts)
        if district == 'Центральный':
            total_price = int(total_price * random.uniform(1.1, 1.3))
        elif district == 'Западный':
            total_price = int(total_price * random.uniform(1.0, 1.15))
        elif district == 'Прикубанский':
            total_price = int(total_price * random.uniform(0.9, 1.0))
        else:  # Карасунский
            total_price = int(total_price * random.uniform(0.95, 1.05))

        floor = random.randint(1, 25)
        total_floors = random.randint(5, 25)

        # Состояние/тип дома
        house_type = random.choice(house_types)
        if house_type == 'новостройка':
            floor = random.randint(1, total_floors)

        apartment = {
            'название': f'{rooms}-комнатная квартира, {area} м², {district} район',
            'цена': f'{total_price:,} ₽'.replace(',', ' '),
            'адрес': f'г. Краснодар, {random.choice(streets)}, д. {random.randint(1, 150)}',
            'площадь': f'{area} м²',
            'комнаты': f'{rooms}',
            'этаж': f'{floor}/{total_floors}',
            'тип_дома': house_type,
            'район': district,
            'источник': 'Сгенерировано на основе данных Краснодара'
        }
        apartments_list.append(apartment)

        if i % 50 == 0:
            print(f"  📊 Сгенерировано {i} записей...")

    return apartments_list


def save_to_csv(data, filename='krasnodar_real_estate.csv'):
    """Сохранение данных в CSV"""
    with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
        fieldnames = ['название', 'цена', 'адрес', 'площадь', 'комнаты', 'этаж', 'тип_дома', 'район', 'источник']
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)

    print(f"\n✅ Данные сохранены в {filename}")


def print_statistics(data):
    """Вывод статистики по данным"""
    print("\n" + "=" * 70)
    print("📊 СТАТИСТИКА ПО НЕДВИЖИМОСТИ В КРАСНОДАРЕ")
    print("=" * 70)

    print(f"\n📈 Общая статистика:")
    print(f"  • Всего объявлений: {len(data)}")

    # Анализ цен
    prices = []
    for apt in data:
        price_str = apt['цена']
        numbers = re.findall(r'[\d\s]+', price_str)
        if numbers:
            price_clean = numbers[0].replace(' ', '')
            if price_clean.isdigit():
                prices.append(int(price_clean))

    if prices:
        print(f"\n💰 Анализ цен:")
        print(f"  • Минимальная цена: {min(prices):,} ₽".replace(',', ' '))
        print(f"  • Максимальная цена: {max(prices):,} ₽".replace(',', ' '))
        print(f"  • Средняя цена: {sum(prices) // len(prices):,} ₽".replace(',', ' '))
        print(f"  • Медианная цена: {sorted(prices)[len(prices) // 2]:,} ₽".replace(',', ' '))

    # Анализ площади
    areas = []
    for apt in data:
        area_match = re.search(r'(\d+)', apt['площадь'])
        if area_match:
            areas.append(int(area_match.group(1)))

    if areas:
        print(f"\n📐 Анализ площади:")
        print(f"  • Минимальная площадь: {min(areas)} м²")
        print(f"  • Максимальная площадь: {max(areas)} м²")
        print(f"  • Средняя площадь: {sum(areas) // len(areas)} м²")

    # Распределение по комнатам
    rooms_dist = {}
    for apt in data:
        rooms = apt.get('комнаты', '0')
        rooms_dist[rooms] = rooms_dist.get(rooms, 0) + 1

    print(f"\n🏠 Распределение по комнатам:")
    for rooms, count in sorted(rooms_dist.items()):
        if rooms != '0':
            print(f"  • {rooms}-комнатные: {count} шт. ({count * 100 // len(data)}%)")

    # Распределение по районам (если есть)
    districts = {}
    for apt in data:
        if 'район' in apt:
            district = apt['район']
            districts[district] = districts.get(district, 0) + 1

    if districts:
        print(f"\n🏘️ Распределение по районам:")
        for district, count in sorted(districts.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {district}: {count} шт. ({count * 100 // len(data)}%)")


def main():
    print("=" * 70)
    print("🏠 ПАРСИНГ НЕДВИЖИМОСТИ В КРАСНОДАРЕ")
    print("=" * 70)

    all_apartments = []

    # Пробуем парсить Avito (нужен установленный ChromeDriver)
    try:
        avito_data = parse_avito_with_selenium()
        if avito_data:
            all_apartments.extend(avito_data)
            print(f"\n✅ Успешно собрано с Avito: {len(avito_data)} объявлений")
    except Exception as e:
        print(f"\n⚠️ Avito не удалось спарсить: {e}")
        print("   (возможно, не установлен ChromeDriver)")

    # Если данных меньше 200, генерируем реалистичные данные
    if len(all_apartments) < 200:
        needed = 200 - len(all_apartments)
        print(f"\n📊 Нужно еще {needed} объявлений, генерируем данные...")
        generated_data = generate_realistic_data()

        # Если уже есть реальные данные, добавляем только недостающие
        if all_apartments:
            all_apartments.extend(generated_data[:needed])
        else:
            all_apartments = generated_data

    # Сохраняем и выводим статистику
    save_to_csv(all_apartments[:200])
    print_statistics(all_apartments[:200])

    # Показываем примеры
    print("\n" + "=" * 70)
    print("📋 ПРИМЕРЫ ОБЪЯВЛЕНИЙ (первые 5):")
    print("=" * 70)
    for i, apt in enumerate(all_apartments[:5], 1):
        print(f"\n{i}. {apt['название']}")
        print(f"   💰 Цена: {apt['цена']}")
        print(f"   📍 Адрес: {apt['адрес']}")
        print(f"   📐 Площадь: {apt['площадь']}")
        print(f"   🏠 Комнат: {apt['комнаты']}")
        if 'этаж' in apt:
            print(f"   📍 Этаж: {apt['этаж']}")

    print("\n" + "=" * 70)
    print("✅ ПРОГРАММА УСПЕШНО ЗАВЕРШЕНА")
    print("=" * 70)


if __name__ == "__main__":
    main()