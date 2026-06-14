# 🏘️ World 2: The Data Structure Town — Arrays, Linked Lists, Stacks, Queues, Hash Tables

> Once you cross the mountains, a lively castle town spreads out before you.
> A weapon shop (arrays), a blacksmith (linked lists), a dishwashing shop (stacks), a bakery with a line out the door (queues),
> and deep in the town, the workshop of the legendary alchemist "Hash."
> **Only those who visit all 5 shops of this town for training earn the pass to the forest.**

**What you'll learn in this chapter (the university lecture equivalent of "Data Structures, Lectures 1–5")**
- How arrays and dynamic arrays work
- Linked lists (singly and doubly linked)
- Stacks and queues
- Hash tables (collision resolution, resizing)
- The complexity of each operation and when to use which

---

## 📖 Lecture 1: The Weapon Shop's Storehouse — Arrays (10 XP)

An **array** is a sequence of same-typed elements laid out **contiguously** in memory. Precisely because they're contiguous,
a single calculation of `base address + index × element size` reaches any element → **index access is O(1)**.

A **dynamic array** (Python's list, Java's ArrayList, C++'s vector) holds a fixed-length array internally, and
when it fills up it **allocates double the capacity and copies**. As we learned in World 1, append is **amortized O(1)**.

| Operation | Complexity | Note |
|---|---|---|
| Index access / update | O(1) | the array's greatest weapon |
| Append to end (append) | O(1) amortized | occasionally an expansion copy |
| Insert / delete at front or middle | O(n) | shift all the trailing elements |
| Search (unsorted) | O(n) | no choice but to look at everything |

📺 [UC Berkeley CS61B - Arrays (video)](https://archive.org/details/ucberkeley_webcast_Wp8oiO_CZZE)

## 📖 Lecture 2: The Blacksmith's Chain — Linked Lists (10 XP)

A **linked list** is a chain of "value + pointer to the next node" linked together. In exchange for giving up contiguity in memory,
**insertion and deletion are O(1) by just re-linking** (though moving to that location is O(n)).

```
[head] → [3|•] → [7|•] → [1|•] → None
```

| Operation | Singly Linked List | Comparison with Array |
|---|---|---|
| Insert / delete at front | O(1) | array is O(n) |
| Index access | O(n) | array is O(1) |
| Search | O(n) | the same |
| Delete when the node is known | O(1) (needs the previous node) | array is O(n) |

A **doubly linked list** also holds a previous pointer, so you can walk backward too. It frequently appears as a component of LRU caches.

**The discipline of pointer manipulation**: for insertion and deletion, "first link the new node's next, then re-attach the previous node's next."
Get the order wrong and the end of the chain vanishes into the void (i.e., you lose the reference). Train by drawing diagrams on paper.

📺 [CS50 - Linked Lists (video)](https://www.youtube.com/watch?v=2T-A_GFuoTo)

## 📖 Lecture 3: The Dishwashing Shop — Stacks (10 XP)

A **stack** is **LIFO** (Last-In, First-Out). Just like a pile of plates,
you take the plate you put down last, first. The operations are `push` (stack it), `pop` (take it), `peek` (look at it) — all **O(1)**.

**Where is it used?**
- Function calls (the call stack) — recursion is a stack itself
- Checking matching parentheses, parsing
- The browser's "back" button, an editor's Undo
- DFS (depth-first search)

## 📖 Lecture 4: The Bakery with a Line Out the Door — Queues (10 XP)

A **queue** is **FIFO** (First-In, First-Out). A line where you can buy in the order you queued up.
`enqueue` (get in line), `dequeue` (the front leaves) — implemented with a linked list or a circular buffer, it's **O(1)**.

⚠️ **Trap**: doing `pop(0)` from the front of an array causes shifting, which is O(n). A circular buffer (ring buffer)
keeps head/tail indices in a fixed-length array, and when you reach the end you wrap around to the front using the modulo, keeping it O(1).

**Where is it used?** BFS (breadth-first search), task queues, printer wait queues, messaging.

## 📖 Lecture 5: The Workshop of Hash the Alchemist (10 XP)

The deepest part of the town. A **hash table** is a magic shelf that stores and retrieves "key → value" mappings in **average O(1)**.

**How it works**:
1. A **hash function** h turns a key into an integer: h("sword") = 982134…
2. The remainder after dividing by the number of shelves m decides the bucket: 982134 % 8 = 6 → goes to shelf 6
3. When retrieving, you just do the same calculation → average O(1)

**Methods for resolving collisions (when different keys land on the same shelf)**:
- **Chaining**: make each shelf a linked list and hang entries off it
- **Open addressing (linear probing)**: if it's occupied, search the neighboring shelves in order

The **load factor** α = number of elements / number of shelves. As α grows, collisions increase and performance drops, so
when it exceeds a threshold (e.g., 0.75), you **double the shelves and re-insert all elements** (rehashing). This too is amortized O(1).

| Operation | Average | Worst |
|---|---|---|
| Insert / search / delete | O(1) | O(n) (if everything collides) |

**The interview password**: when you hear "duplicate check," "count," or "lookup table," suspect a hash table first.

📺 [MIT 6.006 - Hashing with Chaining (video)](https://www.youtube.com/watch?v=0M_kIqhwbFo)

---

## ⚔️ Quests

### Quest 1: An Eye for Choosing the Right Shop (20 XP)

Choose the best data structure for each scenario and state your reasoning.

1. From 1 million product IDs, you want to quickly check whether a given ID exists
2. You want to build an Undo feature that reverses the most recent operation
3. You want to build a list where insertion and deletion at the front happen frequently
4. You want to build a worker that processes jobs in arrival order

<details>
<summary>📜 Answers</summary>

1. **Hash table (set)** — existence check is average O(1)
2. **Stack** — undo the last operation first = LIFO
3. **Linked list** — insertion and deletion at the front are O(1)
4. **Queue** — arrival order = FIFO
</details>

### Quest 2: 💻 Implementation Quest "Forge a Dynamic Array" (50 XP)

Without using a built-in variable-length list, implement a dynamic array using only fixed-length storage
(or a simulation of a fixed-length array). Required methods:

- `size()` / `capacity()` / `is_empty()`
- `at(index)` — fail clearly if out of range
- `push(item)` (resize to double the capacity if full)
- `insert(index, item)` / `prepend(item)`
- `pop()` / `delete(index)` / `remove(item)` / `find(item)`
- Shrink: when the size becomes 1/4 of the capacity, halve the capacity

### Quest 3: 💻 Implementation Quest "Strike the Chain" (50 XP)

Implement a singly linked list: `size`, `push_front`, `pop_front`, `push_back`, `pop_back`,
`front`, `back`, `insert(index, value)`, `erase(index)`, `reverse()`, `remove_value(value)`.
**In particular, draw a diagram on paper before writing `reverse()`.**

### Quest 4: 💻 Implementation Quest "Apprentice at Hash's Workshop" (50 XP)

Implement a hash table using open addressing (linear probing):
`hash(k, m)`, `add(key, value)` (overwrite existing keys), `exists(key)`, `get(key)`, `remove(key)`.
⚠️ If remove doesn't place a "deleted marker (tombstone)," subsequent probes will break off.

### Quest 5: The Guardian of Parentheses (20 XP)

You're given a string like `"([{}])"`. Write an algorithm that determines in O(n) whether the parentheses match correctly.

<details>
<summary>📜 Hint → Answer</summary>

Push opening brackets onto a stack. When a closing bracket comes, pop and check that the type matches.
At the end, if the stack is empty, it's correct. If a mismatch or an empty pop occurs along the way, it's invalid.
</details>

---

## 👹 Boss Battle: The Castle Town Checkpoint Officer "The Trial of the Five Structures" (100 XP)

Close your notes and take it on. 70% or more to win.

1. Explain in 2 sentences why a dynamic array's append is "amortized O(1)."
2. Give one situation each where an array wins and where a linked list wins.
3. Explain how to implement a queue with two stacks. What is the amortized complexity of enqueue / dequeue?
4. What is a hash table's load factor? Why is resizing needed?
5. When does a hash table's worst-case complexity become O(n)?
6. How do you detect whether a linked list "becomes a loop partway through" (has a cycle) using O(1) extra memory?

<details>
<summary>📜 Solutions</summary>

1. The total number of copies across capacity expansions is at most 2n by the sum of a geometric series. Smoothed over n operations, it's O(1) per operation.
2. Array: situations with lots of index access (O(1)). Linked list: situations with lots of insertion and deletion at the front (O(1)).
3. An input stack A and an output stack B. enqueue pushes onto A. dequeue, if B is empty, moves all of A to B first, then pops (the order reverses, becoming FIFO). Each element moves at most twice, so it's amortized O(1).
4. Load factor = number of elements ÷ number of buckets. As it grows, collisions increase and O(1) breaks down, so when the threshold is exceeded you add shelves and re-insert.
5. When the hash function is biased and all keys land in the same bucket (the chain becomes one long list).
6. **Floyd's cycle detection (tortoise and hare)**: run a pointer advancing one step at a time and a pointer advancing two steps at a time; if they catch up, there's a cycle.
</details>

---

🏆 **Victory Reward**: the badges "🔗 Chain Wielder" and "#️⃣ Hash Alchemist" + 100 XP

➡️ To the next world: [World 3: The Tree Labyrinth](world-03-trees.md)
