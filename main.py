import requests
from prefs import *
from tabulate import tabulate
from bs4 import BeautifulSoup

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import types
import datetime

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
                    final_table[j].append(rows[j][z]) # Убираем бесполезный z: 3, и оставляем все остальное

        print(final_table)
        for_date = str(all_dates[i]) # даты

        print(for_date[4:-5])
        print(tabulate(final_table, headers=[], tablefmt="grid"))
        printed_table += for_date[4:-5].strip().rstrip().rstrip('\n') + "\n" # дата
        for j in range(len(final_table)):
            s = ''
            for z in range(len(final_table[j])):
                s += final_table[j][z].strip().rstrip().rstrip('\n') + "\n"
            printed_table += s + "\n"
        printed_table += "----------------------------------------------" + "\n" # конец расписания текущей даты
        printed_list.append(printed_table)
    return printed_list



bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.id == myChatId:
        markup = types.InlineKeyboardMarkup()
        today = types.InlineKeyboardButton("Сегодня", callback_data='today')
        tomorrow = types.InlineKeyboardButton("Завтра", callback_data='tomorrow')
        full = types.InlineKeyboardButton("Фул", callback_data='full')
        markup.add(today)
        markup.add(tomorrow)
        markup.add(full)

        bot.send_message(message.chat.id,
                         "выбор?".format(message.from_user),
                         reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    current_date = datetime.datetime.now().strftime('%d.%m.%Y')
    tomorrow_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
    # data[1] = datetime.datetime.now().strftime('%d.%m.%Y')

    current_date_datetime = datetime.datetime.now()
    tomorrow_date_datetime = (datetime.date.today() + datetime.timedelta(days=1))
    #TODO

    if "today" in call.data:
        tablelist = get_timetable_list()
        for i in tablelist:
            if i[:10] == current_date:
                bot.send_message(call.message.chat.id,
                                i)
    if "tomorrow" in call.data:
        tablelist = get_timetable_list()
        for i in tablelist:
            if i[:10] == tomorrow_date:
                bot.send_message(call.message.chat.id,
                                 i)

    if "full" in call.data:
        tablelist = get_timetable_list()
        for i in tablelist:
            bot.send_message(call.message.chat.id,
                                 i)

bot.infinity_polling(timeout=10, long_polling_timeout = 5)