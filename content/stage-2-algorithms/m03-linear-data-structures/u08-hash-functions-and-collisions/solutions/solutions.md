# Practice solutions

## `string_slot`

Each of L characters takes one update, for O(L) time. The running number uses O(1) extra space for these capacities.

## `make_chained_map`

For bounded keys and good distribution, get takes O(1) average time. Put takes amortized O(1) average time. One resize takes O(n), and long chains can make searches O(n). Buckets and pairs take O(n + initial capacity) space.

## `make_probing_map`

Without deletes, an empty slot proves a key is absent. On a full table, limit the walk to one turn.
For bounded key length, worst-case time is O(capacity). Even hashes and light load give O(1) average time.
The table uses O(capacity) space and the loop uses O(1) extra space.

## Next practice

LeetCode Explore Hash Table. Design HashMap.
