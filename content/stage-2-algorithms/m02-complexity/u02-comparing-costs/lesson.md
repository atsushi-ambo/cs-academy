# Comparing O(n), O(n log n), O(n^2) with real timings

Imagine an alert system that checks n events. It can make one scan, one
scan for each level, or one scan for each event. In this model each scan visits n items.

| n | One scan | One scan per halving | All pairs |
| --- | --- | --- | --- |
| 4 | 4 | 8 | 16 |
| 8 | 8 | 24 | 64 |
| 16 | 16 | 64 | 256 |

Halve a group until its size reaches 1. For 16, the chain is 16 → 8 → 4 → 2 → 1.
There are four halvings. For powers of two, their number is log₂ n.
At small input sizes, setup may matter more than growth. A stopwatch measures
elapsed time on one run. Counts let you compare the work as n changes.
