import src.apps.quotes.api as api
from unittest.mock import patch
from src.apps.core.state import clear_state
from src.apps.core.types import LanguageCode
from src.apps.quotes.state import SubscriptionBuilder
from src.apps.quotes.types import RawSubscription, Subscription
from src.utils.testing import MockTeleBotTestCase


class TestApi(MockTeleBotTestCase):

    def setUp(self):
        self.dummy_raw_sub = RawSubscription(interval='EVERY_DAY', timezone='UTC', base_time='12:00')
        self.dummy_sub = Subscription(chat_id=1, base_hour=12, base_minute=0,
                          timezone='UTC', language=LanguageCode.ENG, creation_ts=0,
                          raw_subscription=self.dummy_raw_sub)
        clear_state()
        super().setUp()

    def test_send_quote(self):
        api.send_quote(self.bot, 1, LanguageCode.ENG)
        api.send_quote(self.bot, 1, LanguageCode.RUS)

    def test_send_quotes_menu(self):
        api.send_quotes_menu(self.bot, 1, LanguageCode.ENG)
        api.send_quotes_menu(self.bot, 1, LanguageCode.RUS)

    def test_subscribe(self):
        api.subscribe(self.bot, 1, LanguageCode.ENG)
        api.subscribe(self.bot, 1, LanguageCode.RUS)

    def test_send_subscribing_interval_step(self):
        api.send_subscribing_interval_step(self.bot, 1, LanguageCode.ENG)
        api.send_subscribing_interval_step(self.bot, 1, LanguageCode.RUS)

    def test_handle_subscribing_interval_step(self):
        api.handle_subscribing_interval_step(self.bot, 1, 2, 'subscribing/interval_menu/EVERY_DAY', LanguageCode.ENG)
        api.handle_subscribing_interval_step(self.bot, 1, 2, 'subscribing/interval_menu/EVERY_DAY', LanguageCode.RUS)
        api.handle_subscribing_interval_step(self.bot, 1, 2, 'subscribing/interval_menu/EVERY_WEEK', LanguageCode.ENG)
        api.handle_subscribing_interval_step(self.bot, 1, 2, 'subscribing/interval_menu/EVERY_WEEK', LanguageCode.RUS)

    def test_send_subscribing_base_weekday_step(self):
        api.send_subscribing_base_weekday_step(self.bot, 1, 2, LanguageCode.ENG)
        api.send_subscribing_base_weekday_step(self.bot, 1, 2, LanguageCode.RUS)

    def test_handle_subscribing_base_weekday_step(self):
        api.handle_subscribing_base_weekday_step(self.bot, 1, 2, 'subscribing/base_weekday_menu/MONDAY', LanguageCode.ENG)
        api.handle_subscribing_base_weekday_step(self.bot, 1, 2, 'subscribing/base_weekday_menu/MONDAY', LanguageCode.RUS)

    def test_send_subscribing_timezone_step(self):
        api.send_subscribing_timezone_step(self.bot, 1, 2, LanguageCode.ENG)
        api.send_subscribing_timezone_step(self.bot, 1, 2, LanguageCode.RUS)

    def test_handle_subscribing_timezone_step(self):
        api.handle_subscribing_timezone_step(self.bot, 1, 2, 'subscribing/timezone_menu/UTC', LanguageCode.ENG)
        api.handle_subscribing_timezone_step(self.bot, 1, 2, 'subscribing/timezone_menu/UTC', LanguageCode.RUS)
        api.handle_subscribing_timezone_step(self.bot, 1, 2, 'subscribing/timezone_menu/Europe%Moscow', LanguageCode.ENG)
        api.handle_subscribing_timezone_step(self.bot, 1, 2, 'subscribing/timezone_menu/Europe%Moscow', LanguageCode.RUS)

    def test_send_subscribing_custom_timezone_step(self):
        api.send_subscribing_custom_timezone_step(self.bot, 1, 2, LanguageCode.ENG)
        api.send_subscribing_custom_timezone_step(self.bot, 1, 2, LanguageCode.RUS)

    def test_send_subscribing_base_time_step(self):
        api.send_subscribing_base_time_step(self.bot, 1, 2, LanguageCode.ENG)
        api.send_subscribing_base_time_step(self.bot, 1, 2, LanguageCode.RUS)

    def test_handle_subscribing_base_time_step(self):
        api.handle_subscribing_base_time_step(self.bot, 1, 2, 'subscribing/base_time_menu/10:00', LanguageCode.ENG)
        api.handle_subscribing_base_time_step(self.bot, 1, 2, 'subscribing/base_time_menu/10:00', LanguageCode.RUS)

    def test_send_subscribing_custom_base_time_step(self):
        api.send_subscribing_custom_base_time_step(self.bot, 1, 2, LanguageCode.ENG)
        api.send_subscribing_custom_base_time_step(self.bot, 1, 2, LanguageCode.RUS)

    def test_create_subscription(self):
        with patch.object(SubscriptionBuilder, 'create_subscription') as create_subscription_mock:
            create_subscription_mock.return_value = self.dummy_sub
            api.create_subscription(self.bot, 1, 2, LanguageCode.ENG)
            api.create_subscription(self.bot, 1, 2, LanguageCode.RUS)

    def test_cancel_subscribing(self):
        api.cancel_subscribing(self.bot, 1, 2, LanguageCode.ENG)
        api.cancel_subscribing(self.bot, 1, 2, LanguageCode.RUS)

    def test_send_manage_subscriptions_menu(self):
        api.send_manage_subscriptions_menu(self.bot, 1, LanguageCode.ENG)
        api.send_manage_subscriptions_menu(self.bot, 1, LanguageCode.RUS)

    def test_send_remove_subscription_menu(self):
        api.send_remove_subscription_menu(self.bot, 1, 2, LanguageCode.ENG)
        api.send_remove_subscription_menu(self.bot, 1, 2, LanguageCode.RUS)

    def test_remove_subscription(self):
        api.remove_subscription(self.bot, 1, 2, 'managing_subscriptions/remove_menu/1', LanguageCode.ENG)
        api.remove_subscription(self.bot, 1, 2, 'managing_subscriptions/remove_menu/1', LanguageCode.RUS)

    def test_return_to_manage_subscriptions_menu(self):
        api.return_to_manage_subscriptions_menu(self.bot, 1, 2, LanguageCode.ENG)
        api.return_to_manage_subscriptions_menu(self.bot, 1, 2, LanguageCode.RUS)
