# Hands-on

Save this example as `experiment.py` in a scratch directory.
Run `python3 experiment.py` from that directory.

```python
from heapq import heappop, heappush

heap = [(9, "api")]
heappush(heap, (1, "db"))
heappush(heap, (2, "cache"))
print(heappop(heap))
```

Expected output

```text
(1, 'db')
```

Set both low-cost entries to cost 1. Predict which host comes out first before you run it.
