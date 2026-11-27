def chain_values(head):
    """Given a head or None, return a fresh list of values in forward order.
    Use value and next. Walk at most 100 integer nodes. Leave all links in place.
    Example: 4 -> 4 -> 0 -> None becomes [4, 4, 0]."""
    raise NotImplementedError


def first_match(head, target):
    """Return the first node whose value equals target, or None if absent.
    Use value and next. There are up to 100 integer nodes. Leave links unchanged.
    Example: in 2 -> 7 -> 7, searching for 7 returns the middle node itself."""
    raise NotImplementedError


def make_singly_linked_list():
    """Finish Node and SinglyLinkedList. Keep head, tail, and size.
    Values are integers. push_front and append insert in O(1).
    find returns the first matching node or None. remove deletes the first
    match and returns True, or False on a miss. to_list builds a fresh list.
    len reads size. Store data in nodes. The factory returns an empty list.
    Example: append(4), push_front(9), append(4), remove(4) leaves [9, 4]."""

    class Node:
        def __init__(self, value, next_node=None):
            raise NotImplementedError

    class SinglyLinkedList:
        def __init__(self):
            self.head = None
            self.tail = None
            self.size = 0

        def push_front(self, value):
            raise NotImplementedError

        def append(self, value):
            raise NotImplementedError

        def find(self, value):
            raise NotImplementedError

        def remove(self, value):
            raise NotImplementedError

        def to_list(self):
            raise NotImplementedError

        def __len__(self):
            raise NotImplementedError

    return SinglyLinkedList()
