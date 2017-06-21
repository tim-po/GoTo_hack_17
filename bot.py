import uuid

import config
import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
import json

bot = telebot.TeleBot(config.token)
custom_butons = {}


# def add_corners(im, rad):
#     circle = Image.new('L', (rad * 2, rad * 2), 0)
#     draw = ImageDraw.Draw(circle)
#     draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
#     alpha = Image.new('L', im.size, 255)
#     w, h = im.size
#     alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
#     alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
#     alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
#     alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
#     im.putalpha(alpha)
#     return im
#
#
# def add_text(im, text, font_size=100, two_strings=False):
#     width, height = im.size
#     draw = ImageDraw.Draw(im)
#     font = ImageFont.truetype("ofont.ru_Impact.ttf", font_size)
#     im = add_corners(im, 400)
#     draw.text((100, 100), text, (0, 0, 0), font=font)
#
#     draw.text((100, height - 120), "Тут будет чей-то текст", (0, 0, 0), font=font)
#     ImageDraw.Draw(im)
#     return im


def get_user(user_id):
    with open('db.json') as data_file:
        user = json.load(data_file).get(str(user_id))
    return user

#
# @bot.message_handler(content_types=['document'])
# def handle_docs_audio(message):
#     markup = types.ReplyKeyboardMarkup(row_width=1)
#     menu = types.KeyboardButton('/menu')
#     markup.add(menu)
#     file_id = message.photo[-1].file_id
#     path = bot.get_file(file_id)
#     extn = '.' + str(path.file_path).split('.')[-1]
#     downloaded_file = bot.download_file(path.file_path)
#     cname = str(uuid.uuid4()) + extn
#     with open('images/' + cname, 'wb') as new_file:
#         new_file.write(downloaded_file)
#     with open('images/' + cname, 'wb') as new_file:
#         p = new_file.read(downloaded_file)
#     photo = add_corners(p
#                         , rad=400)
#     photo_with_text = add_text(photo, message.text)
#     bot.send_photo(chat_id=message.chat.id, document=photo_with_text, reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    welcome_button1 = types.KeyboardButton('участник')
    welcome_button2 = types.KeyboardButton('преп')
    welcome_button3 = types.KeyboardButton('орг')
    welcome_button4 = types.KeyboardButton('модер')
    markup.add(welcome_button1, welcome_button2, welcome_button3, welcome_button4)
    bot.send_message(message.chat.id, text='Вы кто?', reply_markup=markup)


@bot.message_handler(func=lambda message: True if
message.text == 'участник' or message.text == 'преп' or message.text == 'орг' or message.text == 'модер'
else False)
def send_message_token(message):
    token_req = message
    if message.text == 'участник':
        markup = types.ReplyKeyboardMarkup(row_width=1)
        welcome_button1 = types.KeyboardButton('ад')
        welcome_button2 = types.KeyboardButton('прекладное')
        welcome_button3 = types.KeyboardButton('биолог')
        welcome_button4 = types.KeyboardButton('роботех')
        markup.add(welcome_button1, welcome_button2, welcome_button3, welcome_button4)
        bot.send_message(message.chat.id,
                         'окей ты участник, наслаждайся урезаным функционалом и выбери плз свое направление',
                         reply_markup=markup)
    elif message.text == 'преп' or 'орг' or 'модер':
        markup2 = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, 'введи токен', reply_markup=markup2)
    return token_req


@bot.message_handler(func=lambda message: True if
message.text == 'ад' or message.text == 'прекладное' or message.text == 'биолог' or message.text == 'роботех'
else False)
def send_mesage(message):
    group_id = {'роботех': 'rt', 'ад': 'ad', 'прекладное': 'pr', 'биолог': 'bi'}
    with open('db.json') as data_file:
        data = json.load(data_file)
    while data.get(str(message.from_user.id)) is not None:
        data.pop(str(message.from_user.id))
    data[message.from_user.id] = [group_id[message.text]]
    with open('db.json', 'w') as outfile:
        json.dump(data, outfile)


@bot.message_handler(func=lambda message: True if
message.reply_to_message == send_message_token or
message.text == 'преп token' or message.text == 'орг token' or message.text == 'Q3xzc6vv'
else False)
def send_mesage(message):
    user_class = {'преп token': 'prep', 'орг token': 'org', 'Q3xzc6vv': 'tvorog'}
    with open('db.json') as data_file:
        data = json.load(data_file)
    while data.get(str(message.from_user.id)) is not None:
        data.pop(str(message.from_user.id))
    data[message.from_user.id] = [user_class[message.text]]
    with open('db.json', 'w') as outfile:
        json.dump(data, outfile)
    if message.text == 'преп token':
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'оке ты преп тебе доступны функции препода', reply_markup=markup)
    elif message.text == 'орг token':
        markup2 = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'оке ты орг тебе доступны функции организатора', reply_markup=markup2)
    elif message.text == 'мастер на все руки token':
        markup3 = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'оке ты модер тебе доступны все функции', reply_markup=markup3)
    else:
        bot.send_message(chat_id=message.chat.id, text='токен не верен, иди учись школьник')


