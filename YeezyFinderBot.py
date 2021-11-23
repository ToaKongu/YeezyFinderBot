import telebot
import sqlite3
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

bot = telebot.TeleBot("TOKEN")
URLs = {'Кроссовки YEEZY Boost 350 V2': ['https://brandshop.ru/goods/324555/gw3773/', 'https://brandshop.ru/goods/278657/gw0089/', 'https://brandshop.ru/goods/303149/gw2871/', 'https://brandshop.ru/goods/283577/gy7658/', 'https://brandshop.ru/goods/250390/fz5000/', 'https://brandshop.ru/goods/21769/krossovki-adidas-originals-yeezy-boost-350-v2-core-black-core-black-red/', 'https://brandshop.ru/goods/253698/fz5246/', 'https://brandshop.ru/goods/201230/krossovki-adidas-originals-yeezy-boost-350-v2-reflective-cloud-white/', 'https://brandshop.ru/goods/179136/krossovki-adidas-originals-yeezy-boost-350-v2-glow-glow-glow/', 'https://brandshop.ru/goods/269439/fz5240/', 'https://brandshop.ru/goods/215719/krossovki-adidas-originals-yeezy-boost-350-v2-yecheil-yecheil-yecheil/', 'https://brandshop.ru/goods/312357/gy3438/', 'https://brandshop.ru/goods/211959/krossovki-adidas-originals-yeezy-boost-350-v2-yeezreel-yeezreel-yeezreel/', 'https://brandshop.ru/goods/229638/krossovki-adidas-originals-yeezy-boost-350-v2-zyon-zyon-zyon/', 'https://brandshop.ru/goods/224296/krossovki-adidas-originals-yeezy-boost-350-v2-cinder-cinder-cinder/', 'https://brandshop.ru/goods/181084/krossovki-adidas-originals-yeezy-boost-350-v2-black-black-black/', 'https://brandshop.ru/goods/226944/krossovki-adidas-originals-yeezy-boost-350-v2-linen-linen-linen/', 'https://brandshop.ru/goods/18915/krossovki-adidas-originals-yeezy-boost-350-v2-stealth-grey-beluga-solar-red/', 'https://brandshop.ru/goods/20279/krossovki-adidas-originals-yeezy-boost-350-v2-core-black-red/', 'https://brandshop.ru/goods/20827/krossovki-adidas-originals-yeezy-boost-350-v2-core-black-vintage-white/', 'https://brandshop.ru/goods/20278/krossovki-adidas-originals-yeezy-boost-350-v2-core-black-green/', 'https://brandshop.ru/goods/80422/krossovki-adidas-originals-yeezy-boost-350-v2-blue-tint-grey-three-high-resolution-red/', 'https://brandshop.ru/goods/20277/krossovki-adidas-originals-yeezy-boost-350-v2-core-black-cooper-metallic/', 'https://brandshop.ru/goods/147706/krossovki-adidas-originals-yeezy-boost-350-v2-sesame-sesame-sesame/', 'https://brandshop.ru/goods/44750/krossovki-adidas-originals-yeezy-boost-350-v2-white-core-black-red/', 'https://brandshop.ru/goods/36728/krossovki-adidas-originals-yeezy-boost-350-v2-triple-white/', 'https://brandshop.ru/goods/201738/krossovki-adidas-originals-yeezy-boost-350-v2-citrin-citrin-citrin/', 'https://brandshop.ru/goods/167506/krossovki-adidas-originals-yeezy-boost-350-v2-trfrm-grey-grey-grey/', 'https://brandshop.ru/goods/148169/krossovki-adidas-originals-yeezy-boost-350-v2-semi-frozen-yellow-raw-steel-red/', 'https://brandshop.ru/goods/201752/krossovki-adidas-originals-yeezy-boost-350-v2-cloud-white-cloud-white-cloud-white/'], 
        'Кроссовки YEEZY 450': ['https://brandshop.ru/goods/303159/gy5368/', 'https://brandshop.ru/goods/280994/h68038/'],
        'Кроссовки YEEZY 500': ['https://brandshop.ru/goods/324560/gx3606/'],
        'Кроссовки YEEZY Boost 700 V3': ['https://brandshop.ru/goods/269447/gy0189/'], 
        'Кроссовки YEEZY Boost 700 MNVN': ['https://brandshop.ru/goods/299420/gz3079/', 'https://brandshop.ru/goods/319684/gz0717/'], 
        'Сланцы YEEZY Foam Runner': ['https://brandshop.ru/goods/324550/gw3355/', 'https://brandshop.ru/goods/310052/gw3354/', 'https://brandshop.ru/goods/310057/gx8774/', 'https://brandshop.ru/goods/298110/gv7903/', 'https://brandshop.ru/goods/286674/fy4567/', 'https://brandshop.ru/goods/286679/gv7904/']}

