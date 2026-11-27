# Solutions

## `service_groups`

Each leaf fixes one include-or-skip choice per item. There are 2ⁿ leaves. Copies give O(n·2ⁿ) time and output space for n ≥ 1. The path and frames use O(n) working space.

## `job_orders`

Each path reaches a unique order. There are n! complete paths. Scans with used flags and copying outputs take O(n·n!) time and O(n·n!) output space for n ≥ 1. The flags, path, and frames take O(n) working space.

## `count_boards`

Pruning rules out a whole branch as soon as its next queen clashes. There are at most O(n!) paths and partial paths combined. Scanning n candidate columns per active call gives an O(n·n!) time bound with typical set operations. Sets and frames take O(n) space.

## Next practice

LeetCode Explore Recursion II. Try Subsets, Permutations, N-Queens II.
