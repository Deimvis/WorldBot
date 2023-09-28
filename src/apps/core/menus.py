from telebot import types
from src.apps.core.types import LanguageCode
from src.static import MENU


def build_main_menu(language: LanguageCode):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_quotes = types.KeyboardButton(MENU[language.name]['main_menu']['quotes_menu'])
    markup.add(button_quotes)
    return markup


# main_menu = build_main_menu()
