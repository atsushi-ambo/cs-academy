# Merge sort and quicksort

## Why

Large event batches need fewer comparisons than simple sorts in many common cases.

## Picture

```text
merge sort   [4, 2, 5, 3] -> [4, 2]     [5, 3]
Lomuto       [4, 2, 5, 3] -> [2]    3   [5, 4]
```

The first row splits by position. The second groups around the pivot value 3, which lands at index 1.

## Example

Merge [2, 4] and [3, 5] by taking 2, 3, and 4 in order. Append the leftover 5.
With Hoare partition, keep the cut index in the left call because it can still need work.

## Common mistakes

A merge must keep leftovers and take from the left on ties for stability.
Lomuto skips a finished pivot in the recursive calls. Hoare includes its cut in the left call.

## At work

Use a stable merge to keep the order of equally timed events in a log.
In-place partitioning saves a merge buffer when sorting a list you can change.

## Summary

Merge sort uses O(n log n) time and O(n) extra list space. Quicksort uses O(n log n) time with balanced splits.
Uneven splits can bring quicksort to O(n²) time and O(n) stack space.

**Model answer**

Merge sort splits by position and uses a new list to merge sorted runs. Quicksort splits by a pivot value and moves items inside the input list. It still uses stack space, which grows when the splits are uneven.
