# Solutions

## Count two full passes

```python
checks = 0
for item in range(3):
    checks += 1
for label in range(3):
    checks = checks + 1
print(checks)
```

The first pass adds n and the second adds n. Time is O(n) and extra space is O(1).

## `shelf_checks`

Each item needs one or two checks. Time is O(n). One running count uses O(1) extra space.

## `pair_checks`

The loop does n × (n − 1) / 2 checks. Time is O(n²) and extra space is O(1).

## `shared_shelf_pairs`

For a returns and b records the solution takes O(1 + a + ab) time. The counter uses O(1) extra space.
