# Heap sort and comparing all sorts

## Why

Heap sort gives a bound on time and sorts within the same array.
Use it when extra storage is limited and tied keys may change order.

## Diagram

```text
[ 9  6  5  1 | 12 ]
[ 1  6  5 |  9  12 ]  after the swap
[ 6  1  5 |  9  12 ]  after the sift
```

The bar separates the active prefix from the sorted suffix.
First 9 moves to its final slot. Then 6 becomes the new root.

## Example

The remaining heap is [6, 1, 5]. Send 6 to the next slot on the left of 9.
Sift [5, 1] if needed. The final list is [1, 5, 6, 9, 12].

## Common mistakes

A child at end belongs to the sorted suffix. Leave it alone.
Heap sort can change the order of tied records when a swap skips past one of them.

## Real-world use

For a batch of timings that must stay in one list, heap sort limits extra space.
For a mixed log batch with arrival order on ties, a stable merge sort can use a buffer.

## Summary

Build in O(n), then extract in O(n log n) worst-case time overall.
Selection is simple but quadratic. Insertion works well near sorted order.
Merge can be stable with a buffer. Quicksort needs good splits to avoid its quadratic worst case.

## Model explanation

The active prefix holds a max-heap, so its first value is the largest remaining key. Swap it into the last active slot and shrink the heap. The sift fixes only the prefix, so the new suffix stays sorted.
