# Graphs: BFS and DFS

## Why

Use a graph to find which servers can reach one another. Use BFS when each edge costs one hop.

## How the layers look

```text
        a           distance 0
       / \
      b   c         distance 1
      |
      d             distance 2
```

From a, one hop reaches b or c. Two hops along a, b, d reach d.
DFS can go a, b, d, c. BFS goes a, b, c, d.

## Example

```python
from collections import deque

queue = deque(["b", "c"])
queue.append("d")
print(queue.popleft(), queue.popleft(), queue.popleft())
```

Output is `b c d`. The first layer leaves the queue before the next layer.

## Common mistakes

Mark at first discovery to keep a vertex from entering the queue twice.
For a matrix, preserve direction by reading row then column.
For a grid, check bounds before reading a neighbor.

## At work

Use BFS to count relays, or start a search at each unseen host to find isolated network groups.

## Summary

BFS uses a queue. DFS uses recursion or a stack. Both track visited vertices.

## Model explanation

BFS starts with the source in a queue. It visits all points at one distance before visiting points one hop farther away. I mark each point when I add it, so its first distance is saved.
