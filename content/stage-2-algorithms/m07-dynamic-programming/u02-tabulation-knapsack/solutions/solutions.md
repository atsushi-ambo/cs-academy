# Solutions

## `bag_value`

The smaller capacity still stores the answer before the current item. Each item can contribute to a choice only once.

For n items and capacity C, time is O((n+1)(C+1)) and extra space is O(C+1).

## `min_coins`

Every valid payment has a final coin. Removing it leaves a smaller amount already solved.

For A amount and m coins, time is O((A+1)(m+1)) and extra space is O(A+1).

## `lcs_length`

A matching suffix can extend a common subsequence of the shorter prefixes. A mismatch must drop at least one final letter.

For string lengths m and n, time and table space are O((m+1)(n+1)). Just two rows can reduce space to O(n+1).

## `bag_choices`

The backward walk preserves the optimal value. If skipping costs value, taking the current item is necessary.

For n items and capacity C, time and extra space are O((n+1)(C+1)). The backward walk alone takes O(n) time.

## Next practice

LeetCode Explore Dynamic Programming. Partition Equal Subset Sum. Coin Change. Longest Common Subsequence.
