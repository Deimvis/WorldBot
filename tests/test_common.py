import multiprocessing
import os
import pytest
import telebot
import main as entry_point


def simple_start():
    bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
    bot.polling()


def test_simple_start():
    try:
        p = multiprocessing.Process(target=simple_start)
        p.start()
        p.join(2)
        assert p.is_alive()
        p.terminate()
        p.join()
    except Exception as error:
        pytest.fail(f'Bot didn\'t start:\n{error}')


def test_real_start():
    try:
        p = multiprocessing.Process(target=entry_point.main)
        p.start()
        p.join(2)
        assert p.is_alive()
        p.terminate()
        p.join()
    except Exception as error:
        pytest.fail(f'Entry point failed:\n{error}')
