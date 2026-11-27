import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class MakeTotal(unittest.TestCase):
    def test_one(self):
        self.assertEqual(practice.make_total(3)(2), 5)

    def test_zero_and_repeat(self):
        add = practice.make_total(0)
        self.assertEqual([add(0), add(3), add(3), add(-7)], [0, 3, 6, -1])

    def test_separate(self):
        first, second = practice.make_total(3), practice.make_total(3)
        self.assertEqual(first(5), 8)
        self.assertEqual(second(-1), 2)
        self.assertEqual(first(0), 8)


class Timed(unittest.TestCase):
    def test_zero_args_and_name(self):
        readings = [4, 7]
        notes = []
        def health():
            return 'ok'
        wrapped = practice.timed(health, lambda: readings.pop(0), notes.append)
        self.assertEqual(wrapped(), 'ok')
        self.assertEqual(wrapped.__name__, 'health')
        self.assertEqual(notes, [3])

    def test_forwards_and_measures_each_call(self):
        ticks = [2, 2, 10, 16]
        events = []
        def clock():
            events.append('clock')
            return ticks.pop(0)
        def check(host, mode='fast'):
            events.append('check')
            return (host, mode)
        wrapped = practice.timed(check, clock, events.append)
        self.assertEqual(wrapped('db', mode='slow'), ('db', 'slow'))
        self.assertEqual(wrapped(host='api'), ('api', 'fast'))
        self.assertEqual(events, ['clock', 'check', 'clock', 0, 'clock', 'check', 'clock', 6])


class RetryWithLog(unittest.TestCase):
    def test_zero(self):
        events = []
        wrapped = practice.retry_with_log(lambda: events.append('called'), 0, events.append)
        self.assertIsNone(wrapped())
        self.assertEqual(events, [])

    def test_one_and_arguments(self):
        events = []
        def get(host, *, offset):
            events.append(host)
            return offset
        wrapped = practice.retry_with_log(get, 1, events.append)
        self.assertEqual(wrapped('db', offset=0), 0)
        self.assertEqual(wrapped.__name__, 'get')
        self.assertEqual(events, [1, 'db'])

    def test_stops_at_success(self):
        replies, notes = [None, 0, 7], []
        wrapped = practice.retry_with_log(lambda: replies.pop(0), 3, notes.append)
        self.assertEqual(wrapped(), 0)
        self.assertEqual(notes, [1, 2])
        self.assertEqual(replies, [7])

    def test_success_is_judged_by_identity_with_none(self):
        class EqualsNone:
            def __eq__(self, other):
                return other is None

            def __ne__(self, other):
                return other is not None

            __hash__ = None

        reply = EqualsNone()
        calls, notes = [], []
        def get():
            calls.append('call')
            return reply
        wrapped = practice.retry_with_log(get, 3, notes.append)
        self.assertIs(wrapped(), reply)
        self.assertEqual(notes, [1])
        self.assertEqual(calls, ['call'])

    def test_all_fail(self):
        notes = []
        wrapped = practice.retry_with_log(lambda: None, 3, notes.append)
        self.assertIsNone(wrapped())
        self.assertEqual(notes, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
