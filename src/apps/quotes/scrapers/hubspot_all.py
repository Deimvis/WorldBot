import csv
import logging
import re
import os
from pathlib import Path
from typing import Iterable
from src.apps.core.types import LanguageCode
from src.apps.quotes.types import Quote
from src.apps.quotes.scrapers.base import ScraperBase
from src.apps.quotes.scrapers.exceptions import BadDataException
from src.apps.quotes.scrapers.utils import CLOSING_QUOTES, DASHES, OPENING_QUOTES


log_ = logging.getLogger('HubspotAllScraper')


class HubspotAllScraper(ScraperBase):
    SOURCE_NAME = 'hubspot/all/ENG'
    URL = 'https://offers.hubspot.com/250-famous-quotes'
    LANGUAGE = LanguageCode.ENG

    def scrape(self) -> Iterable[Quote]:
        with (Path(os.getenv('FILES_DIR_PATH')) / 'quotes' / 'hubspot.tsv').open() as file:
            reader = csv.DictReader(file, delimiter='\t', )
            for row in reader:
                yield Quote(author=row['Author'], text=row['Text'], language=self.LANGUAGE, source=self.source())