all_shoes = {'Кроссовки YEEZY Boost 350 V2', 'Кроссовки YEEZY 450', 'Кроссовки YEEZY 500', 'Кроссовки YEEZY Boost 700 V3', 'Кроссовки YEEZY Boost 700 MNVN', 'Сланцы YEEZY Foam Runner'}
all_sizes = {'4 US': ['36 EU', '3.5 UK', '22 JP'], '4.5 US': ['36.5 EU', '4 UK', '22.5 JP'], '5 US': ['37.5 EU', '4.5 UK', '23 JP'], '5.5 US': ['38 EU', '5 UK', '23.5 JP'], '6 US': ['38.5 EU', '5.5 UK', '24 JP'], '6.5 US': ['39.5 EU', '6 UK', '24.5 JP'], '7 US': ['40 EU', '6.5 UK', '25 JP'], '7.5 US': ['40.5 EU', '7 UK', '25.5 JP'], '8 US': ['41.5 EU', '7.5 UK', '26 JP'], '8.5 US': ['42 EU', '8 UK', '26.5 JP'], '9 US': ['42.5 EU', '8.5 UK', '27 JP'], '9.5 US': ['43.5 EU', '9 UK', '27.5 JP'], '10 US': ['44 EU', '9.5 UK', '28 JP'], '10.5 US': ['44.5 EU', '10 UK', '28.5 JP'], '11 US': ['45.5 EU', '10.5 UK', '29 JP'], '11.5 US': ['46 EU', '11 UK', '29.5 JP'], '12 US': ['46.5 EU', '11.5 UK', '30 JP'], '12.5 US': ['47.5 EU', '12 UK', '30.5 JP'], '13 US': ['48 EU', '12.5 UK', '31 JP'], '13.5 US': ['48.5 EU', '13 UK', '31.5 JP'], '14 US': ['49.5 EU', '13.5 UK', '32 JP'], '14.5 US': ['50 EU', '14 UK', '32.5 JP']}
all_commands = {'Выбрать кроссовки', 'За какими кроссовками я слежу', 'Отменить слежку за конкретными кроссовками', 'Изменить размер', 'info'}

menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.row('Выбрать кроссовки')
menu_keyboard.row('За какими кроссовками я слежу')
menu_keyboard.row('Отменить слежку за конкретными кроссовками')
menu_keyboard.row('Изменить размер')
menu_keyboard.row('info')

choice_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
choice_keyboard.row('Отмена')
choice_keyboard.row('Кроссовки YEEZY Boost 350 V2')
choice_keyboard.row('Кроссовки YEEZY 450')
choice_keyboard.row('Кроссовки YEEZY 500')
choice_keyboard.row('Кроссовки YEEZY Boost 700 V3')
choice_keyboard.row('Кроссовки YEEZY Boost 700 MNVN')
choice_keyboard.row('Сланцы YEEZY Foam Runner')

delete_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
delete_keyboard.row('Кроссовки YEEZY Boost 350 V2')
delete_keyboard.row('Кроссовки YEEZY 450')
delete_keyboard.row('Кроссовки YEEZY 500')
delete_keyboard.row('Кроссовки YEEZY Boost 700 V3')
delete_keyboard.row('Кроссовки YEEZY Boost 700 MNVN')
delete_keyboard.row('Сланцы YEEZY Foam Runner')

size_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
size_keyboard.row('4 US', '4.5 US', '5 US')
size_keyboard.row('5.5 US', '6 US', '6.5 US')
size_keyboard.row('7 US', '7.5 US', '8 US')
size_keyboard.row('8.5 US', '9 US', '9.5 US')
size_keyboard.row('10 US', '10.5 US', '11 US')
size_keyboard.row('11.5 US', '12 US', '12.5 US')
size_keyboard.row('13 US', '13.5 US', '14 US')
size_keyboard.row('14 US')

yon_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
yon_keyboard.row('Да', 'Нет')


try:
    sqlite_connection = sqlite3.connect(
        'sqlite_YEEZY.db', check_same_thread=False)
    sqlite_create_table_query = 'CREATE TABLE IF NOT EXISTS yeezy (user_id INT, shoes TEXT);'

    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    print("Таблица SQLite с регистарцией создана")

except sqlite3.Error as error:
    print("Ошибка при подключении к SQLite с регистрацией", error)
    pass


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

