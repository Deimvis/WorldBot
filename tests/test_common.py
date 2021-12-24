import os
import pytest
import telebot


def test_simple_start():
    try:
        bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
    except Exception as e:
        pytest.fail('Bot did not start:\n{}'.format(e))
