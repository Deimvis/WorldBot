import unittest
from pydantic import ValidationError
from src.apps.core.types import LanguageCode
from src.apps.quotes.types import Quote, RawSubscription, Source, Subscription


class TestQuote(unittest.TestCase):

    def test_smoke(self):
        _ = Quote(author='Michael Altshuler', text='The bad news is time flies. The good news is you\'re the pilot.', language=LanguageCode.ENG)

    def test_invalid_author(self):
        with self.assertRaises(ValidationError):
            Quote(author='a' * 1001, text='hello', language=LanguageCode.ENG)

    def test_invalid_text(self):
        with self.assertRaises(ValidationError):
            Quote(text='', language=LanguageCode.ENG)

    def test_valid_author(self):
        _ = Quote(author=None, text='hello', language=LanguageCode.ENG)

    def test_invalid_language(self):
        with self.assertRaises(ValidationError):
            Quote(text='hello', language='123')
        with self.assertRaises(ValidationError):
            Quote(text='hello', language='english')
        with self.assertRaises(ValidationError):
            Quote(text='hello', language='eng')
        with self.assertRaises(ValidationError):
            Quote(text='hello', language='ENG')

    def test_valid_language(self):
        _ = Quote(text='hello', language=LanguageCode.ENG)
        _ = Quote(text='hello', language=LanguageCode.RUS)

    def test_to_database_row(self):
        _ = Quote(author='Michael Altshuler', text='The bad news is time flies. The good news is you\'re the pilot.', language=LanguageCode.ENG, source=Source(name='Forbes', url='https://forbes.com')).to_database_row()

    def test_from_database_row(self):
        _ = Quote.from_database_row({'author': 'Michael Altshuler', 'text': 'The bad news is time flies. The good news is you\'re the pilot.', 'language': 'ENG', 'source': None})


class TestRawSubscription(unittest.TestCase):

    def test_smoke(self):
        _ = RawSubscription()

    def test_invalid_interval(self):
        with self.assertRaises(ValidationError):
            RawSubscription(interval='123')
        with self.assertRaises(ValidationError):
            RawSubscription(interval='EVERY_SECOND')
        with self.assertRaises(ValidationError):
            RawSubscription(interval='EVERY_MINUTE')
        with self.assertRaises(ValidationError):
            RawSubscription(interval='EVERY_HOUR')

    def test_valid_interval(self):
        RawSubscription(interval='EVERY_DAY')
        RawSubscription(interval='EVERY_WEEK')

    def test_invalid_base_weekday(self):
        with self.assertRaises(ValidationError):
            RawSubscription(base_weekday='123')
        with self.assertRaises(ValidationError):
            RawSubscription(base_weekday='Monday')
        with self.assertRaises(ValidationError):
            RawSubscription(base_weekday='monday')

    def test_valid_base_weekday(self):
        RawSubscription(base_weekday='MONDAY')
        RawSubscription(base_weekday='TUESDAY')
        RawSubscription(base_weekday='WEDNESDAY')
        RawSubscription(base_weekday='THURSDAY')
        RawSubscription(base_weekday='FRIDAY')
        RawSubscription(base_weekday='SATURDAY')
        RawSubscription(base_weekday='SUNDAY')

    def test_invalid_timezone(self):
        with self.assertRaises(ValidationError):
            RawSubscription(timezone='MSK')
        with self.assertRaises(ValidationError):
            RawSubscription(timezone='Москва')

    def test_valid_timezone(self):
        RawSubscription(timezone='UTC')
        RawSubscription(timezone='GMT')
        RawSubscription(timezone='EST')
        RawSubscription(timezone='Europe/Amsterdam')
        RawSubscription(timezone='America/Adak')
        RawSubscription(timezone='Europe/Moscow')
        RawSubscription(timezone='Etc/GMT+3')
        RawSubscription(timezone='Etc/GMT+6')
        RawSubscription(timezone='Etc/GMT+9')
        RawSubscription(timezone='Etc/GMT+12')

    def test_invalid_base_time(self):
        with self.assertRaises(ValidationError):
            RawSubscription(base_time='123')
        with self.assertRaises(ValidationError):
            RawSubscription(base_time='12-00')
        with self.assertRaises(ValidationError):
            RawSubscription(base_time='12 00')
        with self.assertRaises(ValidationError):
            RawSubscription(base_time='1200')
        with self.assertRaises(ValidationError):
            RawSubscription(base_time='12 : 00')
        with self.assertRaises(ValidationError):
            RawSubscription(base_time='24:00')
        with self.assertRaises(ValidationError):
            RawSubscription(base_time='00:60')

    def test_valid_base_time(self):
        RawSubscription(base_time='12:00')
        RawSubscription(base_time='13:45')
        RawSubscription(base_time='00:00')
        RawSubscription(base_time='23:59')


