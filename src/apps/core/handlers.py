import src.apps.core.api as api
from src.apps.core.db import update_user_info
from src.apps.core.shortcuts import get_language


def on_start_cmd(bot, message):
    update_user_info(message.from_user)
    api.send_start_menu(bot, message.chat.id, get_language(message))


def on_last_updates_cmd(bot, message):
    api.send_last_updates(bot, message.chat.id, get_language(message))


def on_about_cmd(bot, message):
    api.send_about(bot, message.chat.id, get_language(message))


def on_easter_egg_cmd(bot, message):
    api.send_easter_egg(bot, message.chat.id, get_language(message))


def on_unhandeled_msg(bot, message):
    api.send_bad_message_reaction(bot, message)
