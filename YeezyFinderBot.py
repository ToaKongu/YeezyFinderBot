import keyboards
import replies
import URLs
import config
import time
import asyncio
import aiohttp
import telebot
import sqlite3
import pymysql
from mysql.connector import connect, Error
from bs4 import BeautifulSoup
from threading import Thread


bot = telebot.TeleBot(config.TOKEN)

all_shoes = {'Кроссовки YEEZY Boost 350 V2', 'Кроссовки YEEZY 450', 'Кроссовки YEEZY 500', 'Кроссовки YEEZY Boost 700 V3', 'Кроссовки YEEZY Boost 700 MNVN', 'Сланцы YEEZY Foam Runner'}
all_sizes = {'4 US': ['36 EU', '3.5 UK', '22 JP'], '4.5 US': ['36.5 EU', '4 UK', '22.5 JP'], '5 US': ['37.5 EU', '4.5 UK', '23 JP'], '5.5 US': ['38 EU', '5 UK', '23.5 JP'], '6 US': ['38.5 EU', '5.5 UK', '24 JP'], '6.5 US': ['39.5 EU', '6 UK', '24.5 JP'], '7 US': ['40 EU', '6.5 UK', '25 JP'], '7.5 US': ['40.5 EU', '7 UK', '25.5 JP'], '8 US': ['41.5 EU', '7.5 UK', '26 JP'], '8.5 US': ['42 EU', '8 UK', '26.5 JP'], '9 US': ['42.5 EU', '8.5 UK', '27 JP'], '9.5 US': ['43.5 EU', '9 UK', '27.5 JP'], '10 US': ['44 EU', '9.5 UK', '28 JP'], '10.5 US': ['44.5 EU', '10 UK', '28.5 JP'], '11 US': ['45.5 EU', '10.5 UK', '29 JP'], '11.5 US': ['46 EU', '11 UK', '29.5 JP'], '12 US': ['46.5 EU', '11.5 UK', '30 JP'], '12.5 US': ['47.5 EU', '12 UK', '30.5 JP'], '13 US': ['48 EU', '12.5 UK', '31 JP'], '13.5 US': ['48.5 EU', '13 UK', '31.5 JP'], '14 US': ['49.5 EU', '13.5 UK', '32 JP'], '14.5 US': ['50 EU', '14 UK', '32.5 JP']}
all_commands = ['Выбрать кроссовки', 'За какими кроссовками я слежу', 'Отменить слежку за конкретными кроссовками', 'Изменить размер', 'info']


conn_and_cur = ['', '']
def connection_to_mysql():
    try:
        with pymysql.connect(
            host='localhost',
            user='ToaKongu',
            password='61evopop',
            database='YeezyFinderBot'
        ) as connection:
            print(connection)

        create_table = """CREATE TABLE IF NOT EXISTS yeezy 
            (user_id INT(20), size VARCHAR(10), shoes1 NVARCHAR(30) DEFAULT 'no', shoes2 NVARCHAR(30) DEFAULT 'no', shoes3 NVARCHAR(30) DEFAULT 'no', PRIMARY KEY(user_id))"""
        cursor = connection.cursor()
        connection.ping(reconnect=True)
        cursor.execute(create_table)
        connection.commit()
        conn_and_cur[0], conn_and_cur[1] = connection, cursor
    except Error as err:
        print(err)


def reconnect_to_mysql():
    while True:
        connection_to_mysql()
        time.sleep(60 * 60)


async def find_shoes_side(url, session, his_size, available_size, available_not_size):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36", "content-type": "text"}
    async with session.get(url, headers=headers, allow_redirects=True) as response:
        htmls = await response.read()

        soup = BeautifulSoup (htmls, 'html.parser')
        avail = soup.findAll('button', class_="btn product-order__btn btn_black")
        size = soup.findAll('div', class_="product-plate product-page__plate")
        if size:
            size = size[0].getText()
            result_size = his_size in size or all_sizes[his_size][0] in size or all_sizes[his_size][1] in size or all_sizes[his_size][2] in size
        if not avail and result_size:
            available_size.append(url)
        elif not avail and not result_size:
            available_not_size.append(url)



async def find_shoes_main(his_size, URLs, available_size, available_not_size):

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in URLs:
            task = asyncio.create_task(find_shoes_side(i, session, his_size, available_size, available_not_size))
            tasks.append(task)
        await asyncio.gather(*tasks)


