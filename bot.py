# importing public libraries
import datetime as dt
from datetime import datetime
import time
import pandas as pd
import sqlite3

# importing library from pyTelegramBotAPI
import telebot
# library for keyboard settings
from telebot import types

# importing internal modules
import secrets

# initializing the bot
# store token in file secrets.py
bot = telebot.TeleBot(secrets.bot_token)


# initializing database
chat_id_db_link = secrets.chat_id_db_link + secrets.chat_id_db_name
connect = sqlite3.connect(chat_id_db_link)
cursor = connect.cursor()
# creating a table
cursor.execute("""CREATE TABLE IF NOT EXISTS chat_id_data(
    chat_id INTEGER,
    login TEXT,
    timestamp INTEGER
    )""")
connect.commit()


@bot.message_handler(chat_types=['private'], commands=['start'])
def start_keyboard(message):
    # creating a keyboard
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='👤 Log in')
    btn2 = types.KeyboardButton(text='📖 Manual')
    kb.add(btn1, btn2)
    bot.send_message(
        message.chat.id, f'Hi, {message.from_user.first_name}!', reply_markup=kb)


@bot.message_handler(chat_types=['private'], content_types=['text'])
def keyboard_navigation(message):
    if message.text == '📖 Manual':
        bot.send_message(message.chat.id, (f'Bot is designed to receive files\n'
                                           f'To receive the file, you need to log in'
                                           ))
    if message.text == '👤 Log in':
        msg = bot.send_message(
            message.chat.id, (f'To log in, enter your username'))
        bot.register_next_step_handler(msg, check_login)


def check_login(message):
    chat_id = message.chat.id
    user_login = message.text
    timestamp_now = int(time.time())
    user_info = [chat_id, user_login, timestamp_now]
    authorization_data_full = authorization_data()
    authorization_data_current = authorization_data_full[
        authorization_data_full['login'] == user_login]
    # check login in google doc
    if len(authorization_data_current) > 0:
        if authorization_data_current['access'].values[:1][0].lower() == 'yes':
            # database connect
            connect = sqlite3.connect(chat_id_db_link)
            cursor = connect.cursor()
            # checking for duplication
            cursor.execute(f"SELECT * "
                           f"FROM chat_id_data "
                           f"WHERE chat_id_data.chat_id = {chat_id} "
                           f"AND chat_id_data.login = '{user_login}'")
            cursor_output = cursor.fetchone()
            if cursor_output is None:
                # write to db
                cursor.execute(
                    "INSERT INTO chat_id_data VALUES(?,?,?);", user_info)
                connect.commit()
                # send next question
                msg = bot.send_message(
                    message.chat.id, (f'enter your password'))
                bot.register_next_step_handler(msg, check_password)
            else:
                # update timestamp in db
                cursor.execute(
                    f"UPDATE chat_id_data "
                    f"SET timestamp = {user_info[2]} "
                    f"WHERE chat_id_data.chat_id = {chat_id} "
                    f"AND chat_id_data.login = '{user_login}'")
                connect.commit()
                # send next question
                msg = bot.send_message(
                    message.chat.id, (f'enter your password'))
                bot.register_next_step_handler(msg, check_password)
        else:
            bot.send_message(
                message.chat.id, (f'Access for user {user_login} denied'))
    else:
        bot.send_message(message.chat.id, (f'Username {user_login} not found'))


def check_password(message):
    chat_id = message.chat.id
    # database connect
    connect = sqlite3.connect(chat_id_db_link)
    cursor = connect.cursor()

    # take login from db
    #cursor.execute(f"SELECT * "
    #               f"FROM chat_id_data "
    #               f"WHERE chat_id_data.chat_id = {chat_id} "
    #               f"AND chat_id_data.login = '{user_login}'")
    #cursor_output = cursor.fetchone()
    #user_password = 
    
    bot.send_message(
        message.chat.id, (f'Пока тут все!, но вот тебе твой логин {message.text}'))


# read authorization data
# file structure "login,password,chat_id,access"
# get_data_from_goolge_docs.py
def authorization_data():
    link_authorization_data = secrets.authorization_data_link + \
        secrets.authorization_data_name
    authorization_data = pd.read_csv(f'{link_authorization_data}.csv', sep=',')
    return authorization_data


bot.polling()
