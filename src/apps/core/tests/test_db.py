import unittest
import src.apps.core.db as db
from src.utils.testing import TelegramMockFactory


class TestDb(unittest.TestCase):

    def test_update_user_info(self):
        user = TelegramMockFactory.User(
            id=1,
            username='user',
            first_name='name',
            last_name=None,
        )
        db.update_user_info(user)
