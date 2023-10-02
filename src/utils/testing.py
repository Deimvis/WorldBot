import os
import telebot
import unittest
from unittest.mock import create_autospec, patch


class TelegramMockFactory:
    @staticmethod
    def User(id: int = None, username: str = None, first_name: str = None, last_name: str = None, language_code: str = None):
        user = create_autospec(telebot.types.User)
        user.id = id
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.language_code = language_code
        return user

    @staticmethod
    def Chat(chat_id: int = None):
        chat = create_autospec(telebot.types.Chat)
        chat.id = chat_id
        return chat

    @staticmethod
    def Message(chat=None, from_user=None):
        msg = create_autospec(telebot.types.Message)
        msg.chat = chat
        msg.from_user = from_user
        return msg

    @staticmethod
    def CallbackQuery(from_user=None):
        callback = create_autospec(telebot.types.CallbackQuery)
        callback.from_user = from_user
        return callback


class MockTeleBotTestCase(unittest.TestCase):

    def setUp(self):
        self.bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
        super().setUp()

    @classmethod
    def setUpClass(cls):
        cls.patchers = [
            patch('telebot.TeleBot.send_message', autospec=True),
            patch('telebot.TeleBot.edit_message_text', autospec=True),
            patch('telebot.TeleBot.reply_to', autospec=True),
        ]
        for p in cls.patchers:
            p.start()
        super(MockTeleBotTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        for p in cls.patchers:
            p.stop()
        super(MockTeleBotTestCase, cls).tearDownClass()
