import multiprocessing
import os
import pytest
import telebot

from apps.quotes.api import (
    send_quotes_menu,
    send_quotes_subscription_menu,
    send_quotes_subscription_manage_menu,
    send_great_quote,
)
from apps.quotes.utils import get_great_quotes_list

BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')


def simple_start():
    bot = telebot.TeleBot(BOT_TOKEN)
    bot.polling()


def test_simple_start():
    try:
        p = multiprocessing.Process(target=simple_start)
        p.start()
        p.join(5)
        assert p.is_alive()
        p.terminate()
        p.join()
    except Exception as e:
        pytest.fail('Bot did not start:\n{}'.format(e))


def test_parsing_quotes():
    try:
        quotes = get_great_quotes_list()
        assert len(quotes) == 100
    except Exception as e:
        pytest.fail('Parsing quotes failed:\n{}'.format(e))


def test_quotes_menu_is_working():
    try:
        bot = telebot.TeleBot(BOT_TOKEN)
        chat_id = os.getenv('TEST_CHAT_ID')
        send_quotes_menu(bot, chat_id)
    except Exception as e:
        pytest.fail('Sending quotes menu failed:\n{}'.format(e))


def test_send_great_quote_is_working():
    try:
        bot = telebot.TeleBot(BOT_TOKEN)
        chat_id = os.getenv('TEST_CHAT_ID')
        send_great_quote(bot, chat_id)
    except Exception as e:
        pytest.fail('Sending quotes menu failed:\n{}'.format(e))


def test_send_quotes_subscription_menu_is_working():
    try:
        bot = telebot.TeleBot(BOT_TOKEN)
        chat_id = os.getenv('TEST_CHAT_ID')
        send_quotes_subscription_menu(bot, chat_id)
    except Exception as e:
        pytest.fail('Sending quotes menu failed:\n{}'.format(e))


def test_send_quotes_subscription_manage_menu_is_working():
    try:
        bot = telebot.TeleBot(BOT_TOKEN)
        chat_id = os.getenv('TEST_CHAT_ID')
        send_quotes_subscription_manage_menu(bot, chat_id)
    except Exception as e:
        pytest.fail('Sending quotes menu failed:\n{}'.format(e))
