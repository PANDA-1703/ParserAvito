from bs4 import BeautifulSoup
import requests

# product = (input('Название продукта: '))

url = 'https://www.avito.ru/izhevsk?q=' + 'принтер'
request = requests.get(url)
bs = BeautifulSoup(request.text, 'html.parser')

all_product_html = bs.find_all('div', class_='styles-module-theme-CRreZ')  # Ссылка и название

links = []
headers = []
texts = []
for html in all_product_html:
    try:
        product_link = ("https://www.avito.ru" + str(html.get("href")))
    except AttributeError:
        product_link = "Not Found"
    links.append(product_link)

    try:
        product_name = html.find('h3', class_='styles-module-root-TWVKW').text.strip()
    except AttributeError:
        product_name = "Not found"
    headers.append(product_name)

    try:
        product_text = html.find('div', class_='iva-item-descriptionStep-C0ty1').text.strip()
    except AttributeError:
        product_text = "Not found"
    texts.append(product_text)

print(headers)
print(links)
print(texts)

# Описание
# texts = []
# for text in all_text:
#     texts.append(text.text)
# print(texts)
