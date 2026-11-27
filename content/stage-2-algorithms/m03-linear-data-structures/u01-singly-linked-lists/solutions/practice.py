def chain_values(head):
    """Given a head or None, return a fresh list of values in forward order.
    Use value and next. Walk at most 100 integer nodes. Leave all links in place.
    Example: 4 -> 4 -> 0 -> None becomes [4, 4, 0]."""
    values = []
    while head is not None:
        values.append(head.value)
        head = head.next
    return values


def first_match(head, target):
    """Return the first node whose value equals target, or None if absent.
    Use value and next. There are up to 100 integer nodes. Leave links unchanged.
    Example: in 2 -> 7 -> 7, searching for 7 returns the middle node itself."""
    while head is not None:
        if head.value == target:
            return head
        head = head.next
    return None


def make_singly_linked_list():
    """Finish Node and SinglyLinkedList. Keep head, tail, and size.
    Values are integers. push_front and append insert in O(1).
    find returns the first matching node or None. remove deletes the first
    match and returns True, or False on a miss. to_list builds a fresh list.
    len reads size. Store data in nodes. The factory returns an empty list.
    Example: append(4), push_front(9), append(4), remove(4) leaves [9, 4]."""
    class Node:
        def __init__(self, value, next_node=None):
            self.value = value
            self.next = next_node

    class SinglyLinkedList:
        def __init__(self):
            self.head = None
            self.tail = None
            self.size = 0

        def push_front(self, value):
            self.head = Node(value, self.head)
            if self.tail is None:
                self.tail = self.head
            self.size += 1

        def append(self, value):
            node = Node(value)
            if self.tail is None:
                self.head = node
            else:
                self.tail.next = node
            self.tail = node
            self.size += 1

        def find(self, value):
            current = self.head
            while current is not None:
                if current.value == value:
                    return current
                current = current.next
            return None

        def remove(self, value):
            previous = None
            current = self.head
            while current is not None:
                if current.value == value:
                    if previous is None:
                        self.head = current.next
                    else:
                        previous.next = current.next
                    if current is self.tail:
                        self.tail = previous
                    self.size -= 1
                    return True
                previous = current
                current = current.next
            return False

        def to_list(self):
            values = []
            current = self.head
            while current is not None:
                values.append(current.value)
                current = current.next
            return values

        def __len__(self):
            return self.size

    return SinglyLinkedList()
