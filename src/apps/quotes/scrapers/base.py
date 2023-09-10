from abc import ABC, abstractmethod
from typing import Iterable
from lib.requesters import RequesterBase
from src.apps.quotes.utils import Quote


class ScraperBase(ABC):
    def __init__(self, requester: RequesterBase):
        self._requester = requester

    @abstractmethod
    def scrape(self) -> Iterable[Quote]:
        pass

    @property
    def requester(self):
        return self._requester
