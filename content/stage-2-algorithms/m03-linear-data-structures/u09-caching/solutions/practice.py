def memoize_count(compute):
    """compute is a function that takes one string key and returns an integer or None.
    Return a new function that calls compute only once per distinct key. Use your own dict.
    Each wrapper has its own cache. Example: if compute('empty') returns 0, two
    calls for 'empty' both return 0 and call compute just once."""
    memo = {}

    def get(key):
        if key not in memo:
            memo[key] = compute(key)
        return memo[key]

    return get


def make_lru(capacity):
    """Capacity is 0 to 100. Keys are strings and values are integers.
    get returns a value or None and moves a hit to newest. put adds or updates and
    makes the entry newest. Evict the oldest on a new write to a full cache.
    At capacity zero, store nothing. Use nodes (dict), head (oldest), and tail (newest).
    Use your own nodes with key, value, prev, and next. Do not use library caches.
    Example: with capacity 2, put('api', 4), put('db', 8), get('api'), put('web', 2)
    evicts db and leaves api at head and web at tail."""
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    class LRU:
        def __init__(self):
            self.nodes = {}
            self.head = None
            self.tail = None

        def detach(self, node):
            left = node.prev
            right = node.next
            if left is None:
                self.head = right
            else:
                left.next = right
            if right is None:
                self.tail = left
            else:
                right.prev = left
            node.prev = None
            node.next = None

        def add_newest(self, node):
            node.prev = self.tail
            node.next = None
            if self.tail is None:
                self.head = node
            else:
                self.tail.next = node
            self.tail = node

        def get(self, key):
            if key not in self.nodes:
                return None
            node = self.nodes[key]
            self.detach(node)
            self.add_newest(node)
            return node.value

        def put(self, key, value):
            if capacity == 0:
                return
            if key in self.nodes:
                node = self.nodes[key]
                node.value = value
                self.detach(node)
            else:
                if len(self.nodes) == capacity:
                    old = self.head
                    self.detach(old)
                    del self.nodes[old.key]
                node = Node(key, value)
                self.nodes[key] = node
            self.add_newest(node)

    return LRU()


def make_ordered_lru(capacity):
    """Use OrderedDict. Capacity is 0 to 100, keys are strings, and values are integers.
    As before, get returns None on a miss. Hits, inserts, and updates make a key newest.
    Example with capacity 1: put('api', 4), put('db', 8), then get('api') gives None."""
    from collections import OrderedDict

    class LRU:
        def __init__(self):
            self.saved = OrderedDict()

        def get(self, key):
            if key not in self.saved:
                return None
            self.saved.move_to_end(key)
            return self.saved[key]

        def put(self, key, value):
            self.saved[key] = value
            self.saved.move_to_end(key)
            if len(self.saved) > capacity:
                self.saved.popitem(last=False)

    return LRU()


def bounded_count(compute, capacity):
    """Return a fresh lru_cache wrapper around compute. Capacity is 0 to 100.
    compute accepts one positional string key. Call the wrapper like compute.
    Example with capacity 1: calling the wrapper with 'api', 'db', 'api' runs compute three times."""
    from functools import lru_cache

    return lru_cache(maxsize=capacity)(compute)
