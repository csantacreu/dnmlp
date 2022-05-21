
import os
import re
from bs4 import BeautifulSoup
from openpyxl import load_workbook

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
prices = []
raw_prices = []
titles = []
listings = []
for file in html_files:
    with open(file) as fl:
        soup = BeautifulSoup(fl, 'html.parser')
        # titles
        title = soup.find('h4').text
        titles.append(title)
        # prices
        label = soup.find('th', {'class': 'cell-label'})
        label_price = label.parent.td.text
        raw_prices.append(label_price)
        label_price = label_price.translate({ord(i): None for i in '\n ,'})
        if label_price.endswith('USD'):
            label_price = re.search(r'\d+\.?\d*', label_price)
            label_price = label_price[0]
        prices.append(label_price)
        # elif not label_price.endswith('USD'):
        #     label_price = '!!!noPrice'
        listing = {
            'title': title,
            'price': label_price
            }
        listings.append(listing)
    i += 1

workbook = load_workbook(filename=EXCEL_FILE)
sheet = workbook.active
row_n = 3
for listing in listings:
    title_coordinate = f'{TITLE_COL}{row_n}'
    sheet[title_coordinate] = listing['title']
    price_coordinate = f'{PRICE_COL}{row_n}'
    sheet[price_coordinate] = listing['price']
    row_n += 1
workbook.save(filename=EXCEL_FILE)