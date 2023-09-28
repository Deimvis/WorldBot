import unittest
from src.apps.quotes.scrapers.forbes_all_times import ForbesAllTimesScraper
from src.apps.quotes.types import Quote
from lib.requesters import DefaultRequester


class TestForbesAllTimesScraper(unittest.TestCase):

    def setUp(self):
        self.requester = DefaultRequester()
        self.scraper = ForbesAllTimesScraper(self.requester)
        self.scrape_result = list(self.scraper.scrape())

    def test_smoke(self):
        self.assertIsNotNone(self.scrape_result)

    def test_result_is_not_empty(self):
        self.assertGreater(len(self.scrape_result), 0)

    def test_result_has_correct_type(self):
        for quote in self.scrape_result:
            self.assertIsInstance(quote, Quote)

    def test_get_soup(self):
        _ = self.scraper.get_soup()

    def test__beautify_text(self):
        self.assertEqual(self.scraper._beautify_text('Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text(' Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('. Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('1. Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('123... Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text(' .9..9  Hello, some text here!!...'), 'Hello, some text here!!...')

    def test__beautify_author(self):
        self.assertEqual(self.scraper._beautify_author('Somename'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename '), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\r\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\xa0'), 'Somename')
