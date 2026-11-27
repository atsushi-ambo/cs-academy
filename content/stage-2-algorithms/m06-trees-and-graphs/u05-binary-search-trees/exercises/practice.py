def search(root, key):
    """
    Return True if the integer key exists in the BST, or False otherwise. Follow only one
    branch per comparison. Do not change the tree. For Node(8, Node(4)), search(root, 4)
    is True and search(root, 5) is False.
    """
    raise NotImplementedError


def insert(root, key, make_node):
    """
    Insert an integer key into the BST and return its root. Use make_node(key) to make a
    leaf. Keep only one copy of each key. For insert(None, 8, Node), return a node with
    key 8. Adding 4 to that root sets its left link.
    """
    raise NotImplementedError


def delete(root, key):
    """
    Delete an integer key from a strict BST and return the new root. Use the successor
    for two children, and preserve its right child. Deleting 8 from Node(8, Node(4),
    Node(11)) returns a root with key 11 and left key 4.
    """
    raise NotImplementedError


def is_bst(root):
    """
    Return True only if all integer keys obey both subtree rules with no duplicates. Keep
    the tree unchanged. None is valid. Node(8, Node(4, None, Node(8))) is invalid.
    """
    raise NotImplementedError
