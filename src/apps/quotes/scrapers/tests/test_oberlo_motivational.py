import unittest
from src.apps.quotes.scrapers.oberlo_motivational import OberloMotivaionalScraper
from src.apps.quotes.scrapers.utils import DASHES
from src.apps.quotes.types import Quote
from lib.requesters import DefaultRequester


class TestOberloMotivaionalScraper(unittest.TestCase):

    def setUp(self):
        self.requester = DefaultRequester()
        self.scraper = OberloMotivaionalScraper(self.requester)
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

    def test__parse_row(self):
        self.assertEqual(self.scraper._parse_row('“All our dreams can come true, if we have the courage to pursue them.” —Walt Disney'), ('“All our dreams can come true, if we have the courage to pursue them.”', 'Walt Disney'))
        self.assertEqual(self.scraper._parse_row('“The best time to plant a tree was 20 years ago. The second best time is now.” ―Chinese Proverb'), ('“The best time to plant a tree was 20 years ago. The second best time is now.”', 'Chinese Proverb'))
        self.assertEqual(self.scraper._parse_row('“H.O.P.E. = Hold On. Pain Ends.” —'), ('“H.O.P.E. = Hold On. Pain Ends.”', ''))
        self.assertEqual(self.scraper._parse_row('Don’t dream about success. Get out there and work for it.'), ('Don’t dream about success. Get out there and work for it.', ''))
        self.assertEqual(self.scraper._parse_row('“You can’t have a million-dollar dream on a minimum wage work ethic.” ―Unknown'), ('“You can’t have a million-dollar dream on a minimum wage work ethic.”', 'Unknown'))

    def test__beautify_text(self):
        self.assertEqual(self.scraper._beautify_text('Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text(' Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('“ Hello”'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('”””Hello“““'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('“Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text(' “  Hello, some text here!!... “ '), 'Hello, some text here!!...')
        self.assertEqual(self.scraper._beautify_text('“All our dreams can come true, if we have the courage to pursue them.” '), 'All our dreams can come true, if we have the courage to pursue them.')

    def test__beautify_author(self):
        self.assertEqual(self.scraper._beautify_author('Somename'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename '), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\r\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\xa0'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('—Walt Disney'), 'Walt Disney')
        self.assertEqual(self.scraper._beautify_author('―Thomas Ediso'), 'Thomas Ediso')
        for dash in DASHES:
            self.assertEqual(self.scraper._beautify_author(f'{dash}Somename'), 'Somename')
            self.assertEqual(self.scraper._beautify_author(f'{dash}Unknown'), None)
            self.assertEqual(self.scraper._beautify_author(dash), None)

