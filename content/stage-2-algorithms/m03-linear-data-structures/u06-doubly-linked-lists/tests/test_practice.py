import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class InsertAfter(unittest.TestCase):
    def test_insert(self):
        from types import SimpleNamespace

        chain = SimpleNamespace(head=None, tail=None, size=0)

        def make_node(value):
            return SimpleNamespace(value=value, prev=None, next=None)

        first = practice.insert_after(chain, None, 2, make_node)
        self.assertIs(chain.head, first)
        self.assertIs(chain.tail, first)
        self.assertEqual(chain.size, 1)
        last = practice.insert_after(chain, first, 8, make_node)
        middle = practice.insert_after(chain, first, 8, make_node)
        self.assertIs(first.next, middle)
        self.assertIs(middle.next, last)
        self.assertIs(last.prev, middle)
        self.assertIs(middle.prev, first)
        self.assertIsNone(first.prev)
        self.assertIsNone(last.next)
        self.assertIs(chain.tail, last)
        self.assertEqual((chain.size, first.value, middle.value, last.value), (3, 2, 8, 8))


class RemoveNode(unittest.TestCase):
    def test_remove(self):
        from types import SimpleNamespace

        a = SimpleNamespace(value=2, prev=None)
        b = SimpleNamespace(value=4, prev=a)
        c = SimpleNamespace(value=4, prev=b, next=None)
        a.next = b
        b.next = c
        chain = SimpleNamespace(head=a, tail=c, size=3)
        self.assertEqual(practice.remove_node(chain, b), 4)
        self.assertIs(a.next, c)
        self.assertIs(c.prev, a)
        self.assertIsNone(b.next)
        self.assertIsNone(b.prev)
        self.assertEqual(chain.size, 2)
        self.assertEqual(practice.remove_node(chain, c), 4)
        self.assertIs(chain.tail, a)
        self.assertIsNone(a.next)
        self.assertEqual(practice.remove_node(chain, a), 2)
        self.assertIsNone(chain.head)
        self.assertIsNone(chain.tail)
        self.assertEqual(chain.size, 0)

    def test_remove_head_with_successor(self):
        from types import SimpleNamespace

        a = SimpleNamespace(value=6, prev=None)
        b = SimpleNamespace(value=7, prev=a, next=None)
        a.next = b
        chain = SimpleNamespace(head=a, tail=b, size=2)
        self.assertEqual(practice.remove_node(chain, a), 6)
        self.assertIs(chain.head, b)
        self.assertIsNone(b.prev)
        self.assertIsNone(a.next)


class CheckChain(unittest.TestCase):
    def test_valid(self):
        from types import SimpleNamespace

        self.assertIs(practice.check_chain(None, None, 0), True)
        first = SimpleNamespace(value=8, prev=None, next=None)
        self.assertIs(practice.check_chain(first, first, 1), True)
        last = SimpleNamespace(value=8, prev=first, next=None)
        first.next = last
        self.assertIs(practice.check_chain(first, last, 2), True)
        self.assertIs(first.next, last)
        self.assertIs(last.prev, first)

    def test_corrupt(self):
        from types import SimpleNamespace

        first = SimpleNamespace(value=8, prev=None, next=None)
        last = SimpleNamespace(value=8, prev=first, next=None)
        first.next = last
        self.assertIs(practice.check_chain(first, last, 0), False)
        self.assertIs(practice.check_chain(first, last, 3), False)
        self.assertIs(practice.check_chain(first, first, 2), False)
        self.assertIs(practice.check_chain(None, last, 0), False)
        last.next = first
        self.assertIs(practice.check_chain(first, last, 2), False)
        last.next = None
        last.prev = None
        self.assertIs(practice.check_chain(first, last, 2), False)
        self.assertIsNone(last.prev)
