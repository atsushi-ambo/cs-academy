# Hands-on

Save this example as `experiment.py` in a scratch directory.
Run `python3 experiment.py` from that directory.

```python
from collections import deque

frontier = deque(["api", "db"])
frontier.append("cache")
frontier.popleft()
print(frontier.popleft())
```

Expected output

```text
db
```

Replace popleft with pop on both lines. The order changes because the newest item now leaves first.
