# Recursion on lists and strings: sum, reverse, palindrome, flatten

## Make a smaller part with an index

A suffix sum can pass the same list and a larger index. At the end
return zero. Each waiting frame then adds its own size.

```text
suffix sum for [4, 8]: index 0 -> index 1 -> index 2
returns:                    12 <-      8 <-      0
```

## Text has two ends

Reverse the part after the first letter. Then add the first letter at
the end. For a palindrome, compare both ends and move both indexes
in. Stop when the markers meet or cross. Passing indexes avoids copies.

## Follow the order in nested reports

Recurse into each inner list when you reach it. Append sizes to one
result list. Make a fresh output for every top call. A default list
such as `out=[]` is shared across calls and can leak earlier results.

```python
def collect(batch, out):
    for item in batch:
        if isinstance(item, list):
            collect(item, out)
        else:
            out.append(item)

sizes = []
collect([[8], 2, [6, []]], sizes)
print(sizes)
```

This prints `[8, 2, 6]`. An empty batch adds nothing.
