import unittest
from pydantic import ValidationError
from src.apps.core.state import GLOBAL_STATE, Session


class TestSession(unittest.TestCase):

    def test_smoke(self):
        _ = Session(interface_language='RUS', quotes_language='ENG')

    def test_invalid_session(self):
        with self.assertRaises(ValidationError):
            Session()
        with self.assertRaises(ValidationError):
            Session(interface_language='123')
        with self.assertRaises(ValidationError):
            Session(quotes_language='123')

    def test_global_state_reservation(self):
        with self.assertRaises(Exception):
            GLOBAL_STATE['sessions'] = 'override sesssions'
