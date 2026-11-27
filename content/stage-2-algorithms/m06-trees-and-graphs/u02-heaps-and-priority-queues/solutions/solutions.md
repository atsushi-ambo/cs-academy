# Practice solutions

## `sift_up`

The inserted value moves along one path of at most O(log n) edges. The loop swaps in place using O(1) extra space.

## `push`

Appending is amortized O(1). Sifting makes the push amortized O(log n) in time, with O(1) algorithm workspace excluding list storage.

## `sift_down`

A swap repairs the old index, leaving only the chosen subtree to check. Time is O(log n) and extra space is O(1).

## `pop_min`

Moving the last item preserves the complete tree shape. Sifting uses O(log n) time and O(1) extra space.

## `heapify`

Leaves have no work, about a quarter of the nodes can move one level, and fewer can move farther. The sum is O(n) time. In-place sifts use O(1) extra space.

## `schedule`

The arrival index keeps equal-priority jobs in order even when their names sort differently. For n jobs, pushes and pops take O(n log n) time. The heap and output use O(n) space.

## Next practice

LeetCode Explore — Heap. Kth Largest Element in an Array. Last Stone Weight.
