from typing import Iterable, Tuple
from src.apps.core.types import LanguageCode
from src.apps.quotes.types import Quote
from src.apps.quotes.scrapers.base import ScraperBase
from src.apps.quotes.scrapers.utils import DASHES
from bs4 import BeautifulSoup


class ShoppifyMotivaionalScraper(ScraperBase):
    SOURCE_NAME = 'shopify/motivational/ENG'
    URL = 'https://www.shopify.com/blog/motivational-quotes'
    LANGUAGE = LanguageCode['ENG']

    # TODO:
    def scrape(self) -> Iterable[Quote]:
        soup = self.get_soup()
        rows = soup.select('.single-post ol li')
        for row in rows:
            text_, author_ = self._parse_row(row.text)
            text = self._beautify_text(text_)
            author = self._beautify_author(author_)
            # TODO: remove
            try:
                Quote(author=author, text=text, language=self.LANGUAGE)
            except Exception as error:
                import logging
                logging.error(f'BAD {author}, {text}')
            yield Quote(author=author, text=text, language=self.LANGUAGE, source=self.source())

    def get_soup(self):
        response = self.requester.get(self.URL)
        return BeautifulSoup(response.text, 'html.parser')

    def _parse_row(self, row: str) -> Tuple[str, str]:
        """ Returns: (text, author) """
        for dash in DASHES:
            split_ind = row.rfind(dash)
            if split_ind == -1:
                continue
            return row[:split_ind].strip(), row[split_ind+1:].strip()
        return row.strip(), ''

    def _beautify_text(self, text: str) -> str:
        return text.strip().strip(' “”')

    def _beautify_author(self, author: str) -> str | None:
        result = author.strip().strip(' ' + ''.join(DASHES))
        if result in ['', 'Unknown']:
            return None
        return result
