from abc import ABC, abstractmethod
from typing import Iterable
from lib.requesters import RequesterBase
from src.apps.quotes.types import Quote, Source


class ScraperBase(ABC):
    def __init__(self, requester: RequesterBase):
        self._requester = requester

    @abstractmethod
    def scrape(self) -> Iterable[Quote]:
        pass

    @property
    def requester(self):
        return self._requester

    @classmethod
    def source(cls) -> Source | None:
        if hasattr(cls, 'SOURCE_NAME'):
            return Source(name=getattr(cls, 'SOURCE_NAME'), url=getattr(cls, 'URL', None))
        return None
