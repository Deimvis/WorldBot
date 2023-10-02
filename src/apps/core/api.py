import telebot
import time
import src.apps.core.menus as menus
from src.apps.core.shortcuts import get_language, flood_trigger
from src.apps.core.types import LanguageCode
from src.static import MSG


def send_start_menu(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['start'].resolve(), reply_markup=menus.build_main_menu(language))


def send_bad_interaction_reaction(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['bad_message_reaction'].r(), reply_markup=menus.build_main_menu(language))


def send_last_updates(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['last_updates'].r(), parse_mode='HTML')


def send_about(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['about'].r(), parse_mode='HTML')


def send_easter_egg(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, "🥚")


def send_bad_message_reaction(bot, message: telebot.types.Message) -> telebot.types.Message:
    if flood_trigger(message.chat.id):
        return send_bad_message_flooding_reaction(bot, message)
    language = get_language(message)
    return bot.reply_to(message, MSG[language.name]['bad_message_reaction'].r(), reply_markup=menus.build_main_menu(language))


def send_bad_message_flooding_reaction(bot: telebot.TeleBot, message: telebot.types.Message) -> telebot.types.Message:
    msg = bot.reply_to(message, 'AAA')
    cnt = 3
    for timeout in [0.7, 0.3, 0.2, 0.1, 0.05, 0.05, 0.01]:
        time.sleep(timeout)
        cnt += 1
        bot.edit_message_text('A' * cnt, message.chat.id, msg.id)
    while cnt < 4096:
        time.sleep(0.01)
        cnt = min(cnt * 2, 4096)
        bot.edit_message_text('A' * cnt, message.chat.id, msg.id)
    time.sleep(0.1)
    send_start_menu(bot, message.chat.id, get_language(message))
