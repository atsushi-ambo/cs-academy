def make_node(value, left=None, right=None):
    """
    Complete the Node class inside make_node. Return one new node with the given value
    and child links. Omitted links are None. For example, make_node("api",
    make_node("db")).left.value is "db".
    """
    class Node:
        def __init__(self, value, left, right):
            self.value = value
            self.left = left
            self.right = right

    return Node(value, left, right)


def preorder(root):
    """
    Return a new list of values in preorder. Use recursion. A missing link is None. Keep
    the .value, .left, and .right attributes unchanged. preorder(Node(4, Node(9),
    Node(2))) returns [4, 9, 2].
    """
    out = []

    def visit(node):
        if node is None:
            return
        out.append(node.value)
        visit(node.left)
        visit(node.right)

    visit(root)
    return out


def inorder(root):
    """
    Return a new list of values in inorder. Use recursion. A missing link is None. Keep
    the .value, .left, and .right attributes unchanged. inorder(Node(4, Node(9),
    Node(2))) returns [9, 4, 2].
    """
    out = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        out.append(node.value)
        visit(node.right)

    visit(root)
    return out


def postorder(root):
    """
    Return a new list of values in postorder. Use recursion. A missing link is None. Keep
    the .value, .left, and .right attributes unchanged. postorder(Node(4, Node(9),
    Node(2))) returns [9, 2, 4].
    """
    out = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        visit(node.right)
        out.append(node.value)

    visit(root)
    return out


def level_order(root):
    """
    Use a first-in, first-out queue. Return a new list in level order. Leave all node
    links as they are. For Node(4, Node(9, Node(1)), Node(2)), return [4, 9, 2, 1]. For
    None, return [].
    """
    from collections import deque

    if root is None:
        return []
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        out.append(node.value)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return out


def tree_stats(root):
    """
    Return (height, leaves) in one recursive traversal of Node objects. Height counts
    nodes. Keep links unchanged. For Node(1, Node(2), None), return (2, 1). For None,
    return (0, 0).
    """
    if root is None:
        return 0, 0
    if root.left is None and root.right is None:
        return 1, 1
    left_height, left_leaves = tree_stats(root.left)
    right_height, right_leaves = tree_stats(root.right)
    return 1 + max(left_height, right_height), left_leaves + right_leaves
