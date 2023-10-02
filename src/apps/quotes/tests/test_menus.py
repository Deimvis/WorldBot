import unittest
import src.apps.quotes.menus as menus
from src.apps.core.types import LanguageCode


class TestBuildQuotesMenu(unittest.TestCase):

    def test_smoke(self):
        _ = menus.build_quotes_menu(LanguageCode.ENG)

    def test_simple(self):
        menus.build_quotes_menu(LanguageCode.ENG)
        menus.build_quotes_menu(LanguageCode.RUS)


class TestBuildSubscribingIntervalMenu(unittest.TestCase):

    def test_smoke(self):
        _ = menus.build_subscribing_interval_menu(LanguageCode.ENG)

    def test_simple(self):
        menus.build_subscribing_interval_menu(LanguageCode.ENG)
        menus.build_subscribing_interval_menu(LanguageCode.RUS)


class TestBuildSubscribingBaseWeekdayMenu(unittest.TestCase):

    def test_smoke(self):
        _ = menus.build_subscribing_base_weekday_menu(LanguageCode.ENG)

    def test_simple(self):
        menus.build_subscribing_base_weekday_menu(LanguageCode.ENG)
        menus.build_subscribing_base_weekday_menu(LanguageCode.RUS)


class TestBuildSubscribingTimezoneMenu(unittest.TestCase):

    def test_smoke(self):
        _ = menus.build_subscribing_timezone_menu(LanguageCode.ENG)

    def test_simple(self):
        menus.build_subscribing_timezone_menu(LanguageCode.ENG)
        menus.build_subscribing_timezone_menu(LanguageCode.RUS)


class TestBuildSubscribingBaseTimeMenu(unittest.TestCase):

    def test_smoke(self):
        _ = menus.build_subscribing_base_time_menu(LanguageCode.ENG)

    def test_simple(self):
        menus.build_subscribing_base_time_menu(LanguageCode.ENG)
        menus.build_subscribing_base_time_menu(LanguageCode.RUS)


class TestBuildManageSubscriptionsMenu(unittest.TestCase):

    def test_smoke(self):
        _ = menus.build_manage_subscriptions_menu(LanguageCode.ENG)

    def test_simple(self):
        menus.build_manage_subscriptions_menu(LanguageCode.ENG)
        menus.build_manage_subscriptions_menu(LanguageCode.RUS)


class TestBuildRemoveSubscriptionMenu(unittest.TestCase):

    def test_smoke(self):
        _ = menus.build_remove_subscription_menu([1, 2, 3], LanguageCode.ENG)

    def test_simple(self):
        menus.build_remove_subscription_menu([1, 2, 3], LanguageCode.ENG)
        menus.build_remove_subscription_menu([1, 2, 3, 4, 5], LanguageCode.RUS)
        menus.build_remove_subscription_menu([], LanguageCode.RUS)
