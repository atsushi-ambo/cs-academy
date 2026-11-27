# Practice solutions

## `count_codes`

Read the old count with a default of zero. Each visit adds exactly one.
Average time is O(n) for n status codes. The dict uses O(u) space for u distinct codes.

## `group_times`

Each service gets its own list when first seen. Appending keeps sample order.
With bounded-length keys and good hashes, grouping takes O(n) average time and O(n) output space.

## `two_sum`

One lookup and at most one insert per step give O(n) average time for fixed-size numbers and good hashes. The dict may use O(n) space.

## Next practice

LeetCode Explore Hash Table. Two Sum. Group Anagrams.
