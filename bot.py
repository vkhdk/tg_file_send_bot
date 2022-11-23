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

#read authorization data
authorization_data = pd.read_csv('./store/authorization_data.csv', sep=',')

@bot.message_handler(chat_types=['private'],commands=['start'])
def start_keyboard(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Авторизация')
    btn2 = types.KeyboardButton(text='Инструкция')
    kb.add(btn1,btn2)
    bot.send_message(message.chat.id, 'Меню',reply_markup=kb)

bot.polling()