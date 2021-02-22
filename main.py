import telebot
from requests import get
from kinopoisk_parser import random_film, read_pickle_file
from telebot import types

bot = telebot.TeleBot('')


@bot.message_handler(content_types=['text'])
def start_message(message):
    start_message = 'Добро пожаловать! Я бот, который будет помогать Вам с поиском интересных фильмов. ' \
                    'Могу предложить Вам один из топ 250 фильмов КиноПоиска'

    keyboard = types.InlineKeyboardMarkup()
    key_rfb = types.InlineKeyboardButton(text='Фильм из топ-250 по версии КиноПоиска', callback_data='random_film')
    keyboard.add(key_rfb)
    '''key_rfb = types.InlineKeyboardButton(text='Выбрать жанр', callback_data='choose_genre')
    keyboard.add(key_rfb)'''

    bot.send_message(message.chat.id, start_message, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    if call.data == 'random_film':
        keyboard = types.InlineKeyboardMarkup()
        key_rfb = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_rfb)
        key_rfb = types.InlineKeyboardButton(text='Нет', callback_data='random_film')
        keyboard.add(key_rfb)

        film_and_poster = random_film()
        bot.send_photo(call.from_user.id, get(film_and_poster[1]).content)
        bot.send_message(call.from_user.id, film_and_poster[0] + '\n\n' + film_and_poster[2])
        bot.send_message(call.from_user.id, 'Хотите посмотреть этот фильм?', reply_markup=keyboard)

    '''    if call.data == 'choose_genre':
        keyboard = types.InlineKeyboardMarkup()

        genres = read_pickle_file('./data/genres.pickle')
        for key, item in genres.items():
            key_rfb = types.InlineKeyboardButton(text=key, callback_data=item)
            keyboard.add(key_rfb)

        bot.send_message(call.from_user.id, 'Хотите посмотреть этот фильм?', reply_markup=keyboard)'''

    if call.data == 'yes':
        bot.send_message(call.from_user.id, 'Отличный выбор! Приятного просмотра!')


bot.polling(none_stop=True, interval=0)
