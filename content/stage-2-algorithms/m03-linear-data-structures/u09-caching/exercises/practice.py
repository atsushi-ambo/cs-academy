def memoize_count(compute):
    """compute is a function that takes one string key and returns an integer or None.
    Return a new function that calls compute only once per distinct key. Use your own dict.
    Each wrapper has its own cache. Example: if compute('empty') returns 0, two
    calls for 'empty' both return 0 and call compute just once."""
    raise NotImplementedError


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
            raise NotImplementedError

        def add_newest(self, node):
            raise NotImplementedError

        def get(self, key):
            raise NotImplementedError

        def put(self, key, value):
            raise NotImplementedError

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
            raise NotImplementedError

        def put(self, key, value):
            raise NotImplementedError

    return LRU()


def bounded_count(compute, capacity):
    """Return a fresh lru_cache wrapper around compute. Capacity is 0 to 100.
    compute accepts one positional string key. Call the wrapper like compute.
    Example with capacity 1: calling the wrapper with 'api', 'db', 'api' runs compute three times."""
    raise NotImplementedError
