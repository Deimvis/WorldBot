import re
import threading
import telebot
from telebot import types
from config import BOT_TOKEN, DB_PATH
from apps.quotes.api import (
    send_quotes_menu,
    send_great_quote,
    send_quotes_subscription_menu,
    send_quotes_subscription_manage_menu,
    handle_quotes_subscription,
    handle_remove_quote_subscription,
    handle_remove_quote_subscription_do,
    quotes_subscription_type_menu,
    quotes_subscription_everyday_value_menu
)
from apps.quotes.utils import (
    DayOfWeekRUEN,
    get_build_quotes_subscription_status,
    get_remove_quotes_subscription_status
)
from apps.quotes.scheduler import QuotesSubscription
from apps.quotes.sqlite import QuotesSQLiteDatabase


bot = telebot.TeleBot(BOT_TOKEN)
build_quotes_subscription = dict()
remove_quotes_subscription_stage = dict()


def main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_quotes = types.KeyboardButton('💫 Хочу стать мудрее!')
    markup.add(button_quotes)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    update_user_info(message)
    bot.send_message(message.chat.id,
                     'Привет! 🖐\nС наступающим Новым Годом! ❄️️\nЧто на этот раз?', reply_markup=main_menu())


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '💫 Хочу стать мудрее!':
        send_quotes_menu(bot, message.chat.id)
    elif message.text == '🔥 Великая цитата':
        send_great_quote(bot, message.chat.id)
    elif message.text == '✉️ Хочу регулярно получать цитаты':
        build_quotes_subscription[message.chat.id] = dict()
        send_quotes_subscription_menu(bot, message.chat.id)
    elif message.text == '⚙️ Управление подписками':
        send_quotes_subscription_manage_menu(bot, message.chat.id)
    elif (re.fullmatch(r'\d{1,2}', message.text) and
            get_build_quotes_subscription_status(message.chat.id, build_quotes_subscription) == 'need value'):
        build_quotes_subscription[message.chat.id]['value'] = message.text
        subscription = build_quotes_subscription[message.chat.id]
        del build_quotes_subscription[message.chat.id]
        handle_quotes_subscription(bot, message.chat.id, subscription)
    elif (re.fullmatch(r'\w+-\d{1,2}', message.text) and
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


def handle_bad_interaction(chat_id):
    build_quotes_subscription.pop(chat_id, None)
    remove_quotes_subscription_stage.pop(chat_id, None)
    return bot.send_message(chat_id, 'Не кликай просто так! Ты меня ломаешь 😣', reply_markup=main_menu())


def update_user_info(message):
    db = QuotesSQLiteDatabase(DB_PATH)
    db.update_user(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)


@bot.callback_query_handler(func=lambda call: call.data in ['quotes_menu'])
def return_quotes_subscription_menu(call):
    build_quotes_subscription.pop(call.message.chat.id, None)
    remove_quotes_subscription_stage.pop(call.message.chat.id, None)
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    send_quotes_menu(bot, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data in ['great_quotes'])
def quotes_subscription_name(call):
    if get_build_quotes_subscription_status(call.message.chat.id, build_quotes_subscription) != 'need name':
        return handle_bad_interaction(call.message.chat.id)
    build_quotes_subscription[call.message.chat.id]['name'] = call.data
    message_text = 'Отлично!\nТеперь выбери, как часто ты хочешь получать цитату'
    bot.edit_message_text(message_text, call.message.chat.id,
                          call.message.message_id, reply_markup=quotes_subscription_type_menu())


@bot.callback_query_handler(func=lambda call: call.data in ['every_day', 'every_week'])
def quotes_subscription_type(call):
    if get_build_quotes_subscription_status(call.message.chat.id, build_quotes_subscription) != 'need type':
        return handle_bad_interaction(call.message.chat.id)
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


@bot.callback_query_handler(func=lambda call: call.data in ['10', '11', '12', '13', '14', '15', 'other'])
def quotes_subscription_value(call):
    if get_build_quotes_subscription_status(call.message.chat.id, build_quotes_subscription) != 'need value':
        return handle_bad_interaction(call.message.chat.id)
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


@bot.callback_query_handler(func=lambda call: call.data in ['remove_quotes_subscription'])
def remove_quotes_subscription(call):
    return handle_remove_quote_subscription(bot, call.message.chat.id,
                                            call.message.message_id, remove_quotes_subscription_stage)


@bot.callback_query_handler(func=lambda call: call.data in ['remove_subscription_1',
                                                            'remove_subscription_2',
                                                            'remove_subscription_3',
                                                            'remove_subscription_4',
                                                            'remove_subscription_5'])
def remove_quotes_subscription_do(call):
    if get_remove_quotes_subscription_status(call.message.chat.id, remove_quotes_subscription_stage) == 'EMPTY':
        return handle_bad_interaction(call.message.chat.id)
    subs = remove_quotes_subscription_stage[call.message.chat.id]
    selected_sub = subs[int(call.data[-1]) - 1]
    remove_quotes_subscription_stage.pop(call.message.chat.id, None)
    return handle_remove_quote_subscription_do(bot, call.message.chat.id, selected_sub)


if __name__ == '__main__':
    quotes_subscription = QuotesSubscription(bot)

    quotes_subscription_thread = threading.Thread(target=quotes_subscription.run)
    quotes_subscription_thread.start()

    bot.polling(non_stop=True)
