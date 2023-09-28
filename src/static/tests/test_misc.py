import unittest
from src.apps.core.types import LanguageCode
from src.static.misc import MISC_DATA


class TestMiscData(unittest.TestCase):

    def test_smoke(self):
        _ = MISC_DATA

    def test_languages(self):
        supported_languages = set(language.name for language in LanguageCode)
        menus_languages = set(MISC_DATA.keys())
        self.assertEqual(supported_languages, menus_languages)

    def test_getitem(self):
        _ = MISC_DATA['ENG']['weekdays']
