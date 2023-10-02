import datetime
from copy import deepcopy
from unittest.mock import patch
from src.apps.core.types import LanguageCode
from src.apps.quotes.notifier import QuoteNotifier
from src.apps.quotes.types import RawSubscription, Subscription
from src.utils.testing import MockTeleBotTestCase


class TestQuotesNotifier(MockTeleBotTestCase):

    def setUp(self):
        super().setUp()
        self.notifier = QuoteNotifier(self.bot)
        self.dummy_raw_sub = RawSubscription(interval='EVERY_DAY', timezone='UTC', base_time='12:00')

    def test_is_right_time(self):
        original_dt = deepcopy(datetime.datetime)
        make_dt = lambda *args, **kwargs: original_dt(*args, **kwargs)
        with patch('datetime.datetime') as mock_datetime:
            # NOTE: Monday-Sunday: 0-6
            tests = [
                (self._create_Subscription(base_hour=12, base_minute=0), [
                    [make_dt(year=2000, month=1, day=1, hour=12, minute=0, second=0), True],
                    [make_dt(year=2000, month=1, day=2, hour=12, minute=0, second=0), True],
                    [make_dt(year=2000, month=1, day=1, hour=12, minute=1, second=0), False],
                ]),
                (self._create_Subscription(base_weekday=0, base_hour=12, base_minute=0), [  # TARGET=MONDAY
                    [make_dt(year=2000, month=1, day=1, hour=12, minute=0, second=0), False],  # Saturday
                    [make_dt(year=2000, month=1, day=3, hour=12, minute=0, second=0), True],   # Monday
                    [make_dt(year=2000, month=1, day=3, hour=12, minute=1, second=0), False],   # Monday
                ]),
            ]
            for subscription, context in tests:
                for mock_dt, expected_result in context:
                    mock_datetime.now.return_value = mock_dt
                    self.assertEqual(self.notifier.is_right_time(subscription), expected_result)

    def test_send(self):
        self.notifier.send(self._create_Subscription(base_hour=12, base_minute=0))
        self.notifier.send(self._create_Subscription(base_weekday=0, base_hour=12, base_minute=0))

    def _create_Subscription(self, *, base_weekday: int = None, base_hour: int, base_minute: int):
        return Subscription(chat_id=1, base_weekday=base_weekday, base_hour=base_hour, base_minute=base_minute, timezone='UTC',
                            language=LanguageCode.ENG, creation_ts=0, raw_subscription=self.dummy_raw_sub)
