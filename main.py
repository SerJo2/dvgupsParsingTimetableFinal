import requests
from prefs import *
from tabulate import tabulate
from bs4 import BeautifulSoup



response = requests.post('https://www.dvgups.ru/index.php', params=params, cookies=cookies, headers=headers, data=data)
table = response.text


root = BeautifulSoup(table, 'html.parser')
trs = root.find_all('table')
# tr > th > td
for i in trs:
    forRoot = BeautifulSoup(str(i), 'html.parser')
    forTrs = forRoot.select_one('table').select('tr')
    headers = [th.text for th in forTrs[0].select('th')]
    rows = [
        [td.text for td in tr.select('td')]
        for tr in forTrs[0:]
    ]
    print(tabulate(rows, headers=headers, tablefmt="grid"))