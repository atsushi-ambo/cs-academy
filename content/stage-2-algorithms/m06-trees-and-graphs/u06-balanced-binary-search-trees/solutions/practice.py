def balance_factor(root):
    """
    Return left height minus right height using each child's stored .height. A missing
    link and an empty root each give 0 for height or factor. Keep links and heights
    unchanged. Node(9, Node(4)) has factor 1.
    """
    if root is None:
        return 0
    left_height = 0 if root.left is None else root.left.height
    right_height = 0 if root.right is None else root.right.height
    return left_height - right_height


def rotate_left(root):
    """
    Rotate a BST root with a right child. Move that child up, preserve all other
    branches, and update both changed heights. Return the pivot. A root with key 10 and a
    single right child with key 20 becomes a root with key 20 and height 2.
    """
    def refresh(node):
        left = 0 if node.left is None else node.left.height
        right = 0 if node.right is None else node.right.height
        node.height = 1 + max(left, right)

    pivot = root.right
    root.right = pivot.left
    pivot.left = root
    refresh(root)
    refresh(pivot)
    return pivot


def rotate_right(root):
    """
    Rotate a BST root with a left child. Move that child up, preserve all other branches,
    and update both changed heights. Return the pivot. A root with key 20 and a single
    left child with key 10 becomes a root with key 10 and height 2.
    """
    def refresh(node):
        left = 0 if node.left is None else node.left.height
        right = 0 if node.right is None else node.right.height
        node.height = 1 + max(left, right)

    pivot = root.left
    root.left = pivot.right
    pivot.right = root
    refresh(root)
    refresh(pivot)
    return pivot


def avl_insert(root, key, make_node, rotate_left, rotate_right):
    """
    Insert an integer into an AVL tree and return its updated root. Ignore duplicates.
    Use the given node maker and rotation functions. Complete all four repairs. For keys
    30, 10, 20 in that order, return a tree with root 20, left 10, and right 30.
    """
    def height(node):
        return 0 if node is None else node.height

    def balance(node):
        return height(node.left) - height(node.right)

    if root is None:
        return make_node(key)
    if key < root.key:
        root.left = avl_insert(root.left, key, make_node, rotate_left, rotate_right)
    elif key > root.key:
        root.right = avl_insert(root.right, key, make_node, rotate_left, rotate_right)
    else:
        return root
    root.height = 1 + max(height(root.left), height(root.right))

    factor = balance(root)
    if factor > 1:
        if balance(root.left) < 0:
            root.left = rotate_left(root.left)
        return rotate_right(root)
    if factor < -1:
        if balance(root.right) > 0:
            root.right = rotate_right(root.right)
        return rotate_left(root)
    return root
