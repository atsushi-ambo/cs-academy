# Tabulation: knapsack

## Why

Several tool sets leave the same room in a bag. A table lets each smaller answer help later choices.

## Read one cell

```text
previous row     [ value at c-w ] ... [ value at c ]
                        |                   |
                take, add v                skip
                          \                /
                            best cell at c
```

Each new cell uses two possible answers from the previous row. Take the larger value if the item fits.

## Example

```python
best = [0, 0, 0, 0, 0]
for c in range(4, 1, -1):
    best[c] = max(best[c], 5 + best[c - 2])
print(best)
```

Output is `[0, 0, 5, 5, 5]`. One item of weight 2 gives value 5 at every capacity where it fits.

## Common mistakes

Repeated inner lists share the same row. Build new rows one by one.
A single knapsack row needs descending updates. Minimum coins allows reuse and builds by increasing amount.
A subsequence can skip letters, but it keeps order.

## At work

Use capacity tables for small repair kits. Use LCS to compare the order of tags in two text records.

## Summary

Pick a state, fill its dependencies first, and keep enough history to recover the choices you need.

## Model explanation

I read a smaller capacity when I take an item. In descending order that cell still holds the previous row's answer. In increasing order I might read a cell already updated with the same item.
