import requests
from prefs import *
from tabulate import tabulate
from bs4 import BeautifulSoup



response = requests.post('https://www.dvgups.ru/index.php', params=params, cookies=cookies, headers=headers, data=data)
table = response.text


root = BeautifulSoup(table, 'html.parser')
trs = root.select('table')
# tr > th > td
print(trs)
headers = [th.text for th in trs[0].select('th')]
rows = [
    [td.text for td in tr.select('td')]
    for tr in trs[1:]
]

print(tabulate(rows, headers=headers, tablefmt="grid"))
