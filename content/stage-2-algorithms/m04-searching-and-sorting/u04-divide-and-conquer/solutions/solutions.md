# Solutions

## `peak_delay`

The one-item answers cover every value. Combining two answers takes one comparison. With bounds, the time is O(n) and the call stack uses O(log n) space for n ≥ 2.

## `fast_power`

There is one call per halving level, with a constant number of multiplications in each call. That is O(log e) operations and O(log e) frames for e ≥ 2. Python’s large integers add storage and multiplication cost as the result grows.

## `count_inversions`

An inverted pair lies in exactly one half or crosses the split. Counting the cross pairs costs O(n) per full level. Time is O(n log n) for n ≥ 2. The live merge lists use O(n) extra space, and the stack adds O(log n) frames.

## Next practice

LeetCode Explore Recursion II. Try Pow(x, n).
