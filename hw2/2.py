import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json

url = "https://books.toscrape.com/"
books = list()
while True:
    website = requests.get(url)
    html = website.content
    main_soup = BeautifulSoup(html, "html.parser")
    image_containers = main_soup.find_all('div', ('class', 'image_container'))
    rel_links = [container.find('a').get('href') for container in image_containers]
    abs_links = [urllib.parse.urljoin(url, rel_link) for rel_link in rel_links]
    for abs_link in abs_links:
        soup = BeautifulSoup(requests.get(abs_link).content, 'html.parser')
        div = soup.find('div', ('class', 'col-sm-6 product_main'))
        title = div.find('h1').text
        price = div.find('p', ('class', 'price_color')).text
        available = div.find('p', ('class', 'instock availability')).text
        available = int(re.findall(r'\b\d+\b', available)[0])
        description = soup.find("meta", attrs={"name": "description"})["content"].strip()
        books.append({"title": title, "price": price, "available": available, "description": description})
    next_li = main_soup.find('li', ('class', 'next'))
    if not next_li:
        break
    next_link = next_li.find('a')['href']
    url = urllib.parse.urljoin(url, next_link)
with open("books.json", "w", encoding='utf-8') as file:
    json.dump(books, file, ensure_ascii=False)