import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class ChainValues(unittest.TestCase):
    def test_walk(self):
        from types import SimpleNamespace

        tail = SimpleNamespace(value=0, next=None)
        middle = SimpleNamespace(value=4, next=tail)
        head = SimpleNamespace(value=4, next=middle)
        self.assertEqual(practice.chain_values(None), [])
        self.assertEqual(practice.chain_values(tail), [0])
        self.assertEqual(practice.chain_values(head), [4, 4, 0])
        self.assertIs(head.next, middle)
        self.assertIs(middle.next, tail)
        self.assertIsNone(tail.next)


class FirstMatch(unittest.TestCase):
    def test_first_match(self):
        from types import SimpleNamespace

        last = SimpleNamespace(value=7, next=None)
        middle = SimpleNamespace(value=7, next=last)
        head = SimpleNamespace(value=2, next=middle)
        self.assertIsNone(practice.first_match(None, 7))
        self.assertIs(practice.first_match(head, 7), middle)
        self.assertIs(practice.first_match(last, 7), last)
        self.assertIsNone(practice.first_match(head, 9))
        self.assertIs(head.next, middle)
        self.assertIs(middle.next, last)


class MakeSinglyLinkedList(unittest.TestCase):
    def test_edits_and_links(self):
        chain = practice.make_singly_linked_list()
        other = practice.make_singly_linked_list()
        self.assertEqual((len(chain), chain.to_list()), (0, []))
        self.assertIsNone(chain.head)
        self.assertIsNone(chain.tail)
        self.assertIsNone(chain.find(0))
        self.assertIs(chain.remove(0), False)
        chain.push_front(4)
        first_four = chain.head
        self.assertIs(chain.tail, first_four)
        chain.push_front(9)
        chain.append(4)
        last_four = chain.tail
        self.assertIs(chain.head.next, first_four)
        self.assertIs(first_four.next, last_four)
        self.assertIsNone(last_four.next)
        self.assertIs(chain.find(4), first_four)
        self.assertEqual(len(chain), 3)
        self.assertIs(chain.remove(4), True)
        self.assertIs(chain.head.next, last_four)
        snapshot = chain.to_list()
        self.assertEqual(snapshot, [9, 4])
        snapshot.append(0)
        self.assertEqual(chain.to_list(), [9, 4])
        self.assertIs(chain.remove(4), True)
        self.assertIs(chain.tail, chain.head)
        self.assertIs(chain.remove(9), True)
        self.assertIsNone(chain.head)
        self.assertIsNone(chain.tail)
        self.assertEqual(len(chain), 0)
        chain.append(0)
        self.assertIs(chain.head, chain.tail)
        self.assertEqual((len(chain), chain.to_list()), (1, [0]))
        self.assertEqual((len(other), other.to_list()), (0, []))
