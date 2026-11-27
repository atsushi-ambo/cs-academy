# Loop patterns: counting, accumulating, searching, nested loops

## Decide what the report needs

Count: increase a total by 1 for each match. Sum: add the value.
Search: stop at the first match. Put the missing result after the loop.

```python
total = 0
for size in [2, 12, 18]:
    if size >= 10:
        total += size
print(total)
```

This prints 30. The two large files add their sizes.

## Trace rows and indexes

```text
[[4, 7], [], [9]] -> visit 4, 7, then 9
```

The outer loop chooses a row, even an empty one. The inner loop reads
the items in that row. If you want to keep only some items, append them
to a fresh list. Removing an item in place can skip its neighbor.
