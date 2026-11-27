import unittest
from datetime import timedelta

from app.fsrs import Grade, answer_grade, due_date, retrievability, update

from .support import TODAY


class FSRSTest(unittest.TestCase):
    def test_published_initial_stabilities_and_retention_identity(self):
        for grade, value in zip(Grade, [0.40255, 1.18385, 3.173, 15.69105], strict=True):
            with self.subTest(grade=grade):
                memory = update(None, grade, TODAY)
                self.assertEqual(memory.stability, value)
                self.assertAlmostEqual(retrievability(value, value), 0.9)
        self.assertAlmostEqual(update(None, Grade.AGAIN, TODAY).difficulty, 7.1949)
        self.assertEqual(due_date(update(None, Grade.AGAIN, TODAY)), TODAY + timedelta(days=1))
        self.assertEqual(due_date(update(None, Grade.GOOD, TODAY)), TODAY + timedelta(days=3))

    def test_fsrs5_equations_with_defaults_after_three_days(self):
        memory = update(None, Grade.GOOD, TODAY)
        self.assertAlmostEqual(memory.difficulty, 5.2824344223, places=8)
        for grade, stability, difficulty, interval in [
            (Grade.AGAIN, 1.0555610913, 6.7969325799, 1),
            (Grade.HARD, 4.9245118334, 6.0349502556, 5),
            (Grade.GOOD, 10.7389258461, 5.2729679313, 11),
            (Grade.EASY, 25.7936050948, 4.5109856070, 26),
        ]:
            with self.subTest(grade=grade):
                next_day = TODAY + timedelta(days=3)
                updated = update(memory, grade, next_day)
                self.assertAlmostEqual(updated.stability, stability, places=8)
                self.assertAlmostEqual(updated.difficulty, difficulty, places=8)
                self.assertEqual(due_date(updated), next_day + timedelta(days=interval))

    def test_same_day_and_hint_grades(self):
        memory = update(None, Grade.GOOD, TODAY)
        self.assertAlmostEqual(update(memory, Grade.GOOD, TODAY).stability, 4.4668580644)
        self.assertEqual(answer_grade(False, 0), Grade.AGAIN)
        self.assertEqual(answer_grade(True, 0), Grade.GOOD)
        self.assertEqual(answer_grade(True, 1), Grade.HARD)
        self.assertEqual(answer_grade(True, 2), Grade.AGAIN)
        self.assertEqual(answer_grade(True, 3), Grade.AGAIN)
