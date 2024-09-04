import requests
from prefs import *
from tabulate import tabulate
from bs4 import BeautifulSoup

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import types

API_TOKEN = token

def gettable():
    response = requests.post('https://www.dvgups.ru/index.php', params=params, cookies=cookies, headers=headers, data=data)
    table = response.text


    root = BeautifulSoup(table, 'html.parser')
    all_dates = root.find_all('h3')
    trs = root.find_all('table')
    for i in range(len(trs)):
        for_root = BeautifulSoup(str(trs[i]), 'html.parser')
        for_trs = for_root.select_one('table').select('tr')
        rows = [
            [td.text for td in tr.select('td')]
            for tr in for_trs[0:]
        ]

        for_date = str(all_dates[i])

        print(for_date[4:-5])
        print(tabulate(rows, headers=[], tablefmt="grid"))

        return tabulate(rows, headers=[], tablefmt="grid")




bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Вывести расписание", callback_data='tableReply')
    markup.add(button1)

    bot.send_message(message.chat.id,
                     "afk gameplay".format(message.from_user),
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if "table" in call.data:
        table = gettable()
        bot.send_message(call.message.chat.id,
                         table)


bot.infinity_polling(timeout=10, long_polling_timeout = 5)