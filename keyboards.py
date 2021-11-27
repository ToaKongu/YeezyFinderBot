import telebot

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

fun_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
fun_keyboard.row('Я уже ищу твои кросcовки...')