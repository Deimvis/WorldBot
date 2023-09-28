import src.apps.core.api as api
import src.apps.core.menus as menus
import src.apps.quotes.api as quotes_api
import src.apps.quotes.menus as quotes_menus
from lib.utils.functools import apply
from src.apps.core.db import update_user_info
from src.apps.core.types import LanguageCode
from src.apps.core.shortcuts import get_language
from src.static import MSG


def on_start_cmd(bot, message):
    update_user_info(message.from_user)
    api.send_start_menu(bot, message.chat.id, get_language(message))


def on_unhandeled_msg(bot, message):
    api.send_bad_message_reaction(bot, message)


def on_last_updates_cmd(bot, message):
    api.send_last_updates(bot, message.chat.id, get_language(message))


def on_about_cmd(bot, message):
    api.send_about(bot, message.chat.id, get_language(message))
