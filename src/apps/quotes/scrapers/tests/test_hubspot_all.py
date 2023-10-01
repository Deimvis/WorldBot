import unittest
from src.apps.quotes.scrapers.hubspot_all import HubspotAllScraper
from src.apps.quotes.types import Quote
from lib.requesters import DefaultRequester


class TestHubspotAllScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.requester = DefaultRequester()
        cls.scraper = HubspotAllScraper(cls.requester)
        cls.scrape_result = list(cls.scraper.scrape())

    def test_smoke(self):
        self.assertIsNotNone(self.scrape_result)

    def test_result_is_not_empty(self):
        self.assertGreater(len(self.scrape_result), 0)

    def test_result_has_correct_type(self):
        for quote in self.scrape_result:
            self.assertIsInstance(quote, Quote)
