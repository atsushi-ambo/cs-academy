def search(root, key):
    """
    Return True if the integer key exists in the BST, or False otherwise. Follow only one
    branch per comparison. Do not change the tree. For Node(8, Node(4)), search(root, 4)
    is True and search(root, 5) is False.
    """
    while root is not None:
        if key == root.key:
            return True
        if key < root.key:
            root = root.left
        else:
            root = root.right
    return False


def insert(root, key, make_node):
    """
    Insert an integer key into the BST and return its root. Use make_node(key) to make a
    leaf. Keep only one copy of each key. For insert(None, 8, Node), return a node with
    key 8. Adding 4 to that root sets its left link.
    """
    if root is None:
        return make_node(key)
    if key < root.key:
        root.left = insert(root.left, key, make_node)
    elif key > root.key:
        root.right = insert(root.right, key, make_node)
    return root


def delete(root, key):
    """
    Delete an integer key from a strict BST and return the new root. Use the successor
    for two children, and preserve its right child. Deleting 8 from Node(8, Node(4),
    Node(11)) returns a root with key 11 and left key 4.
    """
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    elif root.left is None:
        return root.right
    elif root.right is None:
        return root.left
    else:
        successor = root.right
        while successor.left is not None:
            successor = successor.left
        root.key = successor.key
        root.right = delete(root.right, successor.key)
    return root


def is_bst(root):
    """
    Return True only if all integer keys obey both subtree rules with no duplicates. Keep
    the tree unchanged. None is valid. Node(8, Node(4, None, Node(8))) is invalid.
    """
    def check(node, low, high):
        if node is None:
            return True
        if low is not None and node.key <= low:
            return False
        if high is not None and node.key >= high:
            return False
        return check(node.left, low, node.key) and check(node.right, node.key, high)

    return check(root, None, None)