'''
@bot.message_handler()
def send_message_himself(message):
    while True:
        cursor.execute('SELECT * from yeezy')
        data = cursor.fetchall()
        for i in all_shoes:
            pass
        time.sleep(3)
'''


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Привет, я YeezyFinderBot. Моя задача состоит в том, чтобы помочь тебе отследить появление твоих любимых кроссовок в магазинах\nВыбери свой размер обуви', reply_markup=size_keyboard)
    cursor.execute('SELECT * from yeezy')
    data = cursor.fetchall()
    his_size = []
    for i in data:
        if i[0] == message.chat.id and i[1][-2:] == 'US':
            his_size.append(i[1])
        if len(his_size) == 1:
            break
    bot.register_next_step_handler(msg, start, his_size)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text in all_commands and message.text != 'info':
        cursor.execute('SELECT * from yeezy')
        data = cursor.fetchall()
        his_shoes = []
        his_size = []
        for i in data:
            if i[0] == message.chat.id and i[1][-2:] != 'US':
                his_shoes.append(i[1])
            elif i[0] == message.chat.id and i[1][-2:] == 'US':
                his_size.append(i[1])
            if len(his_shoes) == 3:
                break


    if message.text == 'Выбрать кроссовки':
        if len(his_shoes) == 3:
            msg = bot.send_message(message.chat.id, f'К сожалению, одновременно можно следить только за тремя парами обуви :(\n\nТы уже следишь за следующими кроссовками:\n • {his_shoes[0]}\n • {his_shoes[1]}\n • {his_shoes[2]}\nЕсли хочешь следить за другими кроссовками, сначала отмени слежку за какими-то из своих')
        else:
            if len(his_shoes) == 1:
                msg = bot.send_message(message.chat.id, f'Ты следишь за следующими позициями:\n • {his_shoes[0]}')
            elif len(his_shoes) == 2:
                msg = bot.send_message(message.chat.id, f'Ты следишь за следующими позициями:\n • {his_shoes[0]}\n • {his_shoes[1]}')
            msg = bot.send_message(message.chat.id, 'За появлением какой обуви ты хочешь следить? (Можно отслеживать максимум 3 модели)', reply_markup=choice_keyboard)
            bot.register_next_step_handler(msg, choice, his_shoes, his_size)


    elif message.text == 'За какими кроссовками я слежу':
        if len(his_shoes) == 0:
            msg = bot.send_message(message.chat.id, f'Ты пока не выбрал, за какими кроссовками следить')
        elif len(his_shoes) == 1:
            msg = bot.send_message(message.chat.id, f'Ты следишь за следующими позициями:\n • {his_shoes[0]}')
        elif len(his_shoes) == 2:
            msg = bot.send_message(message.chat.id, f'Ты следишь за следующими позициями:\n • {his_shoes[0]}\n • {his_shoes[1]}')
        elif len(his_shoes) == 3:
            msg = bot.send_message(message.chat.id, f'Ты следишь за следующими позициями:\n • {his_shoes[0]}\n • {his_shoes[1]}\n • {his_shoes[2]}')


    elif message.text == 'Отменить слежку за конкретными кроссовками':
        if len(his_shoes) == 0:
            msg = bot.send_message(message.chat.id, 'Сейчас ты не следишь ни за какими кроссовками')
            return
        elif len(his_shoes) == 1:
            msg = bot.send_message(message.chat.id, f'Ты следишь за следующими позициями:\n • {his_shoes[0]}')
        elif len(his_shoes) == 2:
            msg = bot.send_message(message.chat.id, f'Ты следишь за следующими позициями:\n • {his_shoes[0]}\n • {his_shoes[1]}')
        elif len(his_shoes) == 3:
            msg = bot.send_message(message.chat.id, f'Ты следишь за следующими позициями:\n • {his_shoes[0]}\n • {his_shoes[1]}\n • {his_shoes[2]}')
        msg = bot.send_message(message.chat.id, 'За какими кроссовками ты больше не хочешь следить?', reply_markup=delete_keyboard)
        bot.register_next_step_handler(msg, delete, his_shoes)


    elif message.text == 'Изменить размер':
        msg = bot.send_message(message.chat.id, 'Выбери размер обуви', reply_markup=size_keyboard)
        bot.register_next_step_handler(msg, change_size, his_size)


    elif message.text == 'info':
        msg = bot.send_message(message.chat.id, 'Я YeezyFinderBot. Моя задача состоит в том, чтобы помочь тебе отследить появление твоих любимых кроссовок в магазинах\n\nЯ ищу кроссовки в следующих магазинах:\n • brandshop.ru')


    else:
        msg = bot.send_message(message.chat.id, 'Прости, я не знаю такой команды! Выбери что-то из предложенных снизу...')