# @bot.message_handler(func=lambda message: True if
# len(get_user(message.from_user.id)) > 2 and message.text == ''
# else False)
# def send_mesage_prep(message):
#     markup = types.ReplyKeyboardRemove(selective=False)
#     bot.send_message(message.chat.id, 'оке ты преп тебе доступны преп функции', reply_markup=markup)


@bot.message_handler(commands=['menu'])
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    day_deals = types.KeyboardButton('расписание')
    next_menu = types.KeyboardButton('меню спец команд')
    # coordination = types.KeyboardButton('меню координации')
    # sticker = types.KeyboardButton('редактер стикеров')
    # control_panel = types.KeyboardButton('панель управления')
    # markup = types.ReplyKeyboardRemove(selective=False)
    if len(get_user(message.from_user.id)[0]) <= 2:
        markup.add(day_deals, next_menu)
    elif get_user(message.from_user.id)[0] == 'prep':
        markup.add(day_deals, next_menu)


    elif get_user(message.from_user.id)[0] == 'org':
        markup.add(day_deals, next_menu)


    elif get_user(message.from_user.id)[0] == 'tvorog':
        markup.add(day_deals, next_menu)
    bot.send_message(message.chat.id, 'меню', reply_markup=markup)


@bot.message_handler(func=lambda message: True if
message.text == 'расписание'
else False)
def send_hw_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    menu = types.KeyboardButton('/menu')
    markup.add(menu)
    data = open('day_deals.txt', 'r')
    data2 = data.read()

    if len(get_user(message.from_user.id)[0]) <= 2:
        bot.send_message(message.chat.id, data2, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'скинь мне расписание с пометкой РАСП в начале сообщения'
                         + 'на данный момент:\n' + data2[4:],
                         reply_markup=markup)
    data.close


@bot.message_handler(func=lambda message: True if
message.text[:4] == 'РАСП'
else False)
def send_hw_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    menu = types.KeyboardButton('/menu')
    markup.add(menu)
    data = message.text
    data2 = open('day_deals.txt', 'w')
    data2.write(data)
    data2.close
    bot.send_message(message.chat.id, 'спасибо',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True if
message.text in ['меню спец команд', 'настройка кастомных кнопок', 'название моей деректории',
                 'внутреннюю кнопку 1', 'внутреннюю кнопку 2', 'внутреннюю кнопку 3', 'внутреннюю кнопку 4'] else False)
def send_button_menu(message):
    button = types.KeyboardButton('настройка кастомных кнопок')
    markup = types.ReplyKeyboardMarkup(row_width=1)
    menu = types.KeyboardButton('/menu')
    if message.text == 'меню спец команд':
        with open('custom_buttons.json') as data_file:
            custom_butons = json.load(data_file)
        if len(get_user(message.from_user.id)[0]) >= 2:
            markup.add(button)
        n = 0
        for i in custom_butons.keys():
            if i[:13] == 'user_dir_name':
                n += 1
        for i in range(n):
            print(i)
            # button_g = 'button' + str(i)
            if custom_butons.get('user_dir_name' + str(i + 1)) is not None:
                button_g = types.KeyboardButton(str(custom_butons.get('user_dir_name' + str(i + 1))))
                markup.add(button_g)
                # else:
                #     button_g = types.KeyboardButton(str(custom_butons.get('user_dir_name' + str(i))))

        bot.send_message(message.chat.id, 'меню спец команд',
                         reply_markup=markup)
    if message.text == 'настройка кастомных кнопок':
        change_dir = types.KeyboardButton('название кнопки')
        inner_button = types.KeyboardButton('функцию кнопки')
        inner_button2 = types.KeyboardButton('внутреннюю кнопку 2')
        inner_button3 = types.KeyboardButton('внутреннюю кнопку 3')
        inner_button4 = types.KeyboardButton('внутреннюю кнопку 4')
        markup.add(menu, change_dir, inner_button)
        bot.send_message(message.chat.id, 'что надо настроить?',
                         reply_markup=markup)
    elif message.text == 'название кнопки':
        bot.send_message(message.chat.id, 'название кнопки с пометкой ДРЕ и номером например ДРЕ1',
                         reply_markup=markup)
    elif message.text == 'функцию кнопки':
        i2 = message.text[-1:]
        name = types.KeyboardButton('название кнопки с пометкой ДРЕ и номером например ДРЕ1' + str(i2))
        funk = types.KeyboardButton('напиши функционал кнопки c пометкой НАЗВ и номером например НАЗВ1')
        markup.add(menu)
        bot.send_message(message.chat.id, 'напиши функционал кнопки c пометкой НАЗВ и номером например НАЗВ1',
                         reply_markup=markup)


