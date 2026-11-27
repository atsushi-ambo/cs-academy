# Higher-order functions on collections: map, filter, reduce, sorting with keys

## Why

A log report can be built from small rules. Each rule handles one job, such as keeping errors.

## Follow the records

```text
logs -> filter -> errors -> map -> delays -> reduce -> total
                     |
                     +-----> sorted by key ---------> view
```

Keep error records first. Use them once for delays and again for the sorted view.

## Example

```python
from functools import reduce

logs = [("api", 500, 7), ("web", 200, 2), ("db", 503, 5)]
delays = [row[2] for row in logs if 500 <= row[1] <= 599]
print(reduce(lambda total, n: total + n, delays, 0))
```

Output is `12`. The status 200 row is skipped.

## Common mistakes

A map or filter iterator is used up after one full pass.
Collect a list when several parts of the report need the same kept rows.
Use an initial value to define the result for empty input.

## At work

Build a latency report for failed requests. Filter by status before you total or sort.

## Summary

Map changes each item. Filter keeps passing items. Reduce combines items in order.
Use sorted with a key to control how records appear.

## Model explanation

I filter the log for error statuses and save the kept rows in a list. I map those rows to delays and reduce the delays to a total. I can reuse the kept rows to make the sorted view.
