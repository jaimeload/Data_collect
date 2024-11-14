from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")

db = client['store']
books = db['books']
with open('books.json', 'r', encoding='utf-8') as file:
    books_json = json.load(file)

data = books_json

CHUNK_SIZE = 100

def data_gen(data, chunk_size=CHUNK_SIZE):
    for i in range(0, len(data), chunk_size):
        yield data[i: i + chunk_size]


data_list = list(data_gen(data, CHUNK_SIZE))

for data_chunk in data_list:
    books.insert_many(data_chunk)

more_than_20_instock = books.count_documents(filter={"available": {"$gte": 20}})
print(more_than_20_instock)
