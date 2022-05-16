
# DarkNet Market Listing Parser

import os

listings_path = './listings'
html_files = []

# os.chdir('./listings')

print(f'cd:     {os.getcwd()}')

for (dirpath, dirname, filenames) in os.walk(listings_path):
    i = 0
    for file_name in filenames:
        i += 1
        print(str(i) + ' ' + file_name)
        # print(f'{i} {file_name}')6
        # Stores the absolute path of each c and h file in file_path
        file_path = os.path.join(os.path.abspath(dirpath), file_name)
        html_files.append(file_path)
print(html_files)
# funcion para cribar cada archivo según la sustancia que sea