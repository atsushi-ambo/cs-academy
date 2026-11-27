# Practice solutions

## `memoize_count`

Make the dict once for each wrapper. A membership test also finds saved zero and None.
A hit takes O(1) average time for good hashes and bounded key length. A miss also costs the full call.
The dict uses O(u) space for u entries, plus the saved results.

## `make_lru`

The dict finds a node directly. Its two links let you move it to the newest end with a few writes.
For bounded keys and good hashes, get takes O(1) average time and put takes amortized O(1) average time.
The cache uses O(capacity) space.

## `make_ordered_lru`

For good hashes and bounded key length, get takes O(1) average time and put takes amortized O(1) average time. The cache uses O(capacity + 1) space.

## `bounded_count`

The wrapper applies the same LRU rule to function arguments. A hit returns the saved result.
With one bounded string key and good hashes, a hit takes O(1) average time. A miss also runs compute.
The wrapper uses O(capacity + 1) space for its entries, plus the saved results.

## Next practice

LeetCode Explore Hash Table. LRU Cache.
