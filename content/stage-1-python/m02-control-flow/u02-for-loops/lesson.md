# for loops and range

## Visit values or visit positions

To send a check to every server, use `for host in hosts`. Python gives
one name to the body at a time. Use `range(len(hosts))` if you also
need the position in a second list. The position is called an index.

```text
hosts:   web   db   cache
index:     0    1       2
```

There are three names. Index 2 is the last position.

## Pick the numbers

```python
print(list(range(2, 6, 2)))
```

The result is `[2, 4]`. Read the three values as start, stop, and step.
For a countdown to zero, try `range(3, -1, -1)`.

## Keep results

Set a total to zero before the loop. Inside the loop, add each price.
The first value must survive until you add the next one. To keep all
the values instead, start an empty list and append each new result.
