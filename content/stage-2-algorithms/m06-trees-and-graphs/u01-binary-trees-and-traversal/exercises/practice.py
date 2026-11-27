def make_node(value, left=None, right=None):
    """
    Complete the Node class inside make_node. Return one new node with the given value
    and child links. Omitted links are None. For example, make_node("api",
    make_node("db")).left.value is "db".
    """
    class Node:
        def __init__(self, value, left, right):
            raise NotImplementedError

    return Node(value, left, right)


def preorder(root):
    """
    Return a new list of values in preorder. Use recursion. A missing link is None. Keep
    the .value, .left, and .right attributes unchanged. preorder(Node(4, Node(9),
    Node(2))) returns [4, 9, 2].
    """
    raise NotImplementedError


def inorder(root):
    """
    Return a new list of values in inorder. Use recursion. A missing link is None. Keep
    the .value, .left, and .right attributes unchanged. inorder(Node(4, Node(9),
    Node(2))) returns [9, 4, 2].
    """
    raise NotImplementedError


def postorder(root):
    """
    Return a new list of values in postorder. Use recursion. A missing link is None. Keep
    the .value, .left, and .right attributes unchanged. postorder(Node(4, Node(9),
    Node(2))) returns [9, 2, 4].
    """
    raise NotImplementedError


def level_order(root):
    """
    Use a first-in, first-out queue. Return a new list in level order. Leave all node
    links as they are. For Node(4, Node(9, Node(1)), Node(2)), return [4, 9, 2, 1]. For
    None, return [].
    """
    raise NotImplementedError


def tree_stats(root):
    """
    Return (height, leaves) in one recursive traversal of Node objects. Height counts
    nodes. Keep links unchanged. For Node(1, Node(2), None), return (2, 1). For None,
    return (0, 0).
    """
    raise NotImplementedError
