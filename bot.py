#importing public libraries
import datetime as dt
from datetime import datetime
import logging
import pandas as pd
import json

#importing library from pyTelegramBotAPI
import telebot
#library for keyboard settings
from telebot import types

#importing internal modules
import secrets

#initializing the bot
#store token in file secrets.py
bot = telebot.TeleBot(secrets.bot_token)

@bot.message_handler(chat_types = ['private'], commands = ['start'])
def start_keyboard(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn1 = types.KeyboardButton(text = '👤 Авторизация')
    btn2 = types.KeyboardButton(text = '📖 Инструкция')
    kb.add(btn1,btn2)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!', reply_markup = kb)

@bot.message_handler(chat_types = ['private'], content_types = ['text'])
def keyboard_navigation(message):
    if message.text == '📖 Инструкция':
        bot.send_message(message.chat.id, (f'Бот создан для отправки файлов за указанную дату.\n'
                                           f'Для получения файла необходимо авторизоваться.'
                                           ))
    if message.text == '👤 Авторизация':
        msg = bot.send_message(message.chat.id, (f'Для авторизации необходимо ввести логин и пароль.\n'
                                                 f'Введите ЛОГИН'))
        bot.register_next_step_handler(msg, check_login)

def check_login(message):
    user_login = message.text
    authorization_data_full = authorization_data()
    authorization_data_current = authorization_data_full[authorization_data_full['login'] == user_login]
    if len(authorization_data_current)>0:
        msg = bot.send_message(message.chat.id, (f'Введите ПАРОЛЬ'))
        bot.register_next_step_handler(msg, check_password)
    else: 
        bot.send_message(message.chat.id, (f'Пользователь с логином {user_login} не найден'))

def check_password(message):
    bot.send_message(message.chat.id, (f'Пока тут все!'))




#read authorization data
def authorization_data():
    link_authorization_data = secrets.authorization_data_link + secrets.authorization_data_name
    authorization_data = pd.read_csv(f'{link_authorization_data}.csv', sep=',')
    return authorization_data

bot.polling()