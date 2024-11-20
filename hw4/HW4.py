import requests
from lxml import html
import csv
import sys


def parse_trading_view_stocks():
    url = 'https://ru.tradingview.com/markets/stocks-russia/market-movers-gainers/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        # Отправка HTTP GET-запроса
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Вызов исключения для плохих HTTP-статусов

        # Явное указание кодировки
        response.encoding = 'utf-8'

        # Парсинг HTML с помощью lxml
        tree = html.fromstring(response.content)

        # XPath для поиска строк таблицы
        rows_xpath = '//table//tr[position()>1]'  # Пропускаем заголовок
        rows = tree.xpath(rows_xpath)

        # Подготовка данных для CSV
        stock_data = []

        for row in rows:
            try:
                # Извлечение данных ячеек с обработкой возможных ошибок
                ticker = row.xpath('.//td[1]//text()')[0].strip() if row.xpath('.//td[1]//text()') else 'N/A'
                company = row.xpath('.//td[2]//text()')[0].strip() if row.xpath('.//td[2]//text()') else 'N/A'
                price = row.xpath('.//td[3]//text()')[0].strip() if row.xpath('.//td[3]//text()') else 'N/A'
                change_percent = row.xpath('.//td[4]//text()')[0].strip() if row.xpath('.//td[4]//text()') else 'N/A'

                stock_data.append([ticker, company, price, change_percent])

            except Exception as row_error:
                print(f"Ошибка при обработке строки: {row_error}")

        # Сохранение в CSV с явным указанием кодировки
        if stock_data:
            with open('russian_stocks.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Тикер', 'Компания', 'Цена', 'Изменение %'])
                csvwriter.writerows(stock_data)

            print(f"Данные сохранены. Всего строк: {len(stock_data)}")
        else:
            print("Данные не найдены")

    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


# Запуск парсера
if __name__ == '__main__':
    parse_trading_view_stocks()
    