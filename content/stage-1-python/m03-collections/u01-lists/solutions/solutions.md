# Solutions and Explanations

Look at this page only after the tests pass, or after you have tried for at
least 20 minutes. Reading a solution is useful only when you compare it with
your own attempt.

## 1. `last_and_first`

```python
def last_and_first(items):
    if not items:
        return []
    return [items[-1], items[0]]
```

- `if not items:` is true when the list is empty. An empty list counts as
  "false" in Python. This check must come first, because `items[-1]` on an
  empty list raises `IndexError`.
- `[items[-1], items[0]]` builds a **new** list, so the input is not changed.
- With one item, `-1` and `0` point to the same box, so the result is
  `["only", "only"]`. The tests check this **edge case** on purpose.

**Takeaway:** always ask "What if the list is empty? What if it has one item?"
These two questions find many bugs.

## 2. `slow_servers`

```python
def slow_servers(servers, response_ms, limit_ms):
    if len(servers) != len(response_ms):
        raise ValueError("servers and response_ms must have the same length")
    slow = []
    for server, ms in zip(servers, response_ms):
        if ms > limit_ms:
            slow.append(server)
    return slow
```

- `zip` stops at the **shorter** list without any error. That is why we check
  the lengths first. Silent data loss is worse than an error.
- `>` (not `>=`): the spec says "greater than". A response of exactly 500 ms
  is not slow. The test `test_limit_is_not_slow` checks this **boundary**.
- `raise ValueError(...)` stops the function and tells the caller what is
  wrong. You will learn more about exceptions in Module 5.

## 3. `without_duplicates`

```python
def without_duplicates(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result
```

- This is the "start empty, loop, decide, collect" pattern exactly.
- `item not in result` looks through `result` from the start. For a list of
  `n` items, this can take about `n × n` steps in total. For 100 items that is
  fine. For 1,000,000 items it is very slow.
- In Module 4 you will learn **sets**, which check membership much faster.
  In Stage 2 you will learn how to describe this cost with **Big-O notation**
  (this solution is `O(n²)`).

## 4. `moving_window_max`

```python
def moving_window_max(values, size):
    if size < 1 or size > len(values):
        return []
    maxima = []
    for start in range(len(values) - size + 1):
        maxima.append(max(values[start:start + size]))
    return maxima
```

- How many windows are there? If there are 7 values and the window size is 3,
  the windows start at index 0, 1, 2, 3, 4. That is `7 - 3 + 1 = 5` windows.
  Off-by-one errors (one too many or one too few) are the most common bug in
  this kind of code. Draw the boxes on paper when you are unsure.
- `values[start:start + size]` is a slice: a new list of `size` items.
- This kind of calculation is used in monitoring: "the maximum CPU usage in
  every 5-minute window."
- This solution looks at every item in every window. In Stage 2 you will
  learn a faster method (a deque-based sliding window), and you can practice it
  with LeetCode problem 239, "Sliding Window Maximum".

## Next practice (outside the app)

- HackerRank: Python → "Lists" and "Find the Runner-Up Score!"
- LeetCode: Explore → Arrays 101 → "Introduction" and "Inserting Items Into an Array"

Solve them, then write one sentence in English in the app about what was new.
