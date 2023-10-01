import unittest
from pydantic import ValidationError
from src.apps.core.types import LanguageCode
from src.static.messages import PlainMessage, ProbabilisticMessage, RandomMessage, MESSAGES_DATA


class TestPlainMessage(unittest.TestCase):

    def test_smoke(self):
        _ = PlainMessage('abc')

    def test_resolve(self):
        self.assertEqual(PlainMessage('abc').resolve(), 'abc')
        self.assertEqual(PlainMessage('123').resolve(), '123')
        self.assertEqual(PlainMessage('').resolve(), '')


class TestRandomMessage(unittest.TestCase):

    def test_smoke(self):
        _ = RandomMessage(['a', 'b', 'c'])

    def test_resolve(self):
        for _ in range(10):
            self.assertIn(RandomMessage(['a', 'b', 'c']).resolve(), ['a', 'b', 'c'])
        self.assertEqual(RandomMessage(['a']).resolve(), 'a')


class TestProbabilisticMessage(unittest.TestCase):

    def test_smoke(self):
        msg = ProbabilisticMessage(type='probabilistic', options=[(0.5, 'a'), (0.5, 'b')])
        msg.resolve()

    def test_invalid_probability(self):
        with self.assertRaises(ValidationError):
            ProbabilisticMessage(type='probabilistic', options=[(0.1, 'a')])
        with self.assertRaises(ValidationError):
            ProbabilisticMessage(type='probabilistic', options=[(1.1, 'a')])
        with self.assertRaises(ValidationError):
            ProbabilisticMessage(type='probabilistic', options=[(0.1, 'a'), (0.1, 'b'), (0.1, 'c')])

    def test_valid_probability(self):
        ProbabilisticMessage(type='probabilistic', options=[(1.0, 'a')])
        ProbabilisticMessage(type='probabilistic', options=[(1, 'a')])
        ProbabilisticMessage(type='probabilistic', options=[(0.5, 'a'), (0.5, 'b')])


class TestMessagesData(unittest.TestCase):

    def test_smoke(self):
        _ = MESSAGES_DATA

    def test_languages(self):
        supported_languages = set(language.name for language in LanguageCode)
        menus_languages = set(MESSAGES_DATA.keys())
        self.assertEqual(supported_languages, menus_languages)

    def test_getitem(self):
        _ = MESSAGES_DATA['ENG']['start']
