
import os
import re
from openpyxl import load_workbook
from bs4 import BeautifulSoup
from lxml import html

EXCEL_FILE = 'data.xlsx'
LISTINGS_PATH = './listings'
MARKET_COL = 'A'
DATE_COL = 'B'
SUBNAME_COL = 'C'
VENDOR_COL = 'D'
URL_COL = 'E'
TITLE_COL = 'F'
QUANTITY_COL = 'G'
PRICE_COL = 'H'
TRANS_COL = 'I'
S_FROM_COL = 'J'
S_TO_COL = 'K'
DESCRIPTION_COL = 'L'

# print(f'\nCD:     {os.getcwd()}\n')

html_files = []
for (dirpath, dirname, filenames) in os.walk(LISTINGS_PATH):
    i = 0
    for file_name in filenames:
        i += 1
        # print(f'{i} {file_name}')
        file_path = os.path.join(os.path.abspath(dirpath), file_name)
        html_files.append(file_path)

# funcion para cribar cada archivo según la sustancia que sea
def which_market():
    pass

i = 0
vendors = []
titles = []
prices = []
raw_prices = []
s_froms = []
s_tos = []
descriptions = []
listings = []
for file in html_files:
    print(f'File:   {file}')
    tree = html.parse(file)
    root = tree.getroot()
    vendor = tree.xpath('//label[contains(text(),"Vendor:")]/../../td/a/text()')[0]
    vendors.append(vendor)
    title = tree.xpath('/html/body/div/div[3]/div/div[1]/h4/text()')[0]
    titles.append(title)
    price = tree.xpath('//label[contains(text(), "Price:")]/../../td/text()')
    if not price:
        price = '!!!no price'
    else:
        price = price[0].translate({ord(i): None for i in '\n\r ,'})
    if price.endswith('USD'):
        price = re.search(r'\d+\.?\d*', price)[0]
    elif not price.endswith('USD'):
        label_currency = re.search(r'\w{3}', price)[0]
    print(price)
    prices.append(price)
    s_from = tree.xpath('//label[contains(text(), "Ships from:")]/../../td/text()')[0]
    s_froms.append(s_from)
    s_to = tree.xpath('//label[contains(text(), "Ships to:")]/../../td/text()')[0]
    s_tos.append(s_to)
    description = tree.xpath('//h5[contains(text(),"Description")]/../div/text()')[0]
    descriptions.append(description)
    print(s_from, s_to)
    listing = {
            'vendor': vendor,
            'title': title,
            'price': price,
            's_from': s_from,
            's_to': s_to,
            'description': description
            }
    listings.append(listing)

workbook = load_workbook(filename=EXCEL_FILE)
sheet = workbook.active
row_n = 3
for listing in listings:
    title_coordinate = f'{TITLE_COL}{row_n}'
    sheet[title_coordinate] = listing['title']
    price_coordinate = f'{PRICE_COL}{row_n}'
    sheet[price_coordinate] = listing['price']
    vendor_coordinate = f'{VENDOR_COL}{row_n}'
    sheet[vendor_coordinate] = listing['vendor']
    s_from_coordinate = f'{S_FROM_COL}{row_n}'
    sheet[s_from_coordinate] = listing['s_from']
    s_to_coordinate = f'{S_TO_COL}{row_n}'
    sheet[s_to_coordinate] = listing['s_to']
    description_coordinate = f'{DESCRIPTION_COL}{row_n}'
    sheet[description_coordinate] = listing['description']
    row_n += 1
workbook.save(filename=EXCEL_FILE)