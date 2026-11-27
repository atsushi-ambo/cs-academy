# Memoization

## Why

Repeated branches may ask the same small question. Save the answer once.

## See the overlap

```text
         fib(4)
        /      \
     fib(3)   fib(2)
      /   \
  fib(2) fib(1)
```

Both branches reach fib(2). The second request can reuse the first result.

## Example

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(4), fib.cache_info().misses)
```

Output is `3 5`. Each different input from 0 through 4 gives one miss.

## Common mistakes

A cache key must contain every part of the state. Coin combinations need the amount and the index.
Check dict membership so stored results such as zero still count as hits.

## At work

Reuse a calculation when multiple planning routes leave the same amount of work and the same available resources.

## Summary

Memoization calculates each needed state on its first visit. Later visits return the saved answer.

## Model explanation

I store the coin index and the remaining amount as the key. The same amount can give a different count when fewer coin values are available. Each pair needs its own saved result.
