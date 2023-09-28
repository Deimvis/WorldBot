import src.apps.core.handlers as handlers
from lib.utils.functools import apply


def register_handlers(bot):
    bot.message_handler(commands=['start'])\
        (apply(bot)(handlers.on_start_cmd))
    bot.message_handler(commands=['last_updates'])\
        (apply(bot)(handlers.on_last_updates_cmd))
    bot.message_handler(commands=['about'])\
        (apply(bot)(handlers.on_about_cmd))
    bot.message_handler(content_types=['text'])\
        (apply(bot)(handlers.on_unhandeled_msg))
