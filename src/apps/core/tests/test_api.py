import src.apps.core.api as api
from src.apps.core.state import clear_state
from src.apps.core.types import LanguageCode
from src.utils.testing import MockTeleBotTestCase, TelegramMockFactory


class TestApi(MockTeleBotTestCase):

    def setUp(self):
        clear_state()
        super().setUp()

    def test_send_start_menu(self):
        api.send_start_menu(self.bot, 1, LanguageCode.ENG)
        api.send_start_menu(self.bot, 1, LanguageCode.RUS)

    def test_send_bad_interaction_reaction(self):
        api.send_bad_interaction_reaction(self.bot, 1, LanguageCode.ENG)
        api.send_bad_interaction_reaction(self.bot, 1, LanguageCode.RUS)

    def test_send_last_updates(self):
        api.send_last_updates(self.bot, 1, LanguageCode.ENG)
        api.send_last_updates(self.bot, 1, LanguageCode.RUS)

    def test_send_about(self):
        api.send_about(self.bot, 1, LanguageCode.ENG)
        api.send_about(self.bot, 1, LanguageCode.RUS)

    def test_send_easter_egg(self):
        api.send_easter_egg(self.bot, 1, LanguageCode.ENG)
        api.send_easter_egg(self.bot, 1, LanguageCode.RUS)

    def test_send_bad_message_reaction(self):
        mf = TelegramMockFactory
        api.send_bad_message_reaction(self.bot, mf.Message(chat=mf.Chat(1), from_user=mf.User('en')))
        api.send_bad_message_reaction(self.bot, mf.Message(chat=mf.Chat(1), from_user=mf.User('ru')))

    def send_bad_message_flooding_reaction(self):
        mf = TelegramMockFactory
        api.send_bad_message_flooding_reaction(self.bot, mf.Message(chat=mf.Chat(1), from_user=mf.User('en')))
        api.send_bad_message_flooding_reaction(self.bot, mf.Message(chat=mf.Chat(1), from_user=mf.User('ru')))