def background_search():
    while True:
        try:
            conn_and_cur[1].execute(f'SELECT shoes1, shoes2, shoes3, size FROM yeezy WHERE user_id = {chat_id}')
            data = conn_and_cur[1].fetchone()
            his_size = data[3]
            URLs_to_check = []
            for shoe in data[:3]:
                if shoe != 'no':
                    URLs_to_check += URLs.URLs[shoe]
            available_size = []
            available_not_size = []
            asyncio.run(find_shoes_main(his_size, URLs_to_check, available_size, available_not_size))
            msg = bot.send_message(chat_id, replies.rep[23])
            msg = bot.send_message(chat_id, replies.rep[24])
            for shoe in available_size:
                msg = bot.send_message(chat_id, shoe)
            msg = bot.send_message(chat_id, replies.rep[25])
            for shoe in available_not_size:
                msg = bot.send_message(chat_id, shoe)
            msg = bot.send_message(chat_id, replies.rep[26])
        except:
            pass

        time.sleep(60 * 60)


@bot.message_handler(commands=['start'])
def start_message(message):
    global chat_id
    chat_id = message.chat.id
    msg = bot.send_message(message.chat.id, replies.rep[0], reply_markup=keyboards.size_keyboard)
    conn_and_cur[1].execute(f'SELECT * FROM yeezy WHERE user_id = {message.chat.id}')
    data = conn_and_cur[1].fetchone()
    if not data:
        conn_and_cur[1].execute(f'INSERT INTO yeezy (user_id) VALUES ({message.chat.id})')
        conn_and_cur[0].commit()
    bot.register_next_step_handler(msg, start)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    conn_and_cur[1].execute(f"SELECT shoes1, shoes2, shoes3, size FROM yeezy WHERE user_id = {message.chat.id}")
    data = conn_and_cur[1].fetchone()
    his_shoes = []
    his_size = data[3]
    for i in data[:3]:
        if i != 'no':
            his_shoes.append(i)

    if message.text == all_commands[0]:
        if len(his_shoes) == 3:
            msg = bot.send_message(message.chat.id, replies.rep[1])
            for i in his_shoes:
                msg = bot.send_message(message.chat.id, ' • ' + i)
            msg = bot.send_message(message.chat.id, replies.rep[2])
        else:
            if len(his_shoes) != 0:
                msg = bot.send_message(message.chat.id, replies.rep[3])
            for i in his_shoes:
                msg = bot.send_message(message.chat.id, ' • ' + i)
            msg = bot.send_message(message.chat.id, replies.rep[4], reply_markup=keyboards.choice_keyboard)
            bot.register_next_step_handler(msg, choice, his_shoes, his_size)

    elif message.text == all_commands[1]:
        if len(his_shoes) == 0:
            msg = bot.send_message(message.chat.id, replies.rep[5])
        else:
            msg = bot.send_message(message.chat.id, replies.rep[3])
            for i in his_shoes:
                msg = bot.send_message(message.chat.id, ' • ' + i)

    elif message.text == all_commands[2]:
        if len(his_shoes) == 0:
            msg = bot.send_message(message.chat.id, replies.rep[5])
            return
        msg = bot.send_message(message.chat.id, replies.rep[3])
        for i in his_shoes:
            msg = bot.send_message(message.chat.id, ' • ' + i)
        msg = bot.send_message(message.chat.id, replies.rep[6], reply_markup=keyboards.delete_keyboard)
        bot.register_next_step_handler(msg, delete, his_shoes)

    elif message.text == all_commands[3]:
        msg = bot.send_message(message.chat.id, replies.rep[7], reply_markup=keyboards.size_keyboard)
        bot.register_next_step_handler(msg, change_size, his_size)

    elif message.text == all_commands[4]:
        msg = bot.send_message(message.chat.id, replies.rep[8])

    else:
        msg = bot.send_message(message.chat.id, replies.rep[9])



def start(message):
    msg = bot.send_message(message.chat.id, replies.rep[10], reply_markup=keyboards.menu_keyboard)
    conn_and_cur[1].execute(f"UPDATE yeezy SET size = '{message.text}' WHERE user_id = {message.chat.id}")
    conn_and_cur[0].commit()


