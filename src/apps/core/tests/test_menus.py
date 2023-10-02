import unittest
from src.apps.core.menus import build_main_menu
from src.apps.core.types import LanguageCode


class TestBuildMainMenu(unittest.TestCase):

    def test_smoke(self):
        _ = build_main_menu(LanguageCode.ENG)

    def test_simple(self):
        build_main_menu(LanguageCode.ENG)
        build_main_menu(LanguageCode.RUS)
