# Practice solutions

## `make_deque`

Creating the ring takes O(capacity) time and space. Each edit takes O(1) time and extra space.

## `offer_index`

If r candidates leave, time is O(r + 1). The edit itself uses O(1) extra space.

## `window_maxima`

A newer index with an equal or higher value can serve longer than the old index.
Each index enters once and leaves at most once, so time is O(n).
The deque uses O(k) space. The output has n - k + 1 peaks.

## Next practice

LeetCode Explore Queue & Stack. Sliding Window Maximum.
