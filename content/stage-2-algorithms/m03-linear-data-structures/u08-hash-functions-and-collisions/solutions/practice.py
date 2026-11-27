def string_slot(key, capacity):
    """key is a string of up to 32 characters. Capacity is positive and at most 1,024.
    Start h at zero. For each ch, update h to (31 * h + ord(ch)) % capacity.
    Return h. Do not use hash(). Example: string_slot('ab', 7) gives 4."""
    h = 0
    for char in key:
        h = (31 * h + ord(char)) % capacity
    return h


def make_chained_map(capacity):
    """Start with 1 to 16 buckets. Use independent lists of (string key, integer value) pairs.
    Use the supplied slot helper. Keys are up to 32 characters. Store at most 100 keys.
    get returns the value or None. put adds or replaces a key. Track size.
    Before adding past capacity, double the buckets and rehash. Use your own buckets, no dict.
    Example from capacity 2: put('a', 4), put('c', 7), put('e', 9) makes four buckets.
    get('c') gives 7 even after the resize."""
    def slot(key, count):
        index = 0
        for char in key:
            index = (31 * index + ord(char)) % count
        return index

    def empty_buckets(count):
        buckets = []
        for i in range(count):
            buckets.append([])
        return buckets

    class ChainedMap:
        def __init__(self):
            self.buckets = empty_buckets(capacity)
            self.size = 0

        def get(self, key):
            index = slot(key, len(self.buckets))
            for saved, value in self.buckets[index]:
                if saved == key:
                    return value
            return None

        def resize(self):
            new_buckets = empty_buckets(2 * len(self.buckets))
            for bucket in self.buckets:
                for key, value in bucket:
                    index = slot(key, len(new_buckets))
                    new_buckets[index].append((key, value))
            self.buckets = new_buckets

        def put(self, key, value):
            index = slot(key, len(self.buckets))
            bucket = self.buckets[index]
            for i in range(len(bucket)):
                if bucket[i][0] == key:
                    bucket[i] = (key, value)
                    return
            if self.size == len(self.buckets):
                self.resize()
                index = slot(key, len(self.buckets))
            self.buckets[index].append((key, value))
            self.size += 1

    return ChainedMap()


def make_probing_map(capacity):
    """Capacity is 1 to 100. Keep slots fixed. Use the supplied slot helper.
    Store string keys of up to 32 characters and integer values in pairs. No dict or deletes.
    get returns the value or None. put returns True on insert or replacement.
    A full table rejects a new key with False. Probe at most capacity slots.
    Example: at capacity 4, 'c' starts at slot 3. After 'c', inserting 'g' uses slot 0."""
    def slot(key):
        index = 0
        for char in key:
            index = (31 * index + ord(char)) % capacity
        return index

    class ProbingMap:
        def __init__(self):
            self.slots = [None] * capacity

        def get(self, key):
            index = slot(key)
            for step in range(capacity):
                pair = self.slots[index]
                if pair is None:
                    return None
                if pair[0] == key:
                    return pair[1]
                index = (index + 1) % capacity
            return None

        def put(self, key, value):
            index = slot(key)
            for step in range(capacity):
                pair = self.slots[index]
                if pair is None or pair[0] == key:
                    self.slots[index] = (key, value)
                    return True
                index = (index + 1) % capacity
            return False

    return ProbingMap()
