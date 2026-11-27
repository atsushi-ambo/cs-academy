# Heaps and priority queues

## Why

A waiting job queue may need to run a check before an older report.
A min-heap keeps the smallest priority at the front.

## Diagram

```text
       1
     /   \
    5     3
   /
  8
```

The list is [1, 5, 3, 8]. Top to bottom and left to right gives the array order.
Every parent is at most its children. The siblings 5 and 3 need no order.

## Example

Push 0 onto [1, 5, 3, 8]. Append 0 at index 4.
Swap it up past 5 and then 1. The heap becomes [0, 1, 3, 8, 5].
Popping 0 moves the last value to the root. Sift it down past the smaller child, 1.

## Common mistakes

A right child may be missing even when a left child exists.
Swapping down with the larger child can leave a smaller child below the new parent.

## Real-world use

A server can rank queued checks by urgency. Use the arrival index for ties.
The same idea can rank events by their next run time.

## Summary

Push sifts up and pop sifts down. Each follows one path.
Building from the bottom takes O(n) time. A heap keeps the minimum ready but leaves other entries partly ordered.

## Model explanation

Save the minimum at index zero, then remove the last item. If the heap still has items, move the old last item to the root. Swap it down with the smaller child until the parent rule holds.
