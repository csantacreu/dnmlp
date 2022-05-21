
# ////////////////////// DarkNet Market Listing Parser //////////////////////

import os
import re
from bs4 import BeautifulSoup
from openpyxl import load_workbook

EXCEL_FILE = 'data.xlsx'

print(f'\nCD:     {os.getcwd()}\n')
listings_path = './listings'

html_files = []
for (dirpath, dirname, filenames) in os.walk(listings_path):
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
h = 2
prices = []
for file in html_files:
    i += 1
    h += 1
    
    with open(file) as fl:
        soup = BeautifulSoup(fl, 'html.parser')
        label = soup.find('th', {'class': 'cell-label'})
        label_price = label.parent.td.text
        label_price = label_price.translate({ord(i): None for i in '\n ,'})
        if label_price == '1375.00USD':
            label_price = '75.00USD'
        if label_price.endswith('USD'):
            label_price = re.search(r'\d+\.?\d*', label.parent.td.text)
            label_price = label_price[0]
        prices.append(label_price)
        # elif not label_price.endswith('USD'):
        #     label_price = '!!!noPrice'
         
        # coordinate = f'H{h}'
        # sheet[coordinate] = label_price
        # print(label_price)
        

workbook = load_workbook(filename=EXCEL_FILE)
sheet = workbook.active
sheet['I3'] = 'h'
workbook.save(filename=EXCEL_FILE)