class TestSubscription(unittest.TestCase):

    def setUp(self):
        self.raw_subs = [
            RawSubscription(interval='EVERY_WEEK', base_weekday='MONDAY', timezone='UTC', base_time='12:00'),
            RawSubscription(interval='EVERY_DAY', timezone='UTC', base_time='12:00'),
        ]

    def test_smoke(self):
        _ = Subscription(chat_id=1, base_weekday=0, base_hour=12, base_minute=30, timezone='UTC', language=LanguageCode.ENG, raw_subscription=self.raw_subs[0])

    def test_invalid_base_weekday(self):
        with self.assertRaises(ValidationError):
            Subscription(chat_id=1, base_weekday=-1, base_hour=0, base_minute=0, timezone='UTC', language=LanguageCode.ENG, raw_subscription=self.raw_subs[0])
        with self.assertRaises(ValidationError):
            Subscription(chat_id=1, base_weekday=7, base_hour=0, base_minute=0, timezone='UTC', language=LanguageCode.ENG, raw_subscription=self.raw_subs[0])

    def test_invalid_base_hour(self):
        with self.assertRaises(ValidationError):
            Subscription(chat_id=1, base_weekday=0, base_hour=-1, base_minute=0, timezone='UTC', language=LanguageCode.ENG, raw_subscription=self.raw_subs[0])
        with self.assertRaises(ValidationError):
            Subscription(chat_id=1, base_weekday=0, base_hour=24, base_minute=0, timezone='UTC', language=LanguageCode.ENG, raw_subscription=self.raw_subs[0])

    def test_invalid_base_minute(self):
        with self.assertRaises(ValidationError):
            Subscription(chat_id=1, base_weekday=0, base_hour=0, base_minute=-1, timezone='UTC', language=LanguageCode.ENG, raw_subscription=self.raw_subs[0])
        with self.assertRaises(ValidationError):
            Subscription(chat_id=1, base_weekday=0, base_hour=0, base_minute=60, timezone='UTC', language=LanguageCode.ENG, raw_subscription=self.raw_subs[0])

    def test_overview(self):
        result = Subscription(chat_id=1, base_weekday=0, base_hour=1, base_minute=1, timezone='UTC', language=LanguageCode.ENG, raw_subscription=self.raw_subs[0]).overview(LanguageCode.ENG)
        expected = 'Monday, 01:01 (UTC)'
        self.assertEqual(result, expected)
        result = Subscription(chat_id=1, base_hour=13, base_minute=5, timezone='Europe/Moscow', language=LanguageCode.ENG, raw_subscription=self.raw_subs[0]).overview(LanguageCode.ENG)
        expected = '13:05 (Europe/Moscow)'
        self.assertEqual(result, expected)

    def test_valid_raw_subscriptions(self):
        for raw_sub in self.raw_subs:
            Subscription(chat_id=1, base_weekday=0, base_hour=0, base_minute=0, timezone='UTC', language=LanguageCode.ENG, raw_subscription=raw_sub)

    def test_from_raw_subscriptions(self):
        for raw_sub in self.raw_subs:
            Subscription.from_raw_subscription(raw_sub, 1, LanguageCode.ENG)

    def test_to_database_row(self):
        for raw_sub in self.raw_subs:
            result = Subscription(chat_id=1, base_weekday=0, base_hour=12, base_minute=30, timezone='UTC', language=LanguageCode.ENG, creation_ts=1, raw_subscription=raw_sub).to_database_row()
            expected = {'chat_id': 1, 'base_weekday': 0, 'base_hour': 12, 'base_minute': 30, 'timezone': 'UTC', 'language': 'ENG', 'creation_ts': 1, '_raw': raw_sub.model_dump_json()}
            self.assertEqual(result, expected)

    def test_from_database_row(self):
        for raw_sub in self.raw_subs:
            Subscription.from_database_row({'chat_id': 1, 'base_weekday': 0, 'base_hour': 12, 'base_minute': 30, 'timezone': 'UTC', 'language': 'ENG', 'creation_ts': 1, '_raw': raw_sub.model_dump_json()})

    def test_database_row_conversion_correctness(self):
        for raw_sub in self.raw_subs:
            expected = Subscription(chat_id=1, base_weekday=0, base_hour=12, base_minute=30, timezone='UTC', language=LanguageCode.ENG, creation_ts=1, raw_subscription=raw_sub)
            result = Subscription.from_database_row(expected.to_database_row())
            self.assertEqual(result, expected)
