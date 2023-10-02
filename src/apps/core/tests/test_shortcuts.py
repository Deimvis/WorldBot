import unittest
from unittest.mock import patch
from src.apps.core.shortcuts import get_language, flood_trigger
from src.apps.core.state import GLOBAL_STATE
from src.apps.core.types import LanguageCode
from src.utils.testing import TelegramMockFactory


class TestGetLanguage(unittest.TestCase):
    def test_smoke(self):
        mf = TelegramMockFactory
        _ = get_language(mf.Message(from_user=mf.User(language_code='en')))

    def test_simple(self):
        mf = TelegramMockFactory
        self.assertEqual(get_language(mf.Message(from_user=mf.User(language_code='en'))), LanguageCode.ENG)
        self.assertEqual(get_language(mf.Message(from_user=mf.User(language_code='ru'))), LanguageCode.RUS)
        self.assertEqual(get_language(mf.CallbackQuery(from_user=mf.User(language_code='en'))), LanguageCode.ENG)
        self.assertEqual(get_language(mf.CallbackQuery(from_user=mf.User(language_code='ru'))), LanguageCode.RUS)

    def test_invalid_argument(self):
        with self.assertRaises(RuntimeError):
            get_language('123')
        with self.assertRaises(RuntimeError):
            get_language('en')
        with self.assertRaises(RuntimeError):
            get_language('eng')


class TestFloodTrigger(unittest.TestCase):

    def setUp(self):
        GLOBAL_STATE.pop('bad_message', None)

    def test_smoke(self):
        _ = flood_trigger(1)

    def test_simple(self):
        for _ in range(9):
            self.assertEqual(flood_trigger(1), False)
        self.assertEqual(flood_trigger(1), True)

    @patch('time.time')
    def test_timeout(self, mock_time):
        mock_time.return_value = 0.0
        for _ in range(9):
            self.assertEqual(flood_trigger(1), False)
        mock_time.return_value = 10.0
        self.assertEqual(flood_trigger(1), False)

    def test_different_chats(self):
        for _ in range(5):
            self.assertEqual(flood_trigger(1), False)
            self.assertEqual(flood_trigger(2), False)
