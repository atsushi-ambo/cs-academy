# Hands-on: check the sign of a lean

Save this in a scratch folder as `lean.py`. Run `python3 lean.py`.

```python
class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        left_height = 0 if left is None else left.height
        right_height = 0 if right is None else right.height
        self.height = 1 + max(left_height, right_height)
def height(node):
    return 0 if node is None else node.height

def factor(node):
    return height(node.left) - height(node.right)

root = Node(9, None, Node(14, Node(11)))
print(factor(root))
```

Expected output:

```text
-2
```

Replace the line that builds root with `root = Node(9, Node(4, Node(2)))`.
Run again. The tree has the same height, but now it leans left.

```text
2
```

Check the two signs. Say which direction a single rotation should go in the second tree.
