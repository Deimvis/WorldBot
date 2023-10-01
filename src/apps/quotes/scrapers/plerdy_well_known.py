import bs4
import re
import logging
from typing import Iterable, Tuple
from src.apps.core.types import LanguageCode
from src.apps.quotes.types import Quote
from src.apps.quotes.scrapers.base import ScraperBase
from src.apps.quotes.scrapers.exceptions import BadDataException
from src.apps.quotes.scrapers.utils import CLOSING_QUOTES, DASHES, OPENING_QUOTES
from bs4 import BeautifulSoup


log_ = logging.getLogger('ForbesAllTimesScraper')


class PlerdyWellKnownScraper(ScraperBase):
    SOURCE_NAME = 'plerdy/well_knwon/RUS'
    URL = 'https://www.plerdy.com/ru/blog/top-famous-quotes/'
    LANGUAGE = LanguageCode.RUS

    def scrape(self) -> Iterable[Quote]:
        soup = self.get_soup()
        for row in self._parse_quote_rows(soup):
            try:
                text_, author_ = self._parse_row(row)
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

    def _parse_quote_rows(self, soup: BeautifulSoup) -> Iterable[bs4.element.Tag]:
        for header in soup.select('h2'):
            if header.text in ['20 самых известных цитат из фильмов', '20 самых известных цитат о любви']:
                continue
            for el in header.next_siblings:
                match el.name:
                    case 'h2':
                        break
                    case 'ul':
                        for item in el.select('li'):
                            yield item

    def _parse_row(self, row: bs4.element.Tag) -> Tuple[str, str]:
        """ Returns: (text, author) """
        if row.find('em'):
            return row.find(string=True, recursive=False).strip(), row.select_one('em').text.strip()
        return self._parse_raw_row(row.text)

    def _parse_raw_row(self, row: str) -> Tuple[str, str]:
        """ Returns: (text, author) """
        pattern = rf'^(?P<text>[{"".join(OPENING_QUOTES)}].*[{"".join(CLOSING_QUOTES)}])\.?\s*(?P<author>.*)$'
        match = re.fullmatch(pattern, row)
        if match:
            return match.group('text'), match.group('author')
        if any(dash in row for dash in DASHES):
            raise BadDataException(f'Bad quote row: {row}')
        log_.debug('Row is out of pattern: %s', row)
        logging.error('Out of pattern %s', row)
        return row.strip(), ''

    def _beautify_text(self, text: str) -> str:
        text = text.strip().rstrip('.')
        return text[(text[0] in OPENING_QUOTES):len(text)-(text[-1] in CLOSING_QUOTES)].strip()

    def _beautify_author(self, author: str) -> str:
        return author.strip()
