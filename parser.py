from bs4 import BeautifulSoup
import requests

product = (input('Название продукта: '))

url = 'https://www.avito.ru/izhevsk?q=' + product
request = requests.get(url)
bs = BeautifulSoup(request.text, 'html.parser')

all_links = bs.find_all('a', class_='styles-module-root-QmppR')  # Ссылка и название
all_text = bs.find_all('div', class_='iva-item-descriptionStep-C0ty1')

links = []
for link in all_links:
    links.append("https://www.avito.ru" + str(link.get("href")))
print(links)

texts = []
for text in all_text:
    texts.append(text.text)
print(texts)
