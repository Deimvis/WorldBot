import unittest
import src.apps.quotes.shortcuts as shortcuts
from src.apps.quotes.state import SubscriptionBuilder


class TestGetSubscriptionBuilder(unittest.TestCase):

    def test_smoke(self):
        shortcuts.get_subscription_builder(1)

    def test_simple(self):
        shortcuts.get_subscription_builder(1)
        shortcuts.get_subscription_builder(2)
        shortcuts.get_subscription_builder(10)
        shortcuts.get_subscription_builder(999999)

    def test_correct_type(self):
        self.assertIsInstance(shortcuts.get_subscription_builder(1), SubscriptionBuilder)
        self.assertIsInstance(shortcuts.get_subscription_builder(2), SubscriptionBuilder)
        self.assertIsInstance(shortcuts.get_subscription_builder(10), SubscriptionBuilder)
        self.assertIsInstance(shortcuts.get_subscription_builder(999999), SubscriptionBuilder)
