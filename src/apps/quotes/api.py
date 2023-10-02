import telebot
import logging
import src.apps.quotes.menus as menus
from src.apps.core.types import LanguageCode
from src.apps.quotes.db import QUOTES_SUBSCRIPTION_TABLE, get_random_quote
from src.apps.quotes.shortcuts import get_subscription_builder
from src.static import MSG
from src.apps.quotes.constants import MAX_QUOTES_SUBSCRIPTIONS
from src.apps.quotes.types import Subscription


def send_quote(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    text = MSG[language.name]['quoting']
    quote = get_random_quote(language)
    if quote is None:
        return bot.send_message(chat_id, text['no_quotes'].r(), reply_markup=menus.build_quotes_menu(language))
    response = text['quote_template'].format(text=quote.text, author=quote.author or '—')
    return bot.send_message(chat_id, response, parse_mode='HTML', reply_markup=menus.build_quotes_menu(language))


def send_quotes_menu(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['quotes_menu'].r(), reply_markup=menus.build_quotes_menu(language))


def subscribe(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    if QUOTES_SUBSCRIPTION_TABLE.count(where={'chat_id': chat_id}) >= MAX_QUOTES_SUBSCRIPTIONS:
        return bot.send_message(chat_id, MSG[language.name]['subscribing']['max_subscriptions_reached'].r())
    return send_subscribing_interval_step(bot, chat_id, language)


def send_subscribing_interval_step(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.send_message(chat_id, MSG[language.name]['subscribing']['interval_step'].r(), reply_markup=menus.build_subscribing_interval_menu(language))


def handle_subscribing_interval_step(bot, chat_id: int, msg_id: int, data: str, language: LanguageCode):
    def fallback():
        cancel_subscribing(bot, chat_id, msg_id, language)
        bot.send_message(chat_id, MSG[language.name]['subscribing']['unexpected_error'].r(), reply_markup=menus.build_quotes_menu(language))

    logging.debug(f'Interval step callback data: {data}')
    interval = data.split('/')[-1]
    get_subscription_builder(chat_id).set_interval(interval, fallback=fallback)


def send_subscribing_base_weekday_step(bot, chat_id: int, msg_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.edit_message_text(MSG[language.name]['subscribing']['base_weekday_step'].r(), chat_id, msg_id, reply_markup=menus.build_subscribing_base_weekday_menu(language))


def handle_subscribing_base_weekday_step(bot, chat_id: int, msg_id: int, data: str, language: LanguageCode):
    def fallback():
        cancel_subscribing(bot, chat_id, msg_id, language)
        bot.send_message(chat_id, MSG[language.name]['subscribing']['unexpected_error'].r(), reply_markup=menus.build_quotes_menu(language))

    logging.debug(f'Base weekday step callback data: {data}')
    base_weekday = data.split('/')[-1]
    get_subscription_builder(chat_id).set_base_weekday(base_weekday, fallback=fallback)


def send_subscribing_timezone_step(bot, chat_id: int, msg_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.edit_message_text(MSG[language.name]['subscribing']['timezone_step'].r(), chat_id, msg_id, reply_markup=menus.build_subscribing_timezone_menu(language))


def handle_subscribing_timezone_step(bot, chat_id: int, msg_id: int, data: str, language: LanguageCode):
    def fallback():
        cancel_subscribing(bot, chat_id, msg_id, language)
        bot.send_message(chat_id, MSG[language.name]['subscribing']['unexpected_error'].r(), reply_markup=menus.build_quotes_menu(language))

    logging.debug(f'Timezone step callback data: {data}')
    timezone = data.split('/')[-1].replace('%', '/')
    get_subscription_builder(chat_id).set_timezone(timezone, fallback=fallback)


def send_subscribing_custom_timezone_step(bot, chat_id: int, msg_id: int, language: LanguageCode) -> telebot.types.Message:
    def handle_custom_timezone(message):
        def fallback():
            cancel_subscribing(bot, chat_id, msg_id, language)
            bot.send_message(chat_id, MSG[language.name]['subscribing']['bad_custom_timezone'].r(), parse_mode='HTML', reply_markup=menus.build_quotes_menu(language))

        logging.debug(f'Custom timezone step msg: {message.text}')
        timezone = message.text
        get_subscription_builder(chat_id).set_timezone(timezone, fallback=fallback)
        send_subscribing_base_time_step(bot, chat_id, msg_id, language)

    # NOTE: link to list with timezones
    msg = bot.edit_message_text(MSG[language.name]['subscribing']['custom_timezone_step'].r(), chat_id, msg_id, parse_mode='HTML',)
    bot.register_next_step_handler(msg, handle_custom_timezone)
    return msg


def send_subscribing_base_time_step(bot, chat_id: int, msg_id: int, language: LanguageCode) -> telebot.types.Message:
    return bot.edit_message_text(MSG[language.name]['subscribing']['base_time_step'].r(), chat_id, msg_id, reply_markup=menus.build_subscribing_base_time_menu(language))


def handle_subscribing_base_time_step(bot, chat_id: int, msg_id: int, data: str, language: LanguageCode):
    def fallback():
        cancel_subscribing(bot, chat_id, msg_id, language)
        bot.send_message(chat_id, MSG[language.name]['subscribing']['unexpected_error'].r(), reply_markup=menus.build_quotes_menu(language))

    logging.debug(f'Base time step callback data: {data}')
    base_time = data.split('/')[-1].replace('%', '/')
    get_subscription_builder(chat_id).set_base_time(base_time, fallback=fallback)


def send_subscribing_custom_base_time_step(bot, chat_id: int, msg_id: int, language: LanguageCode) -> telebot.types.Message:
    def handle_custom_base_time(message):
        def fallback():
            cancel_subscribing(bot, chat_id, msg_id, language)
            bot.send_message(chat_id, MSG[language.name]['subscribing']['bad_custom_base_time'].r(), reply_markup=menus.build_quotes_menu(language))

        logging.debug(f'Base time step msg: {message.text}')
        base_time = message.text
        get_subscription_builder(chat_id).set_base_time(base_time, fallback=fallback)
        create_subscription(bot, chat_id, msg_id, language)

    msg = bot.edit_message_text(MSG[language.name]['subscribing']['custom_base_time_step'].r(), chat_id, msg_id)
    bot.register_next_step_handler(msg, handle_custom_base_time)
    return msg


def create_subscription(bot, chat_id: int, msg_id: int, language: LanguageCode) -> telebot.types.Message:
    def fallback():
        cancel_subscribing(bot, chat_id, msg_id, language)
        bot.send_message(chat_id, MSG[language.name]['subscribing']['unexpected_error'].r(), reply_markup=menus.build_quotes_menu(language))

    subscription = get_subscription_builder(chat_id).create_subscription(chat_id, language, fallback=fallback)
    QUOTES_SUBSCRIPTION_TABLE.insert([subscription.to_database_row()])
    QUOTES_SUBSCRIPTION_TABLE.commit()
    bot.edit_message_text(MSG[language.name]['subscribing']['done_template'].r().format(subscription=subscription.overview(language)), chat_id, msg_id)
    return bot.send_message(chat_id, MSG[language.name]['subscribing']['congratulations'].r(), reply_markup=menus.build_quotes_menu(language))


def cancel_subscribing(bot, chat_id: int, msg_id: int, langauge: LanguageCode) -> telebot.types.Message:
    return bot.edit_message_text(MSG[langauge.name]['subscribing']['cancelled'].r(), chat_id, msg_id)


def send_manage_subscriptions_menu(bot, chat_id: int, language: LanguageCode) -> telebot.types.Message:
    text = MSG[language.name]['managing_subscriptions']
    subscription_rows = QUOTES_SUBSCRIPTION_TABLE.select(where={'chat_id': chat_id})
    if len(subscription_rows) == 0:
        return bot.send_message(chat_id, text['no_subscriptions'].r(), reply_markup=menus.build_quotes_menu(language))
    subscription_rows.sort(key=lambda row: row['id'])
    subscriptions = [Subscription.from_database_row(row) for row in subscription_rows]
    subscription_lines = '\n'.join(text['subscription_line_template'].r().format(num=ind+1, subscription=sub.overview(language)) for ind, sub in enumerate(subscriptions))
    return bot.send_message(chat_id, text['main_menu_template'].r().format(subscription_lines=subscription_lines), reply_markup=menus.build_manage_subscriptions_menu(language))


def send_remove_subscription_menu(bot, chat_id: int, msg_id: int, language: LanguageCode) -> telebot.types.Message:
    text = MSG[language.name]['managing_subscriptions']
    subscription_rows = QUOTES_SUBSCRIPTION_TABLE.select(where={'chat_id': chat_id})
    if len(subscription_rows) == 0:
        return bot.send_message(chat_id, text['no_subscriptions'].r(), reply_markup=menus.build_quotes_menu(language))
    subscription_rows.sort(key=lambda row: row['id'])
    subscriptions = [Subscription.from_database_row(row) for row in subscription_rows]
    subscription_lines = '\n'.join(text['subscription_line_template'].r().format(num=ind+1, subscription=sub.overview(language)) for ind, sub in enumerate(subscriptions))
    sub_ids = [row['id'] for row in subscription_rows]
    return bot.edit_message_text(text['remove_menu_template'].r().format(subscription_lines=subscription_lines), chat_id, msg_id, reply_markup=menus.build_remove_subscription_menu(sub_ids, language))


def remove_subscription(bot, chat_id: int, msg_id: int, data: str, language: LanguageCode):
    logging.debug(f'Remove subscription callback data: {data}')
    text = MSG[language.name]['managing_subscriptions']
    subscription_id = int(data.split('/')[-1])
    subscription_rows = QUOTES_SUBSCRIPTION_TABLE.select(where={'id': subscription_id})
    if len(subscription_rows) == 0:
        bot.edit_message_text(text['subscription_not_found'].r(), chat_id, msg_id)
        return send_quotes_menu(bot, chat_id, language)
    QUOTES_SUBSCRIPTION_TABLE.delete(where={'id': subscription_id})
    QUOTES_SUBSCRIPTION_TABLE.commit()
    subscription = Subscription.from_database_row(subscription_rows[0])
    return bot.edit_message_text(text['removing_done_template'].r().format(subscription=subscription.overview(language)), chat_id, msg_id)


def return_to_manage_subscriptions_menu(bot, chat_id: int, msg_id: int, language: LanguageCode) -> telebot.types.Message:
    text = MSG[language.name]['managing_subscriptions']
    subscription_rows = QUOTES_SUBSCRIPTION_TABLE.select(where={'chat_id': chat_id})
    if len(subscription_rows) == 0:
        bot.delete_message(chat_id, msg_id)
        return bot.send_message(chat_id, text['no_subscriptions'].r(), reply_markup=menus.build_quotes_menu(language))
    subscription_rows.sort(key=lambda row: row['id'])
    subscriptions = [Subscription.from_database_row(row) for row in subscription_rows]
    subscription_lines = '\n'.join(text['subscription_line_template'].r().format(num=ind+1, subscription=sub.overview(language)) for ind, sub in enumerate(subscriptions))
    return bot.edit_message_text(text['main_menu_template'].r().format(subscription_lines=subscription_lines), chat_id, msg_id, reply_markup=menus.build_manage_subscriptions_menu(language))
