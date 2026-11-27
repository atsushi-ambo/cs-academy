# Lists: Keeping Many Values in Order

> Reference sheet. In the app you learn this unit step by step (`steps.yaml`).
> Use this page to review everything on one page.

## Why do we need lists?

Imagine you manage five web servers. With only variables, you would write:

```python
server1 = "web01"
server2 = "web02"
server3 = "web03"
server4 = "web04"
server5 = "web05"
```

This works for five servers. It does not work for five hundred. You also cannot
ask simple questions like "How many servers do I have?" or "Check every server."

A **list** solves this. A list is **one value that holds many values in order**.

```python
servers = ["web01", "web02", "web03", "web04", "web05"]
```

Now `servers` is a single name, but it contains five **items**.

> **Key idea:** A list is like a numbered row of boxes. Each box holds one item,
> and each box has a number called an **index**.

## Indexes start at 0

```text
 index:     0        1        2        3        4
        +--------+--------+--------+--------+--------+
servers | "web01"| "web02"| "web03"| "web04"| "web05"|
        +--------+--------+--------+--------+--------+
 index:    -5       -4       -3       -2       -1
```

```python
servers[0]    # "web01"  (the first item)
servers[2]    # "web03"
servers[-1]   # "web05"  (the last item)
servers[-2]   # "web04"  (second from the end)
```

Why does counting start at 0? The index means **"how many steps from the
start."** The first item is 0 steps from the start. You will see the deeper
reason in Stage 4, when we look at how memory works.

If you use an index that does not exist, Python stops with an error:

```python
servers[5]
# IndexError: list index out of range
```

This is a good thing. Python tells you about the mistake immediately, instead
of giving you a wrong value silently. Read error messages carefully: the last
line tells you **what** went wrong.

## How many items? `len()`

```python
len(servers)   # 5
```

The last valid index is always `len(servers) - 1`. This is why `servers[5]`
failed: the length is 5, so the last index is 4.

## Slices: taking a part of a list

A **slice** returns a **new list** with some of the items.

```python
servers[1:3]   # ["web02", "web03"]
servers[:2]    # ["web01", "web02"]          (from the start)
servers[3:]    # ["web04", "web05"]          (to the end)
servers[:]     # a copy of the whole list
```

The rule is `list[start:stop]`: **start is included, stop is not.**
A helpful way to remember: `servers[1:3]` has `3 - 1 = 2` items.

## Lists are mutable (you can change them)

Lists can be changed **in place** (without making a new list). Watch the list after each line:

```python
servers = ["web01", "web02", "web03"]
servers[0] = "lb01"          # ["lb01", "web02", "web03"]
servers.append("web06")      # ["lb01", "web02", "web03", "web06"]
servers.insert(1, "web00")   # ["lb01", "web00", "web02", "web03", "web06"]
servers.remove("web03")      # ["lb01", "web00", "web02", "web06"]
last = servers.pop()         # last is "web06"; ["lb01", "web00", "web02"]
first = servers.pop(0)       # first is "lb01"; ["web00", "web02"]
```

| Method | What it does | Returns |
|---|---|---|
| `append(x)` | Adds `x` to the end | `None` |
| `insert(i, x)` | Adds `x` at index `i` | `None` |
| `remove(x)` | Removes the first `x`. `ValueError` if `x` is not there | `None` |
| `pop()` / `pop(i)` | Removes the last item / the item at `i` | the removed item |
| `sort()` | Sorts the list in place | `None` |

### A very common mistake

```python
servers = servers.append("web07")   # WRONG
print(servers)                      # None
```

`append` changes the list and returns `None`. Assigning the result back
replaces your list with `None`. Write it like this instead:

```python
servers.append("web07")             # RIGHT
```

The same is true for `sort()`. If you want a **new sorted list** and want to
keep the original, use the built-in function `sorted()`:

```python
ports = [443, 22, 80]
ordered = sorted(ports)   # new list: [22, 80, 443]
print(ports)              # unchanged: [443, 22, 80]
```

## Checking membership: `in`

```python
"web02" in servers      # True or False
"db01" not in servers   # True or False
```

## Looping over a list

You learned `for` loops in the previous module. A list is the most common
thing to loop over:

```python
for server in servers:
    print(f"Checking {server} ...")
```

Read it in English: *"For each server in servers, print a message."*
Choose a singular name (`server`) for one item and a plural name (`servers`)
for the list. This small habit makes code much easier to read.

### Pattern: building a new list (accumulate)

A very common job is "take a list, and make a new list from it."

```python
response_times_ms = [120, 950, 80, 1500, 300]

slow = []                         # 1. start with an empty list
for t in response_times_ms:       # 2. look at each item
    if t > 500:                   # 3. decide
        slow.append(t)            # 4. collect

print(slow)   # [950, 1500]
```

Memorize these four steps: **start empty, loop, decide, collect.** You will use
this pattern hundreds of times. Later in this module you will learn a shorter
way to write it (list comprehensions), but the idea is the same.

### Pattern: computing one value from a list

```python
total = 0
for t in response_times_ms:
    total += t
average = total / len(response_times_ms)
```

Python has built-in functions for common cases: `sum()`, `min()`, `max()`.
Use them in real code. Writing the loop yourself first helps you understand
what they do.

## Walking two lists together: `zip()`

```python
for server, ms in zip(servers, response_ms):
    print(server, ms)
```

`zip` stops at the **shorter** list without any error. When two lists must
match, check `len()` first and stop with `raise ValueError("...")` if they don't.

## Two names, one list (aliasing)

This surprises many beginners:

```python
a = [1, 2, 3]
b = a          # b is NOT a copy. b and a are two names for the same list.
b.append(4)
print(a)       # [1, 2, 3, 4]
```

A variable does not *contain* a list. It *points to* a list. `b = a` makes a
second arrow to the same list. To make an independent copy, use `a.copy()` or
`a[:]`. (This is a *shallow* copy: lists inside the list are still shared.)

```text
a ──┐
    ├──► [1, 2, 3, 4]
b ──┘
```

This matters in real work. If a function changes a list it received, the
caller sees the change. Always ask: **"Does this code change the list, or make
a new one?"**

## Where lists are used in real systems

- A list of hostnames to check in a health-check script.
- Lines read from a log file.
- Rows returned from a database query.
- A JSON array returned by a web API (it becomes a Python list).

## Summary

- A list stores many items **in order**. Indexes start at **0**; `-1` is the last item.
- `len(x)` gives the number of items. The last index is `len(x) - 1`.
- Slices `x[start:stop]` return a **new** list; `stop` is not included.
- `append`, `insert`, `remove`, `pop`, `sort` change the list **in place**.
  Most of them return `None`.
- Use the **start empty, loop, decide, collect** pattern to build new lists.
- `b = a` does not copy. Use `a.copy()` when you need a copy.

## Explain it in English (2–4 sentences)

Write your answer in the app. Try not to look at this page.

> Explain to a new teammate the difference between `ports.sort()` and
> `sorted(ports)`. When would you use each one?

Rubric (self-check, 0–3 each): correct idea / a concrete example / clear English.