def choice(message, his_shoes, his_size):
    if message.text in all_shoes:
        if message.text in his_shoes:
            msg = bot.send_message(message.chat.id, replies.rep[11], reply_markup=keyboards.fun_keyboard)
        else:
            his_shoes.append(message.text)
            while len(his_shoes) < 3:
                his_shoes.append('no')
            conn_and_cur[1].execute(f"UPDATE yeezy SET shoes1 = '{his_shoes[0]}', shoes2 = '{his_shoes[1]}', shoes3 = '{his_shoes[2]}' WHERE user_id = {message.chat.id}")
            conn_and_cur[0].commit()
            msg = bot.send_message(message.chat.id, replies.rep[12], reply_markup=keyboards.fun_keyboard)
        available_size = []
        available_not_size = []
        URLs_to_check = URLs.URLs[message.text]
        asyncio.run(find_shoes_main(his_size, URLs_to_check, available_size, available_not_size))
        if available_size:
            msg = bot.send_message(message.chat.id, replies.rep[13], reply_markup=keyboards.menu_keyboard)
            for i in available_size:
                msg = bot.send_message(message.chat.id, i)
            msg = bot.send_message(message.chat.id, replies.rep[14])
        elif not available_size and available_not_size:
            msg = bot.send_message(message.chat.id, replies.rep[15], reply_markup=keyboards.yon_keyboard)
            bot.register_next_step_handler(msg, choice_2, available_not_size)
        else:
            msg = bot.send_message(message.chat.id, replies.rep[16], reply_markup=keyboards.menu_keyboard)
    elif message.text == 'Отмена':
        msg = bot.send_message(message.chat.id, replies.rep[17], reply_markup=keyboards.menu_keyboard)
    else:
        msg = bot.send_message(message.chat.id, replies.rep[9])
        bot.register_next_step_handler(msg, choice, his_shoes, his_size)


def choice_2(message, available_not_size):
    if message.text == 'Да':
        msg = bot.send_message(message.chat.id, replies.rep[18], reply_markup=keyboards.menu_keyboard)
        for i in available_not_size:
            msg = bot.send_message(message.chat.id, i)
    elif message.text == 'Нет':
        msg = bot.send_message(message.chat.id, replies.rep[17], reply_markup=keyboards.menu_keyboard)
    else:
        msg = bot.send_message(message.chat.id, replies.rep[9])
        bot.register_next_step_handler(msg, choice_2, available_not_size)


def change_size(message, his_size):
    if message.text in his_size:
        msg = bot.send_message(message.chat.id, replies.rep[19], reply_markup=keyboards.menu_keyboard)
    elif message.text in all_sizes:
        msg = bot.send_message(message.chat.id, replies.rep[20], reply_markup=keyboards.menu_keyboard)
        conn_and_cur[1].execute(f"UPDATE yeezy SET size = '{message.text}' WHERE user_id = {message.chat.id}")
        conn_and_cur[0].commit()
    else:
        msg = bot.send_message(message.chat.id, replies.rep[9])
        bot.register_next_step_handler(msg, change_size, his_size)


def delete(message, his_shoes):
    if message.text not in his_shoes and message.text in all_shoes:
        msg = bot.send_message(message.chat.id, replies.rep[21], reply_markup=keyboards.menu_keyboard)
    elif message.text in his_shoes:
        msg = bot.send_message(message.chat.id, replies.rep[22], reply_markup=keyboards.menu_keyboard)
        for i in range(len(his_shoes)):
            if his_shoes[i] == message.text:
                his_shoes[i] = 'no'
                break
        while len(his_shoes) < 3:
            his_shoes.append('no')
        conn_and_cur[1].execute(f"UPDATE yeezy SET shoes1 = '{his_shoes[0]}', shoes2 = '{his_shoes[1]}', shoes3 = '{his_shoes[2]}' WHERE user_id = {message.chat.id}")
        conn_and_cur[0].commit()
    else:
        msg = bot.send_message(message.chat.id, replies.rep[9])
        bot.register_next_step_handler(msg, delete, his_shoes)


def polling():
    bot.polling(none_stop=True)


polling_thread = Thread(target=polling)
reconn_to_mysql = Thread(target=reconnect_to_mysql)
back_search_thread = Thread(target=background_search)


polling_thread.start()
reconn_to_mysql.start()
back_search_thread.start()
