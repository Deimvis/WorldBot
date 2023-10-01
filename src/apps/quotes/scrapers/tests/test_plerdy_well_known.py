import unittest
from bs4 import BeautifulSoup
from src.apps.quotes.scrapers.plerdy_well_known import PlerdyWellKnownScraper
from src.apps.quotes.types import Quote
from lib.requesters import DefaultRequester


class PlerdyWellKnownScraperScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.requester = DefaultRequester()
        cls.scraper = PlerdyWellKnownScraper(cls.requester)
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

    def test__parse_row_simple(self):
        row = BeautifulSoup('<li>«Надеюсь, что после смерти я встречусь с Богом. Предстану перед ним без таланта, и с чистой совестью сообщу Творцу: “Все, что ты подарил мне, я использовала”». <em>Erma Louise Bombeck</em></li>', 'html.parser').select_one('li')
        self.assertEqual(self.scraper._parse_row(row), ('«Надеюсь, что после смерти я встречусь с Богом. Предстану перед ним без таланта, и с чистой совестью сообщу Творцу: “Все, что ты подарил мне, я использовала”».', 'Erma Louise Bombeck'))
        row = BeautifulSoup('<li>«Не тратьте время и не бейтесь в стену. Она не превратится в дверь». Coco Chanel</li>', 'html.parser').select_one('li')
        self.assertEqual(self.scraper._parse_row(row), ('«Не тратьте время и не бейтесь в стену. Она не превратится в дверь»', 'Coco Chanel'))

    def test__beautify_text(self):
        self.assertEqual(self.scraper._beautify_text('Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text(' Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('“ Hello”'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('“Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('«Надеюсь, что после смерти я встречусь с Богом. Предстану перед ним без таланта, и с чистой совестью сообщу Творцу: “Все, что ты подарил мне, я использовала”».'), 'Надеюсь, что после смерти я встречусь с Богом. Предстану перед ним без таланта, и с чистой совестью сообщу Творцу: “Все, что ты подарил мне, я использовала”')

    def test__beautify_author(self):
        self.assertEqual(self.scraper._beautify_author('Somename'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename '), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\r\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\xa0'), 'Somename')
