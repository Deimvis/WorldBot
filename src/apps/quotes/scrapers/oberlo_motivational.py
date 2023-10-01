import logging
import re
from typing import Iterable, Tuple
from src.apps.core.types import LanguageCode
from src.apps.quotes.types import Quote
from src.apps.quotes.scrapers.base import ScraperBase
from src.apps.quotes.scrapers.exceptions import BadDataException
from src.apps.quotes.scrapers.utils import CLOSING_QUOTES, DASHES, OPENING_QUOTES
from bs4 import BeautifulSoup


log_ = logging.getLogger('OberloMotivaionalScraper')


class OberloMotivaionalScraper(ScraperBase):
    SOURCE_NAME = 'oberlo/motivational/ENG'
    URL = 'https://www.oberlo.com/blog/motivational-quotes'
    LANGUAGE = LanguageCode.ENG

    def scrape(self) -> Iterable[Quote]:
        soup = self.get_soup()
        rows = soup.select('.single-post ol li')
        for row in rows:
            try:
                text_, author_ = self._parse_row(row.text)
                text = self._beautify_text(text_)
                author = self._beautify_author(author_)
                if len(text) == 0:
                    continue
                yield Quote(author=author, text=text, language=self.LANGUAGE, source=self.source())
            except BadDataException as error:
                log_.info(str(error))

    def get_soup(self):
        response = self.requester.get(self.URL)
        return BeautifulSoup(response.text, 'html.parser')

    def _parse_row(self, row: str) -> Tuple[str, str]:
        """ Returns: (text, author) """
        pattern = rf'^(?P<text>[{"".join(OPENING_QUOTES)}].*[{"".join(CLOSING_QUOTES)}])\s*[{"".join(DASHES)}](?:\s|[{"".join(DASHES)}])*(?P<author>.*)$'
        match = re.fullmatch(pattern, row)
        if match:
            return match.group('text'), match.group('author')
        if any(dash in row for dash in DASHES):
            raise BadDataException(f'Bad quote row: {row}')
        log_.debug('Row is out of pattern: %s', row)
        return row.strip(), ''

    def _beautify_text(self, text: str) -> str:
        return text.strip().strip(' ' + ''.join(OPENING_QUOTES) + ''.join(CLOSING_QUOTES))

    def _beautify_author(self, author: str) -> str | None:
        result = author.strip().strip(' ' + ''.join(DASHES))
        if result in ['', 'Unknown']:
            return None
        return result
