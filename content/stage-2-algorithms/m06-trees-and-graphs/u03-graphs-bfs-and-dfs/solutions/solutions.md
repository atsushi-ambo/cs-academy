# Solutions

## `hop_counts`

All queued distances are in order from small to large. The first discovery gives the fewest hops.

Time is O(V + E) and extra space is O(V) for the reached part of the graph.

## `stack_reachable`

Taking from the end explores recently found work first. Marking on push keeps one pending entry per vertex.

Time is O(V + E) and extra space is O(V) for reached vertices and edges.

## `component_count`

Any start in the same connected group reaches the same set. The order of group discovery does not change the count.

For the full graph, time is O(V + E) and extra space is O(V).

## `flood_size`

We can generate neighbors as needed, so there is no graph copy. The set prevents revisiting the same cell.

For k reached cells, time and extra space are O(k) since each cell has at most four neighbors.

## Next practice

LeetCode Explore Graph. Number of Provinces. Flood Fill.
