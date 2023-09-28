import telebot
import src.apps.core.menus as menus
from src.apps.core.shortcuts import get_language
from src.apps.core.types import LanguageCode
from src.static import MSG


def send_start_menu(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['start'].resolve(), reply_markup=menus.build_main_menu(language))


def send_bad_message_reaction(bot, message: telebot.types.Message) -> telebot.types.Message:
    language = get_language(message)
    return bot.reply_to(message, MSG[language.name]['bad_message_reaction'].r(), reply_markup=menus.build_main_menu(language))


def send_bad_interaction_reaction(bot, chat_id: int, language: LanguageCode)  -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['bad_message_reaction'].r(), reply_markup=menus.build_main_menu(language))


def send_last_updates(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['last_updates'].r(), parse_mode='HTML')


def send_about(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['about'].r(), parse_mode='HTML')
