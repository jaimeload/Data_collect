import json
from clickhouse_driver import Client

client = Client(
        host='nl433l0a35.eu-central-1.aws.clickhouse.cloud',
        user='default',
        password='O_8zFrV6Muek9',
        secure=True
    )

client.execute('CREATE DATABASE IF NOT EXISTS store')

client.execute('''
    CREATE TABLE IF NOT EXISTS store.books (
        title String,
        price String,
        available Int32,
        description String
    ) ENGINE = MergeTree() ORDER BY tuple()
''')

with open('books.json', 'r', encoding='utf-8') as file:
    books_json = json.load(file)

data = [(book['title'], book['price'], book['available'], book['description']) for book in books_json]

# Вставляем данные в таблицу
client.execute('''
    INSERT INTO store.books (title, price, available, description)
    VALUES
''', data)