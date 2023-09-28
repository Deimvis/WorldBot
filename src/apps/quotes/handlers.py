import src.apps.quotes.api as api
from src.apps.core.shortcuts import get_language


def on_quotes_menu_cmd(bot, message):
    api.send_quotes_menu(bot, message.chat.id, get_language(message))


def on_quotes_menu_msg(bot, message):
    api.send_quotes_menu(bot, message.chat.id, get_language(message))


def on_quotes_menu_call(bot, callback):
    api.send_quotes_menu(bot, callback.message.chat.id, get_language(callback))


def on_get_quote_cmd(bot, message):
    api.send_quote(bot, message.chat.id, get_language(message))


def on_get_quote_msg(bot, message):
    api.send_quote(bot, message.chat.id, get_language(message))


def on_subscribe_cmd(bot, message):
    api.subscribe(bot, message.chat.id, get_language(message))


def on_subscribe_msg(bot, message):
    api.subscribe(bot, message.chat.id, get_language(message))


def on_subscribing_interval_call(bot, callback):
    api.handle_subscribing_interval_step(bot, callback.message.chat.id, callback.message.message_id, callback.data, get_language(callback))
    if callback.data.endswith('EVERY_WEEK'):
        api.send_subscribing_base_weekday_step(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))
        return
    if callback.data.endswith('EVERY_DAY'):
        api.send_subscribing_timezone_step(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))
        return
    raise RuntimeError(f'Got unsupported subscribing interval call: {callback.data}')


def on_subscribing_base_weekday_call(bot, callback):
    api.handle_subscribing_base_weekday_step(bot, callback.message.chat.id, callback.message.message_id, callback.data, get_language(callback))
    api.send_subscribing_timezone_step(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))


def on_subscribing_timezone_call(bot, callback):
    if callback.data.endswith('CUSTOM'):
        api.send_subscribing_custom_timezone_step(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))
    else:
        api.handle_subscribing_timezone_step(bot, callback.message.chat.id, callback.message.message_id, callback.data, get_language(callback))
        api.send_subscribing_base_time_step(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))


def on_subscribing_base_time_call(bot, callback):
    if callback.data.endswith('CUSTOM'):
        api.send_subscribing_custom_base_time_step(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))
    else:
        api.handle_subscribing_base_time_step(bot, callback.message.chat.id, callback.message.message_id, callback.data, get_language(callback))
        api.create_subscription(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))


def on_subscribing_return_call(bot, callback):
    api.cancel_subscribing(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))
    api.send_quotes_menu(bot, callback.message.chat.id, get_language(callback))


def on_manage_subscriptions_cmd(bot, message):
    api.send_manage_subscriptions_menu(bot, message.chat.id, get_language(message))


def on_manage_subscriptions_msg(bot, message):
    api.send_manage_subscriptions_menu(bot, message.chat.id, get_language(message))


def on_manage_subscriptions_call(bot, callback):
    api.send_manage_subscriptions_menu(bot, callback.message.chat.id, get_language(callback))


def on_manage_subscriptions_return_call(bot, callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    api.send_quotes_menu(bot, callback.message.chat.id, get_language(callback))


def on_remove_subscription_menu_call(bot, callback):
    api.send_remove_subscription_menu(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))


def on_remove_subscription_call(bot, callback):
    api.remove_subscription(bot, callback.message.chat.id, callback.message.message_id, callback.data, get_language(callback))
    api.send_manage_subscriptions_menu(bot, callback.message.chat.id, get_language(callback))


def on_remove_subscription_return_call(bot, callback):
    api.return_to_manage_subscriptions_menu(bot, callback.message.chat.id, callback.message.message_id, get_language(callback))
