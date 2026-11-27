import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class MakeStack(unittest.TestCase):
    def test_lifo(self):
        stack = practice.make_stack()
        other = practice.make_stack()
        self.assertIsNone(stack.pop())
        stack.push(0)
        self.assertEqual(stack.pop(), 0)
        stack.push(3)
        stack.push(3)
        stack.push(5)
        self.assertIsNone(other.pop())
        self.assertEqual([stack.pop(), stack.pop(), stack.pop(), stack.pop()], [5, 3, 3, None])


class MakeTwoStackQueue(unittest.TestCase):
    def test_fifo(self):
        queue = practice.make_two_stack_queue()
        other = practice.make_two_stack_queue()
        self.assertIsNone(queue.dequeue())
        queue.enqueue(0)
        self.assertEqual(queue.dequeue(), 0)
        queue.enqueue(4)
        queue.enqueue(8)
        self.assertEqual(queue.dequeue(), 4)
        queue.enqueue(8)
        queue.enqueue(2)
        self.assertEqual([queue.dequeue(), queue.dequeue(), queue.dequeue(), queue.dequeue()], [8, 8, 2, None])
        self.assertIsNone(other.dequeue())

    def test_two_stack_state(self):
        queue = practice.make_two_stack_queue()
        for value in [1, 2, 3]:
            queue.enqueue(value)
        self.assertEqual((queue.incoming, queue.outgoing), ([1, 2, 3], []))
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual((queue.incoming, queue.outgoing), ([], [3, 2]))
        queue.enqueue(4)
        self.assertEqual((queue.incoming, queue.outgoing), ([4], [3, 2]))
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual((queue.incoming, queue.outgoing), ([4], [3]))
        self.assertEqual([queue.dequeue(), queue.dequeue(), queue.dequeue()], [3, 4, None])

    def test_amortized_cost(self):
        class CountingList(list):
            moves = 0

            def append(self, value):
                CountingList.moves += 1
                super().append(value)

            def pop(self, *args):
                CountingList.moves += 1
                return super().pop(*args)

        queue = practice.make_two_stack_queue()
        queue.incoming = CountingList()
        queue.outgoing = CountingList()
        count = 400
        for value in range(count):
            queue.enqueue(value)
            if value % 3 == 0:
                self.assertEqual(queue.dequeue(), value // 3)
        taken = (count + 2) // 3
        for value in range(taken, count):
            self.assertEqual(queue.dequeue(), value)
        self.assertIsNone(queue.dequeue())
        self.assertLessEqual(CountingList.moves, 6 * count)

    def test_stack_access(self):
        import ast
        import inspect

        queue = practice.make_two_stack_queue()
        queue.enqueue(6)
        self.assertEqual(queue.dequeue(), 6)
        tree = ast.parse(inspect.getsource(practice.make_two_stack_queue))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                self.assertNotIn(node.module, {"queue", "collections"})
            if isinstance(node, ast.Import):
                self.assertTrue(all(alias.name not in {"queue", "collections"} for alias in node.names))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                self.assertNotEqual(node.func.attr, "insert")
                if node.func.attr == "pop" and node.args:
                    index = node.args[0]
                    if isinstance(index, ast.Constant):
                        self.assertNotEqual(index.value, 0, "Pop the stack end.")


class BracketsMatch(unittest.TestCase):
    def test_brackets(self):
        for text in ("", "([])[]", "()", "[[[]]]", "()()", "[()]", "[([])]", "([()])", "[](())[()]"):
            self.assertIs(practice.brackets_match(text), True, text)
        for text in ("([)]", "]", "(", "()[", "())", "(]", "[(])", "[(", "([(])"):
            self.assertIs(practice.brackets_match(text), False, text)


class MakeRingQueue(unittest.TestCase):
    def test_wrap_and_overflow(self):
        queue = practice.make_ring_queue(2)
        slots = queue.slots
        self.assertEqual(slots, [None, None])
        self.assertIsNone(queue.dequeue())
        self.assertIs(queue.enqueue(4), True)
        self.assertIs(queue.enqueue(8), True)
        self.assertIs(queue.enqueue(9), False)
        self.assertEqual(queue.dequeue(), 4)
        self.assertIs(queue.enqueue(9), True)
        self.assertEqual([queue.dequeue(), queue.dequeue(), queue.dequeue()], [8, 9, None])
        self.assertIs(queue.slots, slots)
        self.assertEqual(slots, [None, None])

    def test_capacity_one_and_duplicates(self):
        queue = practice.make_ring_queue(1)
        self.assertIs(queue.enqueue(0), True)
        self.assertIs(queue.enqueue(0), False)
        self.assertEqual(queue.dequeue(), 0)
        self.assertIs(queue.enqueue(0), True)
        self.assertEqual(queue.dequeue(), 0)
        self.assertIsNone(queue.dequeue())
