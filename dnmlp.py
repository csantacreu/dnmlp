
# /////////////// DarkNet Market Listing Parser ///////////////

import os
from bs4 import BeautifulSoup

listings_path = './listings'
html_files = []

# os.chdir('./listings')

print(f'\nCD:     {os.getcwd()}\n')

for (dirpath, dirname, filenames) in os.walk(listings_path):
    i = 0
    for file_name in filenames:
        i += 1
        # print(f'{i} {file_name}')6
        file_path = os.path.join(os.path.abspath(dirpath), file_name)
        html_files.append(file_path)

# funcion para cribar cada archivo según la sustancia que sea
def which_market():
    pass

i = 0
for file in html_files:
    i += 1
    with open(file) as fl:
        soup = BeautifulSoup(fl, 'html.parser')
        # print(f'Listing title:  {str(soup.body.h4.text)}')
        label = soup.find('th', {'class': 'cell-label'})
        label_price = label.parent.td.text
        print(label_price)
        # print(f'{i}:    {label_price.td.text}')
        