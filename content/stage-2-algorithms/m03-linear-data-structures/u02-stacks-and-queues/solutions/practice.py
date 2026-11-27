def make_stack():
    """Return a fresh empty stack object. Store integers in a Python list.
    push(value) adds at the end. pop() removes and returns the top or None when empty.
    Example: push(4), push(8), pop(), pop(), pop() returns 8, 4, None from the pops."""
    class Stack:
        def __init__(self):
            self.items = []

        def push(self, value):
            self.items.append(value)

        def pop(self):
            if self.items:
                return self.items.pop()
            return None

    return Stack()


def make_two_stack_queue():
    """Return a fresh empty FIFO queue. Use two Python lists as stacks.
    enqueue(value) pushes an integer. dequeue() returns the oldest value or None.
    Keep new values in the lists named incoming and outgoing. Use append and pop at the end.
    Move values from incoming to outgoing only when outgoing is empty.
    Example: enqueue(4), enqueue(8), dequeue(), enqueue(2), dequeue() removes 4 then 8."""
    class Queue:
        def __init__(self):
            self.incoming = []
            self.outgoing = []

        def enqueue(self, value):
            self.incoming.append(value)

        def dequeue(self):
            if not self.outgoing:
                while self.incoming:
                    self.outgoing.append(self.incoming.pop())
            if self.outgoing:
                return self.outgoing.pop()
            return None

    return Queue()


def brackets_match(text):
    """Text has only (, ), [, and ], with up to 1,000 characters.
    Return True if brackets match in order and every opener closes. Use one stack.
    Example: '([])[]' gives True. '([)]' gives False."""
    stack = []
    opener_for = {")": "(", "]": "["}
    for char in text:
        if char in "([":
            stack.append(char)
        else:
            if not stack or stack.pop() != opener_for[char]:
                return False
    return not stack


def make_ring_queue(capacity):
    """Capacity is 1 to 100. Store integers in a fixed list named slots.
    enqueue(value) returns True unless full. A full enqueue returns False and keeps all values.
    dequeue() returns None if empty. Otherwise return the oldest value and clear its slot to None.
    Use O(1) time per call. Example with capacity 2: enqueue(4), enqueue(8), dequeue(), enqueue(9)
    leaves 8 then 9 in FIFO order."""
    class RingQueue:
        def __init__(self):
            self.slots = [None] * capacity
            self.head = 0
            self.size = 0

        def enqueue(self, value):
            if self.size == capacity:
                return False
            index = (self.head + self.size) % capacity
            self.slots[index] = value
            self.size += 1
            return True

        def dequeue(self):
            if self.size == 0:
                return None
            value = self.slots[self.head]
            self.slots[self.head] = None
            self.head = (self.head + 1) % capacity
            self.size -= 1
            return value

    return RingQueue()
