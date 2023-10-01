import unittest
from src.apps.quotes.scrapers.exceptions import BadDataException
from src.apps.quotes.scrapers.shopify_motivational import ShoppifyMotivaionalScraper
from src.apps.quotes.scrapers.utils import DASHES
from src.apps.quotes.types import Quote
from lib.requesters import DefaultRequester


class TestShoppifyMotivaionalScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.requester = DefaultRequester()
        cls.scraper = ShoppifyMotivaionalScraper(cls.requester)
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
        self.assertEqual(self.scraper._parse_row('“We cannot solve problems with the kind of thinking we employed when we came up with them.” — Albert Einstein'), ('“We cannot solve problems with the kind of thinking we employed when we came up with them.”', 'Albert Einstein'))
        self.assertEqual(self.scraper._parse_row('“Women must learn to play the game as men do.” – Eleanor Roosevelt'), ('“Women must learn to play the game as men do.”', 'Eleanor Roosevelt'))
        self.assertEqual(self.scraper._parse_row('“The best time to plant a tree was 20 years ago. The second best time is now.” ―Chinese Proverb'), ('“The best time to plant a tree was 20 years ago. The second best time is now.”', 'Chinese Proverb'))

    def test__parse_row_no_author(self):
        self.assertEqual(self.scraper._parse_row('“H.O.P.E. = Hold On. Pain Ends.” —'), ('“H.O.P.E. = Hold On. Pain Ends.”', ''))
        self.assertEqual(self.scraper._parse_row('Don’t dream about success. Get out there and work for it.'), ('Don’t dream about success. Get out there and work for it.', ''))
        self.assertEqual(self.scraper._parse_row('“Everyone thinks of changing the world, but no one thinks of changing himself.”'), ('“Everyone thinks of changing the world, but no one thinks of changing himself.”', ''))
        self.assertEqual(self.scraper._parse_row('“You can’t have a million-dollar dream on a minimum wage work ethic.” ―Unknown'), ('“You can’t have a million-dollar dream on a minimum wage work ethic.”', 'Unknown'))
        self.assertEqual(self.scraper._parse_row('“You learn more from failure than from success. Don’t let it stop you. Failure builds character.” — Unknown'), ('“You learn more from failure than from success. Don’t let it stop you. Failure builds character.”', 'Unknown'))

    def test__parse_row_tricky(self):
        self.assertEqual(self.scraper._parse_row('“I will not lose, for even in defeat, there’s a valuable lesson learned, so it evens up for me.” —Jay-Z'), ('“I will not lose, for even in defeat, there’s a valuable lesson learned, so it evens up for me.”', 'Jay-Z'))

    def test__parse_row_bad_row(self):
        with self.assertRaises(BadDataException):
            self.scraper._parse_row('―Leo Tolstoy')

    def test__beautify_text(self):
        self.assertEqual(self.scraper._beautify_text('Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text(' Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('“ Hello”'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('”””Hello“““'), 'Hello')
        self.assertEqual(self.scraper._beautify_text('“Hello'), 'Hello')
        self.assertEqual(self.scraper._beautify_text(' “  Hello, some text here!!... “ '), 'Hello, some text here!!...')
        self.assertEqual(self.scraper._beautify_text('“All our dreams can come true, if we have the courage to pursue them.” '), 'All our dreams can come true, if we have the courage to pursue them.')
        self.assertEqual(self.scraper._beautify_text('“We cannot solve problems with the kind of thinking we employed when we came up with them.”'), 'We cannot solve problems with the kind of thinking we employed when we came up with them.')

    def test__beautify_author(self):
        self.assertEqual(self.scraper._beautify_author('Somename'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename '), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\r\n'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('Somename\xa0'), 'Somename')
        self.assertEqual(self.scraper._beautify_author('—Walt Disney'), 'Walt Disney')
        self.assertEqual(self.scraper._beautify_author('―Thomas Ediso'), 'Thomas Ediso')
        self.assertEqual(self.scraper._beautify_author('— Albert Einstein'), 'Albert Einstein')
        for dash in DASHES:
            self.assertEqual(self.scraper._beautify_author(f'{dash}Somename'), 'Somename')
            self.assertEqual(self.scraper._beautify_author(f'{dash}Unknown'), None)
            self.assertEqual(self.scraper._beautify_author(dash), None)

