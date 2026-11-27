# Solutions

## Keep the early exit

```python
checks = 0
for code in [8, 4, 9]:
    checks += 1
    if code == 4:
        break
print(checks)
```

Breaking ends the scan before later items. Time is O(1) in the best case and O(n) in the worst, with O(1) extra space.

## `checks_until_match`

Like the line puzzle, this takes O(1) time if the first item matches and O(n) in the worst case. Extra space is O(1).

## `uniform_hit_cost`

The mean of the evenly spaced costs is halfway from 1 to n. The formula takes O(1) time and O(1) extra space in this model.

## `batch_checks`

For k targets and n nonempty codes, time ranges from O(k) to O(kn). The algorithm uses O(1) extra space.
