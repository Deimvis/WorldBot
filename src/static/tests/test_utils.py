import unittest
import src.static.utils as utils


class TestDictBaseModel(unittest.TestCase):
    class Dummy(utils.DictBaseModel):
        a: int
        b: str

    def test_smoke(self):
        _ = self.Dummy(a=1, b='b')

    def test_simple(self):
        d = self.Dummy(a=1, b='b')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'b')
        self.assertEqual(d.a, d['a'])
        self.assertEqual(d.b, d['b'])
