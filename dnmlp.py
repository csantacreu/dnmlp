import os
os.system('py -m pip install -r requirements.txt')
import re
from datetime import datetime
from openpyxl import load_workbook
from lxml import html

EXCEL_FILE = 'data.xlsx'
LISTINGS_PATH = './listings'
# DESTINATIONS = ('Worldwide', 'European Union', 'United Kingdom')
ASAP_XPATHS = {
    'vendor': '//label[contains(text(),"Vendor:")]/../../td/a/text()',
    'reference': '//a[contains(text(),"Positive")]/@href',
    'title': '//h4/text()',
    'price': '//label[contains(text(), "Price:")]/../../td/text()',
    't_feedback': '//a[contains(text(), "Total")]/span/text()',
    'p_feedback': '//a[contains(text(), "Positive")]/span/text()',
    'n_feedback': '//a[contains(text(), "Negative")]/span/text()',
    's_from': '//label[contains(text(), "Ships from:")]/../../td/text()',
    's_to': '//label[contains(text(), "Ships to:")]/../../td/text()',
    'description': '//h5[contains(text(),"Description")]/../div/text()'
}
COLUMN = {
    'MARKET_COL': 'A',
    'DATE_COL': 'B',
    'SUBNAME_COL': 'C',
    'VENDOR_COL': 'D',
    'URL_COL': 'E',
    'TITLE_COL': 'F',
    'QUANTITY_COL': 'G',
    'PRICE_COL': 'H',
    'T_FEEDBACK_COL': 'I',
    'P_FEEDBACK_COL': 'J',
    'N_FEEDBACK_COL': 'K',
    'S_FROM_COL': 'L',
    'S_TO_COL': 'M',
    'DESCRIPTION_COL': 'N'
}

# class Listing:
#     pass

# class Market:
    
#     def __init__(self, market_n):
#         self.marketN = market_n
    
#     def whichMarket(self):
#         pass
#         print(f'Nombre: {self.marketN}')
# asap_market = Market('ASAP Market')
# asap_market.whichMarket()

html_files = []
for (dirpath, dirname, filenames) in os.walk(LISTINGS_PATH):
    for file_name in filenames:
        file_path = os.path.join(os.path.abspath(dirpath), file_name)
        html_files.append(file_path)

i = 0
listings = []
for file in html_files:
    tree = html.parse(file)

    market = re.search(r'(\w* Market)\.htm', file)[1]

    date = datetime.today().strftime('%d-%b-%Y')

    vendor = tree.xpath(ASAP_XPATHS['vendor'])[0]
    vendor = re.search(r'\w* ', vendor)[0]
    vendor = vendor[:-1]

    reference = tree.xpath(ASAP_XPATHS['reference'])[0]
    reference = re.search(r'\/*.*\/', reference)[0]
    url = f'http://asap2u4pvplnkzl7ecle45wajojnftja45wvovl3jrvhangeyq67ziid.onion{reference}'

    title = tree.xpath(ASAP_XPATHS['title'])[0]

    quantity = re.search(r'\d+\s*[gG]+', title)
    if not quantity:
        quantity = '!!!no quantity'
    else:
        quantity = re.search(r'\d+', quantity[0])[0]

    price = tree.xpath(ASAP_XPATHS['price'])
    if not price:
        price = '!!!no price'
    else:
        price = price[0].translate({ord(i): None for i in '\n\r ,'})
        if price.endswith('USD'):
            price = re.search(r'\d+\.?\d*', price)[0] + ' USD'
        else:
            label_currency = re.search(r'\w{3}', price)[0]
            price = f'({label_currency}) {price}'

    t_feedback = tree.xpath(ASAP_XPATHS['t_feedback'])[0]
    p_feedback = tree.xpath(ASAP_XPATHS['p_feedback'])[0]
    n_feedback = tree.xpath(ASAP_XPATHS['n_feedback'])[0]

    s_from = tree.xpath(ASAP_XPATHS['s_from'])[0]
    s_to = tree.xpath(ASAP_XPATHS['s_to'])[0]

    description = tree.xpath(ASAP_XPATHS['description'])[0]

    listing = {
        'market': market,
        'date': date,
        'vendor': vendor,
        'url': url,
        'title': title,
        'quantity': quantity,
        'price': price,
        't_feedback': t_feedback,
        'p_feedback': p_feedback,
        'n_feedback': n_feedback,
        's_from': s_from,
        's_to': s_to,
        'description': description
            }
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

# debajo de listings, otro para listings de otros países
