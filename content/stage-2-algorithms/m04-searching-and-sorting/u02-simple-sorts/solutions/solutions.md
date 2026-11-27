# Solutions

## `selection_report`

The minimum from the remaining part belongs next. The scans use O(n²) time even for sorted input. The working copy uses O(n) extra space, including the returned list.

## `insertion_jobs`

Each shift opens a spot for the saved record without crossing an equal key. Work is O(n²) in the worst case and O(n) on an ordered list. Extra space is O(n), including the returned copy.

## `bubble_report`

Each pass fixes one more value at the end. A pass without swaps proves order. Time is O(n) on ordered input and O(n²) in the worst case. Extra space is O(n) for the returned copy.

## Next practice

On LeetCode, try Sort Colors, Insertion Sort List.
