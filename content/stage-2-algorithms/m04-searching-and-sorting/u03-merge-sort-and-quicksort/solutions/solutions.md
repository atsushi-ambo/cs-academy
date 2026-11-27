# Solutions

## `merge_jobs`

Only the leading item from each run can be next. Take left on ties and keep each input intact. Time and extra space are O(L + R).

## `merge_sort`

The base case gives sorted runs. Stable merging keeps that property as runs grow. Time is O(n log n) for n ≥ 2. Live copies and merged runs use O(n) extra list space, plus O(log n) frames.

## `lomuto_partition`

The scan gathers smaller or equal values on the left. The final swap places the pivot between the two groups. Time is O(k) for a range of length k and extra space is O(1).

## `hoare_partition`

Each scan moves inward and each swap puts two values on legal sides. The cut separates the groups, even if the pivot moved. Time is O(k) for k items and extra space is O(1).

## `quick_sort`

The model moves a middle value to the end and uses Lomuto. It sorts both sides of the fixed pivot. Partition space is O(1). Balanced splits take O(n log n) time and O(log n) stack space. The worst case takes O(n²) time and O(n) stack space.

## Next practice

On LeetCode, try Sort an Array, Merge Sorted Array.
