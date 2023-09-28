from typing import Iterable, Tuple
from src.apps.core.types import LanguageCode
from src.apps.quotes.types import Quote
from src.apps.quotes.scrapers.base import ScraperBase
from src.apps.quotes.scrapers.utils import DASHES
from bs4 import BeautifulSoup


class OberloMotivaionalScraper(ScraperBase):
    SOURCE_NAME = 'oberlo/motivational/ENG'
    URL = 'https://www.oberlo.com/blog/motivational-quotes'
    LANGUAGE = LanguageCode.ENG

    def scrape(self) -> Iterable[Quote]:
        soup = self.get_soup()
        rows = soup.select('.single-post ol li')
        for row in rows:
            text_, author_ = self._parse_row(row.text)
            text = self._beautify_text(text_)
            author = self._beautify_author(author_)
            if len(text) == 0:
                continue
            yield Quote(author=author, text=text, language=self.LANGUAGE, source=self.source())

    def get_soup(self):
        response = self.requester.get(self.URL)
        return BeautifulSoup(response.text, 'html.parser')

    def _parse_row(self, row: str) -> Tuple[str, str]:
        """ Returns: (text, author) """
        max_split_ind = -1
        for dash in DASHES:
            max_split_ind = max(max_split_ind, row.rfind(dash))
        if max_split_ind == -1:
            return row.strip(), ''
        return row[:max_split_ind].rstrip(''.join(DASHES)).strip(), row[max_split_ind+1:].strip()

    def _beautify_text(self, text: str) -> str:
        return text.strip().strip(' “”')

    def _beautify_author(self, author: str) -> str | None:
        result = author.strip().strip(' ' + ''.join(DASHES))
        if result in ['', 'Unknown']:
            return None
        return result
