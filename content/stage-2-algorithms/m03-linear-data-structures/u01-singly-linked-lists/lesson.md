# Arrays vs singly linked lists: cost of each operation

A list of urgent jobs may change often at its front. A chain keeps those edits small.

    head -> [scan] -> [mail] -> None
    tail ---------------^

The head points to scan. The next link leads to mail, which is also the tail.

**Example.** Insert sync at the front. Make sync point to scan, then move head to sync.

**Common mistake.** Dropping the only node must clear both end references.

**Real work.** A job tool can put an urgent item before the first waiting job.

| Operation | Dynamic array | Chain with head and tail |
|---|---|---|
| Read by index | O(1) | O(n) worst case |
| Find a value | O(n) worst case | O(n) worst case |
| Insert at front | O(n) | O(1) |
| Append | Amortized O(1) | O(1) |
| Remove first item | O(n) | O(1) |
| Remove by value | O(n) worst case | O(n) worst case |
| Read stored size | O(1) | O(1) |

Both use O(n) storage. A chain stores a separate next link in each node.

## Model answer

An array can use the index to reach a slot in one step. A chain follows links from the head to reach index 30. For a front insert, I point the new node at the old head and update head.
