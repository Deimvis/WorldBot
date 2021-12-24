import datetime, random, re, requests, sys, threading
import telebot
from telebot import types
from config import BOT_TOKEN
from apps.quotes.api import (
    send_quotes_menu,
    send_great_quote,
    send_quotes_subscription_menu,
    handle_quotes_subscription,
    quotes_subscription_type_menu,
    quotes_subscription_everyday_value_menu
)
from apps.quotes.scheduler import QuotesSubscription
from apps.quotes.utils import DayOfWeekRUEN, get_build_quotes_subscription_status


bot = telebot.TeleBot(BOT_TOKEN)
build_quotes_subscription = dict()

def main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_quotes = types.KeyboardButton('💫 Хочу стать мудрее!')
    markup.add(button_quotes)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! 🖐\nЧто на этот раз?', reply_markup=main_menu())

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '💫 Хочу стать мудрее!':
        send_quotes_menu(bot, message.chat.id)
    elif message.text == '🔥 Великая цитата':
        send_great_quote(bot, message.chat.id)
    elif message.text == '✉️ Хочу регулярно получать цитаты':
        build_quotes_subscription[message.chat.id] = dict()
        send_quotes_subscription_menu(bot, message.chat.id)
    elif (re.fullmatch(r'\d\d', message.text) and
            get_build_quotes_subscription_status(message.chat.id, build_quotes_subscription) == 'need value'):
        build_quotes_subscription[message.chat.id]['value'] = message.text
        subscription = build_quotes_subscription[message.chat.id]
        del build_quotes_subscription[message.chat.id]
        handle_quotes_subscription(bot, message.chat.id, subscription)
    elif (re.fullmatch(r'\w+-\d\d', message.text) and
            get_build_quotes_subscription_status(message.chat.id, build_quotes_subscription) == 'need value'):
        day_of_week_ru, hour = message.text.split('-')
        if day_of_week_ru.lower() not in DayOfWeekRUEN:
            return bot.send_message(message.chat.id, 'День недели указан неверно, попробуй еще раз!')
        day_of_week = DayOfWeekRUEN[day_of_week_ru.lower()]
        value = day_of_week + '-' + hour
        build_quotes_subscription[message.chat.id]['value'] = value
        subscription = build_quotes_subscription[message.chat.id]
        del build_quotes_subscription[message.chat.id]
        handle_quotes_subscription(bot, message.chat.id, subscription)
    elif message.text == 'debug':
        pass
    else:
        bot.reply_to(message, 'Я тебя не понимаю 😔', reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data in ['great_quotes'])
def quotes_subscription_name(call):
    if get_build_quotes_subscription_status(call.message.chat.id, build_quotes_subscription) != 'need name':
        return bot.send_message(call.message.chat.id, 'Не кликай просто так! Ты меня ломаешь 😣')
    build_quotes_subscription[call.message.chat.id]['name'] = call.data
    message_text = 'Отлично!\nТеперь выбери, как часто ты хочешь получать цитату'
    bot.edit_message_text(message_text, call.message.chat.id,
                          call.message.message_id, reply_markup=quotes_subscription_type_menu())

@bot.callback_query_handler(func=lambda call: call.data in ['every_day', 'every_week'])
def quotes_subscription_type(call):
    if get_build_quotes_subscription_status(call.message.chat.id, build_quotes_subscription) != 'need type':
        return bot.send_message(call.message.chat.id, 'Не кликай просто так! Ты меня ломаешь 😣')
    build_quotes_subscription[call.message.chat.id]['type'] = call.data
    if call.data == 'every_day':
        message_text = 'Великолепно!\nДело за малым! ' \
                       'Выбери время (МСК), в которое тебе будет приходить новая цитата, или укажи своё'
        bot.edit_message_text(message_text, call.message.chat.id,
                              call.message.message_id, reply_markup=quotes_subscription_everyday_value_menu())
    elif call.data == 'every_week':
        message_text = 'Великолепно!\nДело за малым! ' \
                       'Напиши мне дату и время (МСК),' \
                       ' в которое тебе будет приходить новая цитата, в следующем формате:\n' \
                       '<День недели>-<номер часа в 24-часовом формате времени>\n' \
                       'Например, Понедельник-10 или Вторник-18'
        bot.send_message(call.message.chat.id, message_text)

@bot.callback_query_handler(func=lambda call: call.data in ['10', '11', '12', '13', 'other'])
def quotes_subscription_value(call):
    if get_build_quotes_subscription_status(call.message.chat.id, build_quotes_subscription) != 'need value':
        return bot.send_message(call.message.chat.id, 'Не кликай просто так! Ты меня ломаешь 😣')
    if call.data == 'other':
        message_text = 'Хорошо!\n' \
                       'Напиши мне время (МСК),' \
                       ' в которое тебе будет приходить новая цитата, в следующем формате:\n' \
                       '<номер часа в 24-часовом формате времени>\n' \
                       'Например, 10 или 18'
        return bot.send_message(call.message.chat.id, message_text)
    build_quotes_subscription[call.message.chat.id]['value'] = call.data
    subscription = build_quotes_subscription[call.message.chat.id]
    del build_quotes_subscription[call.message.chat.id]
    handle_quotes_subscription(bot, call.message.chat.id, subscription)


if __name__ == '__main__':
    quotes_subscription = QuotesSubscription(bot)

    quotes_subscription_thread = threading.Thread(target=quotes_subscription.run)
    quotes_subscription_thread.start()

    bot.polling(non_stop=True)
