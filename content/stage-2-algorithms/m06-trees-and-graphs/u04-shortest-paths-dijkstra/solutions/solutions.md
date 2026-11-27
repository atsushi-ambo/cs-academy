# Solutions

## `latencies`

Current heap entries expand in cost order. Nonnegative edges ensure that a later route cannot improve a settled distance.

For V reached vertices and E scanned edges, time is O(V + E log(E + 1)) and extra space is O(V + E). Old heap entries can remain.

## `trace_route`

A parent pointer keeps only one link per vertex. The reverse walk recovers the whole route when needed.

For k hosts on the path, time and space are O(k). Detecting an unreachable target takes O(1) average time.

## `lowest_latency`

The first current target pair settles its cost. Its predecessor chain records a best route.

For V reached vertices and E scanned edges, time is O(V + E log(E + 1)) and extra space is O(V + E), including the path.

## Next practice

LeetCode Explore Graph. Network Delay Time.
