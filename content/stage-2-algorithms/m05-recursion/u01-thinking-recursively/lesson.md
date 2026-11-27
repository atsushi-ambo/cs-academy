# Thinking recursively

## A small job plus a smaller copy

A print queue sends n pages, then n - 1, down to one page.
A loop can add each batch. A recursive function returns the first
batch plus the answer for the batches left.

```python
def pages(n):
    if n == 0:
        return 0
    return n + pages(n - 1)

print(pages(3))
```

This prints 6.

```text
calls:   pages(3) -> pages(2) -> pages(1) -> pages(0)
returns: 6        <- 3        <- 1        <- 0
```

On the way back, each waiting call adds its own n. A call needs a
base case, a smaller input, and a return. With two calls per frame,
draw both branches and check for repeated work.
