import calendar
import pytz
import re
import time
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Self
from src.apps.core.types import LanguageCode
from src.static import MISC


class Source(BaseModel):
    name: str
    url: str | None


class Quote(BaseModel):
    author: str | None = None
    text: str
    language: LanguageCode
    source: Source | None = None

    @field_validator('author')
    @classmethod
    def is_author_valid(cls, v):
        assert v is None or len(v) >= 2, 'Author name is too short'
        assert v is None or len(v) <= 1000, 'Author name is too long'
        return v

    @field_validator('text')
    @classmethod
    def is_text_valid(cls, v):
        assert len(v) >= 1, 'Text is empty'
        return v

    @field_validator('language')
    @classmethod
    def is_quotes_language_supported(cls, v):
        assert v.name in ('ENG', 'RUS')
        return v

    def to_database_row(self):
        return {
            'text': self.text,
            'author': self.author,
            'language': self.language.name,
            'source': self.source.model_dump_json() if self.source else None,
        }

    @staticmethod
    def from_database_row(row):
        return Quote(
            author=row['author'],
            text=row['text'],
            language=LanguageCode[row['language']],
            source=Source.model_validate_json(row['source']) if row['source'] else None,
        )


class RawSubscription(BaseModel, validate_assignment=True):
    interval: str | None = None
    base_weekday: str | None = None
    timezone: str | None = None
    base_time: str | None = None

    @field_validator('interval')
    @classmethod
    def interval_is_valid(cls, v):
        assert v in ['EVERY_DAY', 'EVERY_WEEK'], 'Incorrect interval'
        return v

    @field_validator('base_weekday')
    @classmethod
    def base_weekday_is_valid(cls, v):
        assert v is None or v in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'], 'Incorrect base_weekday'
        return v

    @field_validator('timezone')
    @classmethod
    def timezone_is_valid(cls, v):
        assert v in pytz.all_timezones_set, 'Unsupported timezone'
        return v

    @field_validator('base_time')
    @classmethod
    def base_time_is_valid(cls, v):
        assert re.fullmatch(r'^[0-9]{2}:[0-9]{2}', v), 'base_time has invalid format'
        hours, minutes = map(int, v.split(':'))
        assert 0 <= hours <= 23, 'Specified hours for base_time are out of range'
        assert 0 <= minutes <= 59, 'Specified minutes for base_time are out of range'
        return v


class Subscription(BaseModel):
    chat_id: int
    base_weekday: int | None = None
    base_hour: int
    base_minute: int
    timezone: str
    language: LanguageCode
    creation_ts: int = Field(default_factory=lambda: int(time.time()))
    raw_subscription: RawSubscription

    @field_validator('base_weekday')
    @classmethod
    def base_weekday_is_valid(cls, v):
        assert v is None or 0 <= v <= 6, 'base_weekday is out of range'
        return v

    @field_validator('base_hour')
    @classmethod
    def base_hour_is_valid(cls, v):
        assert 0 <= v <= 23, 'base_hour is out of range'
        return v

    @field_validator('base_minute')
    @classmethod
    def base_minute_is_valid(cls, v):
        assert 0 <= v <= 59, 'base_minute is out of range'
        return v

    @field_validator('timezone')
    @classmethod
    def timezone_is_valid(cls, v):
        assert v in pytz.all_timezones_set, 'Unsupported timezone'
        return v

    def overview(self, language: LanguageCode) -> str:
        result = f'{str(self.base_hour).zfill(2)}:{str(self.base_minute).zfill(2)} ({self.timezone})'
        if self.base_weekday is not None:
            weekday_name = MISC[language.name]['weekdays'][calendar.day_name[self.base_weekday].lower()]
            result = f'{weekday_name}, {result}'
        return result

    @staticmethod
    def from_raw_subscription(raw_subscription: RawSubscription, chat_id: int, language: LanguageCode) -> Self:
        assert raw_subscription.interval is not None, 'Raw subscription doesn\'t have interval'
        assert raw_subscription.timezone is not None, 'Raw subscription doesn\'t have timezone'
        assert raw_subscription.base_time is not None, 'Raw subscription doesn\'t have base_time'
        assert (raw_subscription.interval != 'EVERY_WEEK' or raw_subscription.base_weekday is not None), 'Raw subscription doesn\'t have base_weekday'
        base_weekday = getattr(calendar, raw_subscription.base_weekday.upper()) if raw_subscription.base_weekday is not None else None
        base_hour, base_minute = map(int, raw_subscription.base_time.split(':'))
        return Subscription(
            chat_id=chat_id,
            base_weekday=base_weekday,
            base_hour=base_hour,
            base_minute=base_minute,
            timezone=raw_subscription.timezone,
            language=language,
            raw_subscription=raw_subscription,
        )

    def to_database_row(self) -> Dict:
        return {
            'chat_id': self.chat_id,
            'base_weekday': self.base_weekday,
            'base_hour': self.base_hour,
            'base_minute': self.base_minute,
            'timezone': self.timezone,
            'language': self.language.name,
            'creation_ts': self.creation_ts,
            '_raw': self.raw_subscription.model_dump_json()
        }

    @staticmethod
    def from_database_row(row) -> Self:
        return Subscription(
            chat_id=row['chat_id'],
            base_weekday=row['base_weekday'],
            base_hour=row['base_hour'],
            base_minute=row['base_minute'],
            timezone=row['timezone'],
            language=LanguageCode[row['language']],
            creation_ts=row['creation_ts'],
            raw_subscription=RawSubscription.model_validate_json(row['_raw']),
        )
