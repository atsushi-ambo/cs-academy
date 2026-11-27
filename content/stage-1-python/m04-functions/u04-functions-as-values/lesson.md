# Functions as values (lambda, sorted with key)

## Why

A team may need several views of one incident log. Pass a new key for each view.

## How a key orders records

```text
("web", 9) -> (-9, "web")
("api", 9) -> (-9, "api") -> first
```

Both keys start at −9. The second field puts api before web.

## Example

```python
logs = [("web", 9), ("api", 9)]
print(sorted(logs, key=lambda row: (-row[1], row[0])))
```

Output is `[('api', 9), ('web', 9)]`.

## Common mistakes

Pass `key=rule` so Python can call it on each record.
Calling `rule()` right away passes its result instead.
`reverse=True` flips the comparison direction of every field in a tuple key, including the name tie-breaker.
Records with exactly equal keys keep their input order.

## At work

Order alerts by delay first and host second so a teammate can scan the busiest hosts.

## Summary

A callback supplies behavior. A key supplies one comparison value per item.
Use a tuple to compare fields in priority order.

## Model explanation

The key function receives one log record and returns a tuple. I put the negative delay first so high delays come first. I put the host next to break ties in name order.
