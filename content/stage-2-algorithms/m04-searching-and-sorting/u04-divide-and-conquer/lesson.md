# Divide and conquer: split, solve, combine

## Why

A large report can be easier to handle if two smaller reports give you the answers you need.

## Picture

```text
           [2, 6, 9, 4] -> 9
            /         \
     [2, 6] -> 6   [9, 4] -> 9
       /  \           /  \
      2    6         9    4
```

Each line down leads to a smaller input. Each parent keeps the larger answer.

## Example

For `2**5`, compute `2**2` once. Square 4 and multiply by 2 to get 32.
For inversion counts, taking a smaller right item adds one pair for each left item still waiting.

## Common mistakes

Include every item in exactly one half. Stop before splitting a one-item range.
Save a smaller power before squaring it. Two calls with the same arguments repeat the same work.

## At work

Combine peak delay reports for two server groups by taking the larger peak.
Count inversions in event order to measure how far the order differs from timestamp order.

## Summary

Split, solve, combine. Count the levels and the work on each one.
Finding a peak takes linear time. Testing all cross pairs one by one would lose the benefit of the merge.

**Model answer**

I compute the power with half the exponent once and square that result. For an odd exponent, I multiply by the base once more. Halving gives about log₂ e levels for exponent e.
