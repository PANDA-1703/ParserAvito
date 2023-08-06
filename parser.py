from bs4 import BeautifulSoup
import requests
import psycopg2

prod_err = "Not found"

# product = (input('Название продукта: '))

url = 'https://www.avito.ru/izhevsk?q=' + 'принтер' + '&s=104'
request = requests.get(url)
bs = BeautifulSoup(request.text, 'html.parser')

all_product_html = bs.find_all('div', class_='styles-module-theme-CRreZ')  # Ссылка и название

conn = psycopg2.connect(
    host="localhost",
    database="parser",
    user="panda",
    password="0000"
)

create_table_query = '''
    CREATE TABLE if not exists parse
        (
            id serial primary key,
            title varchar(30),
            link varchar(100),
            description text,
            price int,
            placement_date varchar(30)
        );
'''

cursor = conn.cursor()
cursor.execute(create_table_query)
conn.commit()
cursor.close()


links = []
headers = []
prices = []
descriptions = []
placement_date = []
for html in all_product_html:
    try:
        product_link = "https://www.avito.ru" + str(html.find('a', class_='iva-item-sliderLink-uLz1v').get("href"))
    except AttributeError:
        product_link = prod_err
    links.append(product_link)

    try:
        product_name = html.find('h3', class_='styles-module-root-TWVKW').text.strip()
    except AttributeError:
        product_name = prod_err
    headers.append(product_name)

    price_tag = html.find('strong', class_='styles-module-root-LIAav')
    if price_tag and price_tag.span:
        price = price_tag.span.text.strip().replace('\xa0', '').replace('₽', '')
        prices.append(price)
    else:
        prices.append(prod_err)

    try:
        product_description = html.find('div', class_='iva-item-descriptionStep-C0ty1').text.strip()
    except AttributeError:
        product_description = prod_err
    descriptions.append(product_description)

    try:
        product_placement_date = html.find('div', class_='iva-item-dateInfoStep-_acjp').text.strip()
    except AttributeError:
        product_placement_date = prod_err
    placement_date.append(product_placement_date)

    data_to_insert = [(product_name, product_link, product_description, price, product_placement_date)]
    insert_query = '''
        INSERT INTO parse (title, link, description, price, placement)
        VALUES (%s, %s, %s, %s, %s);
    '''
    cursor = conn.cursor()
    cursor.execute(insert_query, data_to_insert)
    conn.commit()
    cursor.close()

printers_data = []
for i in range(len(headers)):
    printer_data = {
        'Заголовок': headers[i],
        'Ссылка': links[i],
        'Описание': descriptions[i],
        'Цена': prices[i],
        'Дата размещения': placement_date[i]
    }
    printers_data.append(printer_data)






# print(printers_data)
