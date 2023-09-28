import unittest
from src.apps.core.types import LanguageCode
from src.static.menus import MENUS_DATA


class TestMenusData(unittest.TestCase):

    def test_smoke(self):
        _ = MENUS_DATA

    def test_languages(self):
        supported_languages = set(language.name for language in LanguageCode)
        menus_languages = set(MENUS_DATA.keys())
        self.assertEqual(supported_languages, menus_languages)

    def test_getitem(self):
        _ = MENUS_DATA['ENG']['main_menu']
