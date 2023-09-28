from typing import List
from lib.requesters import DefaultRequester
from src.apps.quotes.types import Quote
from src.apps.quotes.scrapers.forbes_all_times import ForbesAllTimesScraper
from src.apps.quotes.scrapers.forbes_inspirational import ForbesInspirationalScraper
from src.apps.quotes.scrapers.oberlo_motivational import OberloMotivaionalScraper

def scrape_all() -> List[Quote]:
    requester = DefaultRequester()
    scrapers = [ForbesAllTimesScraper(requester), OberloMotivaionalScraper(requester), ForbesInspirationalScraper(requester)]
    quotes = []
    for scraper in scrapers:
        for quote in scraper.scrape():
            quotes.append(quote)
    return quotes
