from tqdm import tqdm
from typing import List
from lib.requesters import DefaultRequester
from src.apps.quotes.types import Quote
from src.apps.quotes.scrapers.forbes_all_times import ForbesAllTimesScraper
from src.apps.quotes.scrapers.forbes_inspirational import ForbesInspirationalScraper
from src.apps.quotes.scrapers.hubspot_all import HubspotAllScraper
from src.apps.quotes.scrapers.oberlo_motivational import OberloMotivaionalScraper
from src.apps.quotes.scrapers.plerdy_well_known import PlerdyWellKnownScraper
from src.apps.quotes.scrapers.shopify_motivational import ShoppifyMotivaionalScraper


def scrape_all() -> List[Quote]:
    requester = DefaultRequester()
    scrapers = [
        ForbesAllTimesScraper(requester),
        OberloMotivaionalScraper(requester),
        ForbesInspirationalScraper(requester),
        ShoppifyMotivaionalScraper(requester),
        PlerdyWellKnownScraper(requester),
        HubspotAllScraper(requester),
    ]
    quotes = []
    for scraper in tqdm(scrapers, desc='scrape_all'):
        for quote in scraper.scrape():
            quotes.append(quote)
    return quotes
