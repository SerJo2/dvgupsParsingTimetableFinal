import requests
from prefs import *
from tabulate import tabulate
from bs4 import BeautifulSoup

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import types
import datetime

current_date = datetime.datetime.now().strftime('%d.%m.%Y')

API_TOKEN = token

def get_timetable_list():
    response = requests.post('https://www.dvgups.ru/index.php', params=params, cookies=cookies, headers=headers, data=data)
    table = response.text

    printed_list = []

    root = BeautifulSoup(table, 'html.parser')
    all_dates = root.find_all('h3')
    trs = root.find_all('table')
    for i in range(len(trs)):
        printed_table = ""
        for_root = BeautifulSoup(str(trs[i]), 'html.parser')
        for_trs = for_root.select_one('table').select('tr')
        rows = [
            [td.text for td in tr.select('td')]
            for tr in for_trs[0:]
        ]

        final_table = list()
        for x in range(len(rows)):
            final_table.append([])
        print(final_table)

        #rows[x][z] - z: 0 - номер пары, z: 1 - что за пара, z: 2 - аудитория, z: 3 - группы, z:4 - препод

        print(rows)
        for j in range(len(rows)):
            for z in range(len(rows[j])):
                if z != 3:
                    final_table[j].append(rows[j][z])

        print(final_table)
        for_date = str(all_dates[i])

        print(for_date[4:-5])
        print(tabulate(final_table, headers=[], tablefmt="grid"))
        printed_table += for_date[4:-5].strip().rstrip().rstrip('\n') + "\n"
        for j in range(len(final_table)):
            s = ''
            for z in range(len(final_table[j])):
                s += final_table[j][z].strip().rstrip().rstrip('\n') + "\n"
            printed_table += s + "\n"
        printed_table += "----------------------------------------------" + "\n"
        printed_list.append(printed_table)
    return printed_list




bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    markup = types.InlineKeyboardMarkup()
    today = types.InlineKeyboardButton("Вывести расписание", callback_data='today')
    markup.add(today)

    bot.send_message(message.chat.id,
                     "выбор?".format(message.from_user),
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if "today" in call.data:
        tablelist = get_timetable_list()
        for i in tablelist:
            if i[:10] == current_date:
                bot.send_message(call.message.chat.id,
                                i)
        


bot.infinity_polling(timeout=10, long_polling_timeout = 5)