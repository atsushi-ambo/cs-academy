# Solutions

## `reduced_price`

For w weeks, time is O(w + 1). The loop uses O(1) extra space and never adds call frames.

## `unpack_sizes`

Each of n items and lists is pushed and popped once. Time is O(n). The pending stack can use O(n) extra space, for example for a wide list. The returned values also use O(n) space.

## `route_count`

The loop makes O(n + 1) additions and keeps O(1) integer values. The bytes in each count grow with n, so the bit cost is higher. The branching version repeats calls and takes exponential time.
