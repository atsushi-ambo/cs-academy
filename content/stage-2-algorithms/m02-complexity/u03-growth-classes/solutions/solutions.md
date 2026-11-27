# Solutions

## Put the branching rule after the base case

```python
def settings(n):
    if n == 0:
        return 1
    return settings(n - 1) + settings(n - 1)
print(settings(2))
```

There are 2ⁿ leaves. Time is O(2ⁿ) and the longest active path uses O(n) stack space.

## `half_path`

One path has O(log n) calls, so both time and extra stack space grow as O(log n) for n at least 2.

## `order_count`

The loop does O(n) multiplications and keeps O(1) extra numbers. Very large integers cost more per multiplication.

## `triple_checks`

Trying the triples takes O(n³) time. The count takes O(1) time and O(1) extra space in this model.
