# Solutions

## `find_time`

The included ends keep every possible match in the search. Each pass either succeeds or cuts the range roughly in half. Time is O(log n) for n ≥ 2. Extra space is O(1).

## `first_at_least`

When the bounds meet, values before lo are too small and values from lo onward qualify. Time is O(log n) for n ≥ 2. Extra space is O(1).

## `smallest_capacity`

For a fixed capacity, taking the longest possible prefix each day minimizes the number of days. Each test costs O(n). With W starting capacities, time is O(n(1 + log W)). Extra space is O(1).

## Next practice

LeetCode Explore Binary Search. Try Search Insert Position, Capacity To Ship Packages Within D Days.
