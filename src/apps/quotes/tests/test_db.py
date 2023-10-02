import unittest
import src.apps.quotes.db as db
from src.apps.core.types import LanguageCode


class TestDb(unittest.TestCase):

    def test_get_random_quote(self):
        db.get_random_quote(LanguageCode.ENG)
        db.get_random_quote(LanguageCode.RUS)
