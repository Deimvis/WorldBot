import multiprocessing
import os
import pytest
import telebot

from apps.quotes.api import send_quotes_menu
from apps.quotes.utils import get_great_quotes_list


def simple_start():
    bot = telebot.TeleBot(os.getenv('TEST_BOT_TOKEN'))
    bot.polling()

def test_simple_start():
    try:
        p = multiprocessing.Process(target=simple_start)
        p.start()
        p.join(10)
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
    bot = telebot.TeleBot(os.getenv('TEST_BOT_TOKEN'))
    chat_id = os.getenv('TEST_CHAT_ID')
    send_quotes_menu(bot, chat_id)

