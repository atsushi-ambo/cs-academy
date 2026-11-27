def make_deque(capacity):
    """Capacity is 1 to 100. Keep a fixed list named slots and store integers.
    push_left and push_right return True on success or False if full.
    pop_left and pop_right return the item or None if empty. Clear each removed slot to None.
    Use O(1) time per call. Build it from the ring. Do not use collections.deque.
    Example: push_left(4), push_right(8), pop_right(), pop_left() removes 8 then 4."""
    class RingDeque:
        def __init__(self):
            self.slots = [None] * capacity
            self.head = 0
            self.size = 0

        def push_left(self, value):
            raise NotImplementedError

        def push_right(self, value):
            raise NotImplementedError

        def pop_left(self):
            raise NotImplementedError

        def pop_right(self):
            raise NotImplementedError

    return RingDeque()


def offer_index(values, candidates, i):
    """candidates is a deque of indexes in arrival order and decreasing value order.
    i is a new, later index of values. Pop older candidates with value <= values[i] from the right.
    Append i. Leave values unchanged. Example: [0, 1] for [9, 4, 7], with i=2, becomes [0, 2]."""
    raise NotImplementedError


def window_maxima(values, k):
    """Return a fresh list of maxima for windows of width k. Values are integers.
    If k < 1 or k > len(values), return []. Leave values unchanged.
    Use a deque of candidate indexes and one pass. Do not scan each window.
    Example: window_maxima([9, 4, 7, 7], 2) gives [9, 7, 7]."""
    raise NotImplementedError
