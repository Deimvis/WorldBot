from collections import defaultdict
from typing import Any, Callable
from src.apps.core.types import LanguageCode
from src.apps.core.state import GLOBAL_STATE
from src.apps.quotes.types import Subscription, RawSubscription


class SubscriptionBuilder:
    def __init__(self):
        self.raw_subscription = RawSubscription()

    def set_interval(self, interval: str, fallback: Callable[[], Any]):
        try:
            self.raw_subscription.interval = interval
        except:  # noqa
            fallback()
            raise

    def set_base_weekday(self, base_weekday: str, fallback: Callable[[], Any]):
        try:
            self.raw_subscription.base_weekday = base_weekday
        except:  # noqa
            fallback()
            raise

    def set_timezone(self, timezone: str, fallback: Callable[[], Any]):
        try:
            self.raw_subscription.timezone = timezone
        except:  # noqa
            fallback()
            raise

    def set_base_time(self, base_time: str, fallback: Callable[[], Any]):
        try:
            self.raw_subscription.base_time = base_time
        except:  # noqa
            fallback()
            raise

    def create_subscription(self, chat_id: int, language: LanguageCode, fallback: Callable[[], Any]) -> Subscription:
        try:
            return Subscription.from_raw_subscription(self.raw_subscription, chat_id, language)
        except:  # noqa
            fallback()
            raise

    def clear(self):
        self.raw_subscription = RawSubscription()


GLOBAL_STATE['quotes_subscription_builders'] = defaultdict(SubscriptionBuilder)
GLOBAL_STATE.freeze_key('quotes_subscription_builders')
