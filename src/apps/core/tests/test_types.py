import unittest
from src.apps.core.types import LanguageCode


class TestLanguageCode(unittest.TestCase):

    def test_smoke(self):
        _ = LanguageCode['ENG']
        _ = LanguageCode.ENG
        _ = LanguageCode['RUS']
        _ = LanguageCode.RUS

    def test_invalid_language(self):
        with self.assertRaises(KeyError):
            LanguageCode['ABC']
        with self.assertRaises(KeyError):
            LanguageCode['eng']
        with self.assertRaises(KeyError):
            LanguageCode['rus']

    def test_from_IETF(self):
        self.assertEqual(LanguageCode.from_IETF('ru'), LanguageCode.RUS)
        self.assertEqual(LanguageCode.from_IETF('en'), LanguageCode.ENG)
        self.assertEqual(LanguageCode.from_IETF('abc'), LanguageCode.ENG)
