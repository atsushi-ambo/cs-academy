# How memory holds data: addresses, references, stack and heap

A memory address is a location in memory. A Python name holds a reference
that lets Python reach an object. It is useful to draw the reference as an arrow.

```text
names in a frame        objects
queue ────────────────> list ["open"]
alias ──────────────────^
copy ────────────────> another list ["open"]
```

Queue and alias reach the same list. Copy reaches a second list with equal contents.
A call frame holds local names. A call stack keeps track of which frame runs next.
The heap is the general area for objects. An object can outlive the call that made it.

Use `is` for identity and `==` for equal values. Compare `id()` values only for
objects that are still alive. A list slice copies slots, while a memoryview shares
byte storage. A copy of the outer grid alone still shares its rows.