def start(message, his_size):
    msg = bot.send_message(message.chat.id, 'Отлично!', reply_markup=menu_keyboard)
    if his_size:
        cursor.execute('DELETE from yeezy where user_id = ? and shoes = ?', (message.chat.id, his_size[0]))
    cursor.execute('INSERT INTO yeezy VALUES (?, ?)', (message.chat.id, message.text))
    sqlite_connection.commit()


def choice(message, his_shoes, his_size):
    if message.text in all_shoes:
        if message.text in his_shoes:
            msg = bot.send_message(message.chat.id, 'За этими кроссовками ты уже следишь! Но все же подожди минутку, ищу модели...')
        else:
            cursor.execute('INSERT INTO yeezy VALUES (?, ?)', (message.chat.id, message.text))
            sqlite_connection.commit()
            his_shoes.append(message.text)
            msg = bot.send_message(message.chat.id, 'Отличный выбор! Подожди минутку, ищу модели...')
        available_size = []
        available_not_size = []
        for i in URLs[message.text]:
            HTML = get_html(i)
            if HTML:
                result_avail_and_size = get_availability(HTML, his_size)
                if result_avail_and_size == 1:
                    available_size.append(i)
                elif result_avail_and_size == 2:
                    available_not_size.append(i)
        if available_size:
            msg = bot.send_message(message.chat.id, 'Сейчас можно купить следующие модели:', reply_markup=menu_keyboard)
            for i in available_size:
                msg = bot.send_message(message.chat.id, f'{i}')
            msg = bot.send_message(message.chat.id, 'Торопись, чтобы успеть их урвать!')
        elif not available_size and available_not_size:
            msg = bot.send_message(message.chat.id, 'К сожалению, этой модели на твой размер ноги нет, но есть на другие размеры\n\nХочешь на них взглянуть?', reply_markup=yon_keyboard)
            bot.register_next_step_handler(msg, choice_2, available_not_size)
        else:
            msg = bot.send_message(message.chat.id, 'К сожалению, эти кроссовки пока что нельзя нигде купить. Но я пришлю тебе уведомление, когда они появятся в продаже!', reply_markup=menu_keyboard)
    elif message.text == 'Отмена':
        msg = bot.send_message(message.chat.id, 'Не хочешь - не надо!', reply_markup=menu_keyboard)
    else:
        msg = bot.send_message(message.chat.id, 'Прости, я не знаю такой команды! Выбери что-то из предложенных снизу...')
        bot.register_next_step_handler(msg, choice, his_shoes, his_size)


def choice_2(message, available_not_size):
    if message.text == 'Да':
        msg = bot.send_message(message.chat.id, 'Хорошо! Вот они:', reply_markup=menu_keyboard)
        for i in available_not_size:
            msg = bot.send_message(message.chat.id, f'{i}')
    elif message.text == 'Нет':
        msg = bot.send_message(message.chat.id, 'Как скажешь!', reply_markup=menu_keyboard)
    else:
        msg = bot.send_message(message.chat.id, 'Прости, я не знаю такой команды! Выбери что-то из предложенных снизу...')
        bot.register_next_step_handler(msg, choice_2, available_not_size)


def change_size(message, his_size):
    if message.text in his_size:
        msg = bot.send_message(message.chat.id, 'Этот размер уже выбран', reply_markup=menu_keyboard)
    elif message.text in all_sizes:
        msg = bot.send_message(message.chat.id, 'Отлично, размер изменен!', reply_markup=menu_keyboard)
        cursor.execute('DELETE from yeezy where user_id = ? and shoes = ?', (message.chat.id, his_size[0]))
        cursor.execute('INSERT INTO yeezy VALUES (?, ?)', (message.chat.id, message.text))
        sqlite_connection.commit()
    else:
        msg = bot.send_message(message.chat.id, 'Прости, я не знаю такой команды! Выбери что-то из предложенных снизу...')
        bot.register_next_step_handler(msg, change_size, his_size)


def delete(message, his_shoes):
    if message.text not in his_shoes and message.text in all_shoes:
        msg = bot.send_message(message.chat.id, 'За этими кроссовками ты и не следил!', reply_markup=menu_keyboard)
    elif message.text in his_shoes:
        msg = bot.send_message(message.chat.id, 'Кроссовки удалены!', reply_markup=menu_keyboard)
        cursor.execute('DELETE from yeezy where user_id = ? and shoes = ?', (message.chat.id, message.text))
        sqlite_connection.commit()
    else:
        msg = bot.send_message(message.chat.id, 'Прости, я не знаю такой команды! Выбери что-то из предложенных снизу...')
        bot.register_next_step_handler(msg, delete, his_shoes)


bot.polling(none_stop=True)
