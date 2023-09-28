import random
import string
import unittest
from src.utils.state import StateNode


class TestStateNode(unittest.TestCase):

    def test_smoke(self):
        node = StateNode()
        node['key'] = 'value'

    def test_infinite_recursion(self):
        node = StateNode()
        for _ in range(10001):
            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(0, 100)))
            node = node[key]
            self.assertEqual(node.__class__, StateNode)

    def test_assignment(self):
        node = StateNode()
        node['key'] = 'value'
        self.assertEqual(node['key'], 'value')

    def test_freezing(self):
        node = StateNode()
        node.freeze_key('aaa')
        with self.assertRaises(AssertionError):
            node['aaa'] = 'value'

        node['bbb'] = 'value'
        node.freeze_key('bbb')
        with self.assertRaises(AssertionError):
            node['bbb'] = 'new_value'
