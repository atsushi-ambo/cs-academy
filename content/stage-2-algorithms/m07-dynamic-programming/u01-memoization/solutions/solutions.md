# Solutions

## `fib_misses`

Each distinct input gets one entry. Counting entries counts misses for this empty-start cache.

There are O(n) calls and O(n) cache and stack space, counting arithmetic as O(1).

## `stair_ways`

Each nonempty plan has exactly one first move. Results for smaller stair counts get reused by both branches.

There are O(n) operations and O(n) extra space for the stack and cache, treating arithmetic as O(1).

## `coin_ways`

Use and skip separate the combinations by whether they still use the current value. The key distinguishes which values remain available.

For m input coins, d distinct values, and amount A, worst-case time is O(1 + m + d log(d+1) + d(A+1)). Extra space is O(1 + d(A+1)).

## Next practice

LeetCode Explore Dynamic Programming. Climbing Stairs. Coin Change II.
