# Closures and decorators

## Why

Keep one state per monitor. Add timing to many checks without changing their bodies.

## How a wrapper calls the original

```text
caller -> wrapper -> original check
          start      run work
          stop  <-   return result
```

The wrapper runs first and gets control again after the original call.

## Example

```python
def labeler(prefix):
    def label(host):
        return prefix + host
    return label

name = labeler("test-")
print(name("db"))
```

Output is `test-db`. The nested function still reads prefix after labeler returns.

## Common mistakes

Callbacks built in a loop can all read the final value. Use a default to save each value.
A wrapper should return the original result and use `wraps` to keep its name.

## At work

Log and time health checks in one wrapper. Retry only checks safe to repeat, with a fixed limit.

## Summary

A closure can hold state. A decorator can add behavior before or after a call.

## Model explanation

The wrapper reads the clock before and after calling the check with its original arguments. It logs the difference and returns the original result. I use wraps so the replacement keeps the original name.
