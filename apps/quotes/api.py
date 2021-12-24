import os
import random
import telebot
from telebot import types
from config import DB_PATH
from apps.quotes.utils import Quote, update_great_quotes
from apps.quotes.sqlite import QuotesSQLiteDatabase, QuotesSubscriptionsLimitException


def quotes_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_great_quote = types.KeyboardButton('🔥 Великая цитата')
    button_quote_subscription = types.KeyboardButton('✉️ Хочу регулярно получать цитаты')
    markup.add(button_great_quote)
    markup.add(button_quote_subscription)
    return markup

def quotes_subscription_name_menu():
    markup = types.InlineKeyboardMarkup()
    button_great_quote_subscription = types.InlineKeyboardButton('🔥 Великая цитата', callback_data='great_quotes')
    markup.add(button_great_quote_subscription)
    return markup

def quotes_subscription_type_menu():
    markup = types.InlineKeyboardMarkup()
    button_every_day = types.InlineKeyboardButton('Каждый день', callback_data='every_day')
    button_every_week = types.InlineKeyboardButton('Каждую неделю', callback_data='every_week')
    markup.add(button_every_day)
    markup.add(button_every_week)
    return markup

def quotes_subscription_everyday_value_menu():
    markup = types.InlineKeyboardMarkup()
    button_10 = types.InlineKeyboardButton('10:00', callback_data='10')
    button_11 = types.InlineKeyboardButton('11:00', callback_data='11')
    button_12 = types.InlineKeyboardButton('12:00', callback_data='12')
    button_13 = types.InlineKeyboardButton('13:00', callback_data='13')
    button_other = types.InlineKeyboardButton('Укажу своё', callback_data='other')
    markup.add(button_10)
    markup.add(button_11)
    markup.add(button_12)
    markup.add(button_13)
    markup.add(button_other)
    return markup


def send_quotes_menu(bot, chat_id):
    heads = ['🐶', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🦁', '🐵', '🙈']
    head = random.choice(heads)
    bot.send_message(chat_id, 'Выбирай, что по душе {head}'.format(head=head), reply_markup=quotes_menu())

def send_great_quote(bot, chat_id):
    db = QuotesSQLiteDatabase(DB_PATH)
    while True:
        great_quotes = db.get_great_quotes()
        if great_quotes:
            break
        update_great_quotes()
    quote = random.choice(great_quotes)
    response = '{text}\n_{author}_'.format(text=quote[1], author=quote[2])
    bot.send_message(chat_id, response, parse_mode='Markdown', reply_markup=quotes_menu())

def send_quotes_subscription_menu(bot, chat_id):
    message_text = 'Супер!\nВыбирай раздел цитат, на который хотел бы подписаться!'
    bot.send_message(chat_id, message_text, reply_markup=quotes_subscription_name_menu())

def handle_quotes_subscription(bot, chat_id, subscription):
    db = QuotesSQLiteDatabase(DB_PATH)
    try:
        db.add_quotes_subscriber(chat_id, subscription['name'], subscription['type'], subscription['value'])
    except QuotesSubscriptionsLimitException as e:
        return bot.send_message(chat_id, str(e), reply_markup=quotes_menu())
    bot.send_message(chat_id, '🎉 Поздравляю! Подписка оформлена!', reply_markup=quotes_menu())
