def insert_after(chain, left, value, make_node):
    """Edit chain.head, chain.tail, and chain.size. Insert and return a new node.
    Use make_node(value), which returns a node with value, prev=None, next=None.
    left is an existing node in chain, or None only when chain is empty.
    Use O(1) time. Example: insert 4 after 2 in 2 <-> 8 yields 2 <-> 4 <-> 8."""
    raise NotImplementedError


def remove_node(chain, node):
    """Given chain and a known member node, unlink and detach it.
    Adjust head, tail, and size. Return its value. Use O(1) time.
    Example: remove the node 4 from 2 <-> 4 <-> 8 to get 2 <-> 8 and return 4."""
    raise NotImplementedError


def check_chain(head, tail, size):
    """Given head, tail, and a nonnegative size, return True for a valid chain.
    Visit the next links from head. Each prev must equal the node just visited by identity.
    Require exactly size nodes and require the last to be tail. Stop on cycles.
    Do not edit links. Example: 2 -> 8 with 8.prev=None gives False."""
    raise NotImplementedError
