# Hands-on: trace the search

In a scratch folder, save this example as `trace.py` and run `python3 trace.py`.

```python
class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
tree = Node(40, Node(15, None, Node(23)), Node(70, Node(65)))

def trace(root, key):
    path = []
    while root is not None:
        path.append(root.key)
        if key == root.key:
            break
        if key < root.key:
            root = root.left
        else:
            root = root.right
    return path

print(trace(tree, 65))
```

Expected output:

```text
[40, 70, 65]
```

Change the search key from 65 to 22. Run again and read each step in the new path.

```text
[40, 15, 23]
```

Check that the last node has no left child. Explain why a visit to 23 can still mean 22 is missing.
