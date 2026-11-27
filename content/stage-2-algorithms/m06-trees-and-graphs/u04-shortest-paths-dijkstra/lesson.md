# Shortest paths (Dijkstra)

## Why

The smallest number of hops can still have the longest delay.
To estimate transit time, add all link weights.

## Compare two routes

```text
api ---- 12 ----> db
api ----  3 ----> cache ---- 4 ----> db
```

The direct route costs 12. The route through cache costs 3 + 4 = 7.

## Example

```python
from heapq import heappop, heappush

pending = [(12, "db")]
heappush(pending, (7, "db"))
print(heappop(pending))
```

Output is `(7, 'db')`. The old candidate remains in the heap.

## Common mistakes

A node can enter the heap several times. Compare each popped cost with its current best cost.
Only update on a strict improvement. This avoids repeated updates around zero-weight loops.
A negative edge can invalidate a cost already popped from the heap.

## At work

Model links with observed latencies to compare network paths at one point in time.

## Summary

Pop the lowest candidate, skip old entries, and improve neighbor costs.
Use predecessors to return the path. Require nonnegative weights.

## Model explanation

The heap removes the least cost among the pending routes. I skip a pair if its cost is old. Any remaining route can only add nonnegative cost, so it cannot beat the current target cost.
