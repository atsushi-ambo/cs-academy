# From recursion to loops: tail calls and an explicit stack

## Two ways to replace calls

If a call is the last action, update its next arguments as loop
variables. For a delay that falls by one per retry, reuse one number.
Python keeps frames even for tail calls, so the rewrite saves space.

## Keep work still to do

```text
input: [a, [b, c], d]
push from the right: d, [b, c], a
output after popping and opening lists: a, b, c, d
```

The right end of the stack holds what runs next. Open an inner list
by pushing its children in reverse order. This keeps the report in
its original order without needing new call frames.

```python
pending = [["a", ["b", "c"], "d"]]
while pending:
    item = pending.pop()
    if isinstance(item, list):
        for child in reversed(item):
            pending.append(child)
    else:
        print(item)
```

This prints a, b, c, and d on separate lines. Remove `reversed` to see
why the order of the pushes matters.

## Reuse repeated answers

In the stairs task, each count needs just two earlier counts.
Update the pair once per step. The branching version calculates
the same counts over and over.
