# Binary search

## Why

A sorted timestamp list lets you skip groups of entries with one check.

## Picture

```text
index       0   1   2   3
times       2   5   5   8
target 5        ^
```

The arrow shows the first value at least 5. Index 1 is the lower bound.

## Example

Start with lo = 0 and hi = 4. Test index 2. Its value 5 lets you move hi to 2.
Test index 1 and move hi to 1. Test index 0 and move lo to 1. Return 1.

## Common mistakes

Exact search with two included ends must check the last single index.
Lower bound must keep equal values on the high side. Its result may be len(values).

## At work

Start a log scan at the first time in a requested window. For backups, test how much space one day needs.
If a capacity works, any bigger capacity also works.

## Summary

State what your bounds mean before you write a loop. Every update must preserve the rule and narrow the range.

**Model answer**

Every position before lo has a value below the target. An equal value might be the first match, so I set hi to mid and keep looking to its left.