ex = []
for i in range(9):
    if custom_butons.get('user_dir_name' + str(i)) is not None:
        ex.append('user_dir_name' + str(i))
n = 0
for i in custom_butons.keys():
    if i[:13] == 'user_dir_name':
        n += 1


# @bot.message_handler(func=lambda message: True if
# message.text == 'редактер стикеров' else False)
# def send_button_menu(message):
#     bot.send_message(message.chat.id, 'скинь мне фоточку и текст')


# @bot.message_handler(func=lambda message: True if
# message.text in ['функционал кнопки', 'название кнопки 1', 'название кнопки 2',
#                  'название кнопки 3', 'название кнопки 4']
# else False)
# def send_hw_menu(message):
#     i2 = message.text[-1:]
#     markup = types.ReplyKeyboardMarkup(row_width=1)
#     menu = types.KeyboardButton('/menu')
#     markup.add(menu)
#     if message.text[:-2] == 'название кнопки':
#         bot.send_message(message.chat.id, 'напиши мне название с пометкой НАЗВ' + i2 + ' в начале',
#                          reply_markup=markup)
#     elif message.text[:-2] == 'название кнопки':
#         bot.send_message(message.chat.id, 'напиши все что хочешь засунуть в кнопку'
#                                           '(ссылки, команды, объяснение распостраненных проблем)'
#                                           ', с пометкой ФУН ' + i2 + ' в начале',
#                          reply_markup=markup)


@bot.message_handler(func=lambda message: True if
message.text[:3] == 'ДЕР' or message.text[:4] == 'НАЗВ' or message.text[:3] == 'ФУН' and len(message.text) > 5
else False)
def send_hw_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    menu = types.KeyboardButton('/menu')
    with open('custom_buttons.json') as data_file:
        custom_butons = json.load(data_file)
    if message.text[:3] == 'ДЕР':
        i2 = message.text[3]
        custom_butons['user_dir_name' + str(i2)] = message.text[5:]
    elif message.text[:4] == 'НАЗВ':
        i2 = message.text[4]
        custom_butons['user_button_name' + str(i2)] = message.text[6:]
    elif message.text[:3] == 'ФУН':
        i2 = message.text[3]
        custom_butons['user_fun' + str(i2)] = [message.text[5:], message.from_user.id]
    with open('custom_buttons.json', 'w') as outfile:
        json.dump(custom_butons, outfile)
    markup.add(menu)
    bot.send_message(message.chat.id, 'понял принял',
                     reply_markup=markup)


values = []
for i in custom_butons.values():
    values.append(i[0])

print(list(custom_butons.values()))

with open('custom_buttons.json') as data_file:
        custom_butons = json.load(data_file)

@bot.message_handler(func=lambda message: True if
message.text in list(custom_butons.values())
else False)
def send_hw_menu(message):
    with open('custom_buttons.json') as data_file:
        custom_butons = json.load(data_file)
    text = []
    for i in range(9):
        if custom_butons.get('user_dir_name' + str(i)) == message.text:
            text.append(custom_butons.get('user_button_name' + str(i)))
    markup = types.ReplyKeyboardMarkup(row_width=1)
    menu = types.KeyboardButton('/menu')
    markup.add(menu)
    bot.send_message(message.chat.id, text, reply_markup=markup)


# @bot.message_handler(func=lambda message: True if
# message.text == user_text
# else False)
# def send_hw_menu(message):
#     markup = types.ReplyKeyboardMarkup(row_width=1)
#     menu = types.KeyboardButton('/menu')
#     button1 = types.KeyboardButton(button_name1)
#     button2 = types.KeyboardButton('button2')
#     button3 = types.KeyboardButton('button3')
#     button4 = types.KeyboardButton('button4')
#     button5 = types.KeyboardButton('button5')
#     button6 = types.KeyboardButton('button6')
#     button7 = types.KeyboardButton('button7')
#     button8 = types.KeyboardButton('button8')
#     markup.add(button1, button2, button3, button4, button5, button6, button7, button8, menu)
#     bot.send_message(message.chat.id, text,
#                      reply_markup=markup)
print(custom_butons)

if __name__ == '__main__':
    bot.polling(none_stop=True)
