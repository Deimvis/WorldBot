import src.apps.quotes.state  # noqa
import src.apps.quotes.handlers as handlers
from lib.utils.functools import apply
from src.static import MENU


def register_handlers(bot):
    bot.message_handler(commands=['quotes_menu'])\
        (apply(bot)(handlers.on_quotes_menu_cmd))
    bot.message_handler(regexp='|'.join(translated_menu['main_menu']['quotes_menu'] for translated_menu in MENU.values()))\
        (apply(bot)(handlers.on_quotes_menu_msg))
    bot.callback_query_handler(func=lambda call: call.data == 'quotes_menu')\
        (apply(bot)(handlers.on_quotes_menu_call))

    bot.message_handler(commands=['quote'])\
        (apply(bot)(handlers.on_get_quote_cmd))
    bot.message_handler(regexp='|'.join(translated_menu['quotes_menu']['get_quote']  for translated_menu in MENU.values()))\
        (apply(bot)(handlers.on_get_quote_msg))

    bot.message_handler(commands=['subscribe'])\
        (apply(bot)(handlers.on_subscribe_cmd))
    bot.message_handler(regexp='|'.join(translated_menu['quotes_menu']['subscribe'] for translated_menu in MENU.values()))\
        (apply(bot)(handlers.on_subscribe_msg))
    bot.callback_query_handler(func=lambda call: call.data.startswith('subscribing') and call.data.endswith('RETURN'))\
        (apply(bot)(handlers.on_subscribing_return_call))
    bot.callback_query_handler(func=lambda call: call.data.startswith('subscribing/interval_menu'))\
        (apply(bot)(handlers.on_subscribing_interval_call))
    bot.callback_query_handler(func=lambda call: call.data.startswith('subscribing/base_weekday_menu'))\
        (apply(bot)(handlers.on_subscribing_base_weekday_call))
    bot.callback_query_handler(func=lambda call: call.data.startswith('subscribing/timezone_menu'))\
        (apply(bot)(handlers.on_subscribing_timezone_call))
    bot.callback_query_handler(func=lambda call: call.data.startswith('subscribing/base_time_menu'))\
        (apply(bot)(handlers.on_subscribing_base_time_call))

    bot.message_handler(commands=['manage_subscriptions'])\
        (apply(bot))(handlers.on_manage_subscriptions_cmd)
    bot.message_handler(regexp='|'.join(translated_menu['quotes_menu']['manage_subscriptions'] for translated_menu in MENU.values()))\
        (apply(bot)(handlers.on_manage_subscriptions_msg))
    bot.callback_query_handler(func=lambda call: call.data == 'managing_subscriptions/main_menu')\
        (apply(bot)(handlers.on_manage_subscriptions_call))
    bot.callback_query_handler(func=lambda call: call.data == 'managing_subscriptions/main_menu/REMOVE')\
        (apply(bot)(handlers.on_remove_subscription_menu_call))
    bot.callback_query_handler(func=lambda call: call.data.startswith('managing_subscriptions/remove_menu/'))\
        (apply(bot)(handlers.on_remove_subscription_call))
