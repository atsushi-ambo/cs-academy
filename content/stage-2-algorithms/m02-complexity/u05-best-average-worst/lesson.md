# Best, average, and worst cases

You scan a list of n delivery codes from left to right, stopping at the first match.
For a fixed n greater than zero, different targets can have different costs.

| Case | Checks | Why |
| --- | --- | --- |
| Best | 1 | First item matches |
| Worst | n | Last item matches or none match |
| Average under a stated model | (n + 1) / 2 | One match, each position equally likely |

A model describes which inputs can arrive and how often. If all searches miss,
the average is n checks. If most match early, the average can be lower.
Always name the model before giving an average. On an empty list, there are no checks.
