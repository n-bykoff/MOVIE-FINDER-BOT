import telebot
from requests import get
from myparser import random_film
from telebot import types

bot = telebot.TeleBot('')


@bot.message_handler(content_types=['text'])
def start_message(message):
    answer1 = 'Добро пожаловать! Я бот, который будет помогать вам с поиском интересных фильмов'

    keyboard = types.InlineKeyboardMarkup()
    key_rfb = types.InlineKeyboardButton(text='Рандомный фильм', callback_data='random_film')
    keyboard.add(key_rfb)

    bot.send_message(message.chat.id, answer1, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    keyboard = types.InlineKeyboardMarkup()
    key_rfb = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_rfb)
    key_rfb = types.InlineKeyboardButton(text='Нет', callback_data='random_film')
    keyboard.add(key_rfb)

    if call.data == 'random_film':
        film_and_poster = random_film()
        bot.send_photo(call.from_user.id, get(film_and_poster[1]).content)
        bot.send_message(call.from_user.id, film_and_poster[0])
        bot.send_message(call.from_user.id, 'Хотите посмотреть этот фильм?', reply_markup=keyboard)
    if call.data == 'yes':
        bot.send_message(call.from_user.id, 'Отлично! Приятного просмотра!')


bot.polling(none_stop=True, interval=0)
