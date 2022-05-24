
import os
import re
from openpyxl import load_workbook
from lxml import html
from datetime import datetime

EXCEL_FILE = 'data.xlsx'
LISTINGS_PATH = './listings'
COLUMN = {
    'MARKET_COL': 'A',
    'DATE_COL': 'B',
    'SUBNAME_COL': 'C',
    'VENDOR_COL': 'D',
    'URL_COL': 'E',
    'TITLE_COL': 'F',
    'QUANTITY_COL': 'G',
    'PRICE_COL': 'H',
    'TRANS_COL': 'I',
    'S_FROM_COL': 'J',
    'S_TO_COL': 'K',
    'DESCRIPTION_COL': 'L'
}

html_files = []
for (dirpath, dirname, filenames) in os.walk(LISTINGS_PATH):
    i = 0
    for file_name in filenames:
        i += 1
        # print(f'{i} {file_name}')
        file_path = os.path.join(os.path.abspath(dirpath), file_name)
        html_files.append(file_path)

i = 0
vendors = []
urls = []
titles = []
prices = []
raw_prices = []
s_froms = []
s_tos = []
descriptions = []
listings = []
for file in html_files:
    tree = html.parse(file)
    vendor = tree.xpath('//label[contains(text(),"Vendor:")]/../../td/a/text()')[0]
    vendors.append(vendor)
    listing_reference = tree.xpath('//a[contains(text(),"Positive")]/@href')[0]
    listing_reference = re.search(r'\/*.*\/', listing_reference)[0]
    url = f'http://asap2u4pvplnkzl7ecle45wajojnftja45wvovl3jrvhangeyq67ziid.onion{listing_reference}'
    urls.append(url)
    title = tree.xpath('/html/body/div/div[3]/div/div[1]/h4/text()')[0]
    titles.append(title)
    price = tree.xpath('//label[contains(text(), "Price:")]/../../td/text()')
    if not price:
        price = '!!!no price'
    else:
        price = price[0].translate({ord(i): None for i in '\n\r ,'})
        if price.endswith('USD'):
            price = re.search(r'\d+\.?\d*', price)[0] + ' USD'
        else:
            label_currency = re.search(r'\w{3}', price)[0]
            price = f'({label_currency}) {price}'
    prices.append(price)
    s_from = tree.xpath('//label[contains(text(), "Ships from:")]/../../td/text()')[0]
    s_froms.append(s_from)
    s_to = tree.xpath('//label[contains(text(), "Ships to:")]/../../td/text()')[0]
    s_tos.append(s_to)
    description = tree.xpath('//h5[contains(text(),"Description")]/../div/text()')[0]
    descriptions.append(description)
    listing = {
            'vendor': vendor,
            'url': url,
            'title': title,
            'price': price,
            's_from': s_from,
            's_to': s_to,
            'description': description
            }
    listings.append(listing)

workbook = load_workbook(filename=EXCEL_FILE)
sheet = workbook.active
row_n = 2
for listing in listings:
    row_n += 1
    for key, value in listing.items():
        col = key.upper() + '_COL'
        coordinate = f'{COLUMN[col]}{row_n}'
        sheet[coordinate] = listing[key]
workbook.save(filename=EXCEL_FILE)
