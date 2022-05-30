
import os
import re
from openpyxl import load_workbook
from lxml import html
from datetime import datetime

DESTINATIONS = ('Worldwide', 'European Union', 'United Kingdom')
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

ASAP_XPATHS = {
    'vendor': '//label[contains(text(),"Vendor:")]/../../td/a/text()',
    # 'url': url,
    # 'title': title,
    # 'quantity': quantity,
    # 'price': price,
    # 's_from': s_from,
    # 's_to': s_to,
    # 'description': description
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
listings = []
for file in html_files:
    tree = html.parse(file)

    market = file.strip('.htm')

    date = datetime.today().strftime('%d-%b-%Y')

    vendor = tree.xpath('//label[contains(text(),"Vendor:")]/../../td/a/text()')[0]
    vendor = re.search(r'\w* ', vendor).group(0)
    vendor = vendor[:-1]

    reference = tree.xpath('//a[contains(text(),"Positive")]/@href')[0]
    reference = re.search(r'\/*.*\/', reference)
    url = f'http://asap2u4pvplnkzl7ecle45wajojnftja45wvovl3jrvhangeyq67ziid.onion{reference}'

    title = tree.xpath('/html/body/div/div[3]/div/div[1]/h4/text()')[0]

    quantity = re.search(r'\d+\s*[gG]+', title)
    if not quantity:
        quantity = '!!!no quantity'
    else:
        quantity = re.search(r'\d+', quantity[0])[0] + 'g'

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

    s_from = tree.xpath('//label[contains(text(), "Ships from:")]/../../td/text()')[0]
    s_to = tree.xpath('//label[contains(text(), "Ships to:")]/../../td/text()')[0]

    description = tree.xpath('//h5[contains(text(),"Description")]/../div/text()')[0]

    listing = {
        'date': date,
        'vendor': vendor,
        'url': url,
        'title': title,
        'quantity': quantity,
        'price': price,
        's_from': s_from,
        's_to': s_to,
        'description': description
            }
    print(title)
    print(quantity)
    print(vendor)
    print(price + '\n')
    listings.append(listing)

wb = load_workbook(filename=EXCEL_FILE)
sheet = wb.active
row_n = 2
for listing in listings:
    row_n += 1
    for key, value in listing.items():
        col = key.upper() + '_COL'
        coordinate = f'{COLUMN[col]}{row_n}'
        sheet[coordinate] = listing[key]
wb.save(filename=EXCEL_FILE)
