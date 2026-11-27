# Hands-on: trace a queue

In a scratch folder, save this example as `levels.py`. Run `python3 levels.py`.

```python
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

from collections import deque

tree = Node("web", Node("api", Node("db")), Node("cdn"))
queue = deque([tree])
while queue:
    node = queue.popleft()
    print(node.value)
    if node.left is not None:
        queue.append(node.left)
    if node.right is not None:
        queue.append(node.right)
```

Expected output:

```text
web
api
cdn
db
```

Change `popleft()` to `pop()` and run again. The right child now leaves first.
The new output is:

```text
web
cdn
api
db
```

Restore `popleft()`. Check both outputs and explain why db waits in the first run.
