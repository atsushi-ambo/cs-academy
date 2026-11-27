# The call stack: how recursion runs, and recursion depth

## Frames wait for results

```text
value in each frame: 2 -> 1 -> 0
frames return:       2 <- 1 <- 0
```

The frame holding 0 returns first. A print after a recursive call
waits for that return. On error, the traceback shows the waiting calls.

## Depth can cost more than you think

Use `sys.getrecursionlimit()` to see the current limit. Even tail calls
use frames in Python. A loop works well for a long, straight scan.

```python
import sys

def descend(n):
    if n == 0:
        return "done"
    return descend(n - 1)

try:
    print(descend(sys.getrecursionlimit() + 10))
except RecursionError:
    print("too deep")
```

This prints `too deep`. Change the argument to 3 to see `done`.

## Make the next job much smaller

For a scale factor of 3 raised to 5, find 3 raised to 2 once.
Square the result and multiply by 3. Halving the exponent at each
call gives much fewer frames than subtracting 1 each time.
