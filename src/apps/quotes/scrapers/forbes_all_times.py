from typing import Iterable
from src.apps.core.types import LanguageCode
from src.apps.quotes.types import Quote, Source
from src.apps.quotes.scrapers.base import ScraperBase
from bs4 import BeautifulSoup


class ForbesAllTimesScraper(ScraperBase):
    SOURCE_NAME = 'forbes/all_times/RUS'
    URL = 'https://www.forbes.ru/forbeslife/dosug/262327-na-vse-vremena-100-vdokhnovlyayushchikh-tsitat'
    LANGUAGE = LanguageCode.RUS

    def scrape(self) -> Iterable[Quote]:
        soup = self.get_soup()
        rows = soup.select('p[itemprop="articleBody"]')
        for i in range(0, len(rows), 2):
            text = self._beautify_text(rows[i].text)
            author = self._beautify_author(rows[i+1].text)
            yield Quote(author=author, text=text, language=self.LANGUAGE, source=self.source())

    def get_soup(self):
        response = self.requester.get(self.URL)
        return BeautifulSoup(response.text, 'html.parser')

    def _beautify_text(self, text: str) -> str:
        return text.strip().lstrip('0123456789.').lstrip()

    def _beautify_author(self, author: str) -> str:
        return author.strip()
