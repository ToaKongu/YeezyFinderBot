import keyboards
import replies
import URLs
import telebot
import pymysql
from mysql.connector import connect, Error
import requests
from bs4 import BeautifulSoup


bot = telebot.TeleBot("TOKEN")

all_shoes = {'Кроссовки YEEZY Boost 350 V2', 'Кроссовки YEEZY 450', 'Кроссовки YEEZY 500', 'Кроссовки YEEZY Boost 700 V3', 'Кроссовки YEEZY Boost 700 MNVN', 'Сланцы YEEZY Foam Runner'}
all_sizes = {'4 US': ['36 EU', '3.5 UK', '22 JP'], '4.5 US': ['36.5 EU', '4 UK', '22.5 JP'], '5 US': ['37.5 EU', '4.5 UK', '23 JP'], '5.5 US': ['38 EU', '5 UK', '23.5 JP'], '6 US': ['38.5 EU', '5.5 UK', '24 JP'], '6.5 US': ['39.5 EU', '6 UK', '24.5 JP'], '7 US': ['40 EU', '6.5 UK', '25 JP'], '7.5 US': ['40.5 EU', '7 UK', '25.5 JP'], '8 US': ['41.5 EU', '7.5 UK', '26 JP'], '8.5 US': ['42 EU', '8 UK', '26.5 JP'], '9 US': ['42.5 EU', '8.5 UK', '27 JP'], '9.5 US': ['43.5 EU', '9 UK', '27.5 JP'], '10 US': ['44 EU', '9.5 UK', '28 JP'], '10.5 US': ['44.5 EU', '10 UK', '28.5 JP'], '11 US': ['45.5 EU', '10.5 UK', '29 JP'], '11.5 US': ['46 EU', '11 UK', '29.5 JP'], '12 US': ['46.5 EU', '11.5 UK', '30 JP'], '12.5 US': ['47.5 EU', '12 UK', '30.5 JP'], '13 US': ['48 EU', '12.5 UK', '31 JP'], '13.5 US': ['48.5 EU', '13 UK', '31.5 JP'], '14 US': ['49.5 EU', '13.5 UK', '32 JP'], '14.5 US': ['50 EU', '14 UK', '32.5 JP']}
all_commands = ['Выбрать кроссовки', 'За какими кроссовками я слежу', 'Отменить слежку за конкретными кроссовками', 'Изменить размер', 'info']


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
except Error as err:
    print(err)


def get_html(lot):
    try:
        result = requests.get(lot)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Server error')
        return False


def get_availability(HTML, his_size):
    soup = BeautifulSoup(HTML, 'html.parser')
    avail = soup.findAll('div', class_='access')
    size = soup.findAll('div', class_="product-size")
    print(avail)
    print(size)
    result_avail = 'Товар в наличии' in str(avail)
    result_size = his_size[0] in str(size) or all_sizes[his_size[0]][0] in str(size) or all_sizes[his_size[0]][1] in str(size) or all_sizes[his_size[0]][2] in str(size)
    if result_avail and result_size:
        return 1
    elif result_avail and not result_size:
        return 2
    else:
        return 3


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, replies.rep[0], reply_markup=keyboards.size_keyboard)
    cursor.execute(f'SELECT * FROM yeezy WHERE user_id = {message.chat.id}')
    data = cursor.fetchone()
    if not data:
        cursor.execute(f'INSERT INTO yeezy (user_id) VALUES ({message.chat.id})')
        connection.commit()
    bot.register_next_step_handler(msg, start)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    cursor.execute(f"SELECT shoes1, shoes2, shoes3, size FROM yeezy WHERE user_id = {message.chat.id}")
    data = cursor.fetchone()
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
    cursor.execute(f"UPDATE yeezy SET size = '{message.text}' WHERE user_id = {message.chat.id}")
    connection.commit()


def choice(message, his_shoes, his_size):
    if message.text in all_shoes:
        if message.text in his_shoes:
            msg = bot.send_message(message.chat.id, replies.rep[11], reply_markup=keyboards.fun_keyboard)
        else:
            his_shoes.append(message.text)
            while len(his_shoes) < 3:
                his_shoes.append('no')
            cursor.execute(f"UPDATE yeezy SET shoes1 = '{his_shoes[0]}', shoes2 = '{his_shoes[1]}', shoes3 = '{his_shoes[2]}' WHERE user_id = {message.chat.id}")
            connection.commit()
            msg = bot.send_message(message.chat.id, replies.rep[12], reply_markup=keyboards.fun_keyboard)
        available_size = []
        available_not_size = []
        for i in URLs.URLs[message.text]:
            HTML = get_html(i)
            if HTML:
                result_avail_and_size = get_availability(HTML, his_size)
                if result_avail_and_size == 1:
                    available_size.append(i)
                elif result_avail_and_size == 2:
                    available_not_size.append(i)
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
        cursor.execute(f"UPDATE yeezy SET size = '{message.text}' WHERE user_id = {message.chat.id}")
        connection.commit()
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
        cursor.execute(f"UPDATE yeezy SET shoes1 = '{his_shoes[0]}', shoes2 = '{his_shoes[1]}', shoes3 = '{his_shoes[2]}' WHERE user_id = {message.chat.id}")
        connection.commit()
    else:
        msg = bot.send_message(message.chat.id, replies.rep[9])
        bot.register_next_step_handler(msg, delete, his_shoes)


bot.polling(none_stop=True)
