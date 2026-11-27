# while loops

## Test, work, update

Use while when a condition decides whether another round is needed.
For example, stop checking a server once it is ready or the check
budget is gone. Test at the top, so a budget of zero gives zero checks.

```text
remaining before tests: 2 -> 1 -> 0
tests:                 yes  yes   no
```

The third test ends the loop without running the body.

## Two ways out

```python
left = 3
while left > 0:
    left -= 1
    if left == 1:
        break
print(left)
```

This prints 1. The break ends the loop before the budget reaches zero.
A continue instead runs the condition again. Place an index update
before any continue that could keep the index stuck.
