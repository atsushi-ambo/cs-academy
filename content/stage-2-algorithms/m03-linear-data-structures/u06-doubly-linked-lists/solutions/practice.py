def insert_after(chain, left, value, make_node):
    """Edit chain.head, chain.tail, and chain.size. Insert and return a new node.
    Use make_node(value), which returns a node with value, prev=None, next=None.
    left is an existing node in chain, or None only when chain is empty.
    Use O(1) time. Example: insert 4 after 2 in 2 <-> 8 yields 2 <-> 4 <-> 8."""
    node = make_node(value)
    if left is None:
        chain.head = node
        chain.tail = node
    else:
        right = left.next
        node.prev = left
        node.next = right
        left.next = node
        if right is None:
            chain.tail = node
        else:
            right.prev = node
    chain.size += 1
    return node


def remove_node(chain, node):
    """Given chain and a known member node, unlink and detach it.
    Adjust head, tail, and size. Return its value. Use O(1) time.
    Example: remove the node 4 from 2 <-> 4 <-> 8 to get 2 <-> 8 and return 4."""
    left = node.prev
    right = node.next
    if left is None:
        chain.head = right
    else:
        left.next = right
    if right is None:
        chain.tail = left
    else:
        right.prev = left
    node.prev = None
    node.next = None
    chain.size -= 1
    return node.value


def check_chain(head, tail, size):
    """Given head, tail, and a nonnegative size, return True for a valid chain.
    Visit the next links from head. Each prev must equal the node just visited by identity.
    Require exactly size nodes and require the last to be tail. Stop on cycles.
    Do not edit links. Example: 2 -> 8 with 8.prev=None gives False."""
    previous = None
    current = head
    count = 0
    while current is not None:
        if count == size or current.prev is not previous:
            return False
        previous = current
        current = current.next
        count += 1
    return count == size and previous is tail
