import unittest
from src.apps.quotes.scrapers.forbes_inspirational import ForbesInspirationalScraper
from src.apps.quotes.scrapers.utils import DASHES
from src.apps.quotes.types import Quote
from lib.requesters import DefaultRequester


class TestForbesInspirationalScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.requester = DefaultRequester()
        cls.scraper = ForbesInspirationalScraper(cls.requester)
        cls.scrape_result = list(cls.scraper.scrape())

    def test_smoke(self):
        self.assertIsNotNone(self.scrape_result)

    def test_result_is_not_empty(self):
        self.assertGreater(len(self.scrape_result), 0)

    def test_result_has_correct_type(self):
        for quote in self.scrape_result:
            self.assertIsInstance(quote, Quote)

    def test_get_soup(self):
        _ = self.scraper.get_soup()

    def test__is_quote_row(self):
        self.assertEqual(self.scraper._is_quote_row(''), False)
        self.assertEqual(self.scraper._is_quote_row('some text'), False)
        self.assertEqual(self.scraper._is_quote_row('1.\xa0 Life is about making an impact, not making an income. --Kevin Kruse'), True)

    def test__parse_row(self):
        self.assertEqual(self.scraper._parse_row('1.\xa0 Life is about making an impact, not making an income. --Kevin Kruse'), ('1.\xa0 Life is about making an impact, not making an income.', 'Kevin Kruse'))
        self.assertEqual(self.scraper._parse_row('3. Strive not to be a success, but rather to be of value. –Albert Einstein'), ('3. Strive not to be a success, but rather to be of value.', 'Albert Einstein'))

    def test__beautify_text(self):
        self.assertEqual(self.scraper._beautify_text('Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text(' Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('. Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('1. Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('123... Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text(' .9..9  Hello, some text here!!...'), 'Hello, some text here!!...')
        self.assertEqual(self.scraper._beautify_text('1.\xa0 Life is about making an impact, not making an income.'), 'Life is about making an impact, not making an income.')
        self.assertEqual(self.scraper._beautify_text('3. Strive not to be a success, but rather to be of value.'), 'Strive not to be a success, but rather to be of value.')

    def test__beautify_author(self):
        self.assertEqual(self.scraper._beautify_author('Somename'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename '), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\r\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\xa0'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('--Kevin Kruse'), 'Kevin Kruse')
        self.assertEqual(self.scraper._beautify_author('–Albert Einstein'), 'Albert Einstein')
        for dash in DASHES:
            self.assertEqual(self.scraper._beautify_author(dash), None)

