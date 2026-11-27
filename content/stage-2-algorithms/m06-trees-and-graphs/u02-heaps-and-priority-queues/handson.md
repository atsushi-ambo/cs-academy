# Hands-on: try a priority queue

Save this in a scratch folder as `jobs.py`. Run `python3 jobs.py`.

```python
from heapq import heappop, heappush

waiting = []
for index, job in enumerate([(4, "archive"), (1, "z-check"), (1, "a-check")]):
    priority, name = job
    heappush(waiting, (priority, index, name))
while waiting:
    priority, index, name = heappop(waiting)
    print(name)
```

Expected output:

```text
z-check
a-check
archive
```

Change archive's priority from 4 to 0. Run again.

```text
archive
z-check
a-check
```

Check both outputs. Explain why the two check jobs stay in the same order.
