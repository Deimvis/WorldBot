import re
from typing import Iterable, Tuple
from src.apps.core.types import LanguageCode
from src.apps.quotes.types import Quote
from src.apps.quotes.scrapers.base import ScraperBase
from src.apps.quotes.scrapers.utils import DASHES
from bs4 import BeautifulSoup


class ForbesInspirationalScraper(ScraperBase):
    SOURCE_NAME = 'forbes/inspirational/ENG'
    URL = 'https://www.forbes.com/sites/kevinkruse/2013/05/28/inspirational-quotes'
    LANGUAGE = LanguageCode['ENG']

    def scrape(self) -> Iterable[Quote]:
        soup = self.get_soup()
        rows = soup.select('.current-article p')
        for row in rows:
            if not self._is_quote_row(row.text):
                continue
            text_, author_ = self._parse_row(row.text)
            text = self._beautify_text(text_)
            author = self._beautify_author(author_)
            yield Quote(author=author, text=text, language=self.LANGUAGE, source=self.source())

    def get_soup(self):
        response = self.requester.get(self.URL)
        return BeautifulSoup(response.text, 'html.parser')

    def _is_quote_row(self, row: str) -> bool:
        return re.fullmatch(r'[0-9]+\..*', row) is not None

    def _parse_row(self, row: str) -> Tuple[str, str]:
        """ Returns: (text, author) """
        max_split_ind = -1
        for dash in DASHES:
            max_split_ind = max(max_split_ind, row.rfind(dash))
        if max_split_ind == -1:
            return row.strip(), ''
        return row[:max_split_ind].rstrip(''.join(DASHES)).strip(), row[max_split_ind+1:].strip()

    def _beautify_text(self, text: str) -> str:
        return text.strip().lstrip('0123456789.').lstrip()

    def _beautify_author(self, author: str) -> str | None:
        result = author.strip().strip(' ' + ''.join(DASHES))
        if result in ['']:
            return None
        return result
