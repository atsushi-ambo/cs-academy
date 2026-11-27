# Solutions

## Count the levels

```python
size = 8
levels = 0
while size > 1:
    size //= 2
    levels += 1
print(levels)
```

Each pass halves the size. Time is O(log n) for n at least 2, with O(1) extra space.

## `halve_rounds`

As you saw in the line puzzle, there are O(log n) rounds for n at least 2. Extra space is O(1).

## `planned_visits`

The plan describes O(n log n) visits, but computing this count takes O(log n) time for n at least 2. Extra space is O(1).

## `first_over_budget`

Each pass doubles the size until its square crosses the budget. Time is O(log(budget + 2)) and extra space is O(1).
