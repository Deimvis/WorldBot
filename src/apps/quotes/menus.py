from telebot import types
from typing import Sequence
from src.apps.core.types import LanguageCode
from src.static import MENU


def build_quotes_menu(language: LanguageCode):
    text = MENU[language.name]['quotes_menu']
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton(text['get_quote']))
    markup.add(types.KeyboardButton(text['subscribe']))
    markup.add(types.KeyboardButton(text['manage_subscriptions']))
    return markup


def build_subscribing_interval_menu(language: LanguageCode):
    callback_prefix = 'subscribing/interval_menu/'
    text = MENU[language.name]['subscribing']['interval_menu']
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text['every_day'],   callback_data=callback_prefix + 'EVERY_DAY'),
        types.InlineKeyboardButton(text['every_week'],  callback_data=callback_prefix + 'EVERY_WEEK'),
        types.InlineKeyboardButton(text['return_back'], callback_data=callback_prefix + 'RETURN'),
        row_width=2,
    )
    return markup


def build_subscribing_base_weekday_step(language: LanguageCode):
    callback_prefix = 'subscribing/base_weekday_menu/'
    text = MENU[language.name]['subscribing']['base_weekday_menu']
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text['monday'],      callback_data=callback_prefix + 'MONDAY'),
        types.InlineKeyboardButton(text['tuesday'],     callback_data=callback_prefix + 'TUESDAY'),
        types.InlineKeyboardButton(text['wednesday'],   callback_data=callback_prefix + 'WEDNESDAY'),
        types.InlineKeyboardButton(text['thursday'],    callback_data=callback_prefix + 'THURSDAY'),
        types.InlineKeyboardButton(text['friday'],      callback_data=callback_prefix + 'FRIDAY'),
        types.InlineKeyboardButton(text['saturday'],    callback_data=callback_prefix + 'SATURDAY'),
        types.InlineKeyboardButton(text['sunday'],      callback_data=callback_prefix + 'SUNDAY'),
        types.InlineKeyboardButton(text['return_back'], callback_data=callback_prefix + 'RETURN'),
    )
    return markup


def build_subscribing_timezone_menu(language: LanguageCode):
    callback_prefix = 'subscribing/timezone_menu/'
    text = MENU[language.name]['subscribing']['timezone_menu']
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text['timezone_1'],      callback_data=callback_prefix + text['timezone_1'].replace('/', '%')),
        types.InlineKeyboardButton(text['timezone_2'],      callback_data=callback_prefix + text['timezone_2'].replace('/', '%')),
        types.InlineKeyboardButton(text['timezone_3'],      callback_data=callback_prefix + text['timezone_3'].replace('/', '%')),
        types.InlineKeyboardButton(text['timezone_4'],      callback_data=callback_prefix + text['timezone_4'].replace('/', '%')),
        types.InlineKeyboardButton(text['timezone_5'],      callback_data=callback_prefix + text['timezone_5'].replace('/', '%')),
        types.InlineKeyboardButton(text['custom_timezone'], callback_data=callback_prefix + 'CUSTOM'),
        types.InlineKeyboardButton(text['return_back'],     callback_data=callback_prefix + 'RETURN'),
        row_width=2,
    )
    return markup


def build_subscribing_base_time_menu(language: LanguageCode):
    callback_prefix = 'subscribing/base_time_menu/'
    text = MENU[language.name]['subscribing']['base_time_menu']
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text['base_time_1'],      callback_data=callback_prefix + text['base_time_1'].replace('/', '%')),
        types.InlineKeyboardButton(text['base_time_2'],      callback_data=callback_prefix + text['base_time_2'].replace('/', '%')),
        types.InlineKeyboardButton(text['base_time_3'],      callback_data=callback_prefix + text['base_time_3'].replace('/', '%')),
        types.InlineKeyboardButton(text['base_time_4'],      callback_data=callback_prefix + text['base_time_4'].replace('/', '%')),
        types.InlineKeyboardButton(text['base_time_5'],      callback_data=callback_prefix + text['base_time_5'].replace('/', '%')),
        types.InlineKeyboardButton(text['custom_base_time'], callback_data=callback_prefix + 'CUSTOM'),
        types.InlineKeyboardButton(text['return_back'],     callback_data=callback_prefix + 'RETURN'),
        row_width=2,
    )
    return markup


def build_manage_subscriptions_menu(language: LanguageCode):
    callback_prefix = 'managing_subscriptions/main_menu/'
    text = MENU[language.name]['managing_subscriptions']['main_menu']
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text['remove'],      callback_data=callback_prefix + 'REMOVE'),
        types.InlineKeyboardButton(text['return_back'], callback_data=callback_prefix + 'RETURN'),
        row_width=1,
    )
    return markup


def build_remove_subscription_menu(sub_ids: Sequence[int], language: LanguageCode):
    callback_prefix = 'managing_subscriptions/remove_menu/'
    text = MENU[language.name]['managing_subscriptions']['remove_menu']
    markup = types.InlineKeyboardMarkup()
    markup.add(
        *(types.InlineKeyboardButton(text['button_template'].format(num=ind+1), callback_data=callback_prefix + str(sub_id))
          for ind, sub_id in enumerate(sub_ids)),
        row_width=2,
    )
    markup.add(types.InlineKeyboardButton(text['return_back'], callback_data=callback_prefix + 'RETURN'))
    return markup
