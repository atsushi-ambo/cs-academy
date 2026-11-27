# ⚙️ World 7: The Clockwork Underground — Inside the Machine

> Beneath the desert sprawled a vast city of gears and clockwork.
> The spells (code) you cast up on the surface were, in truth,
> all powered by the turning gears of this underground city.
> "Those who learn only the spells of the upper worlds are mages.
> **Those who come to know how this city works are called sages.**"

**What you'll learn in this chapter (a university course would call it "Computer Systems / Intro to OS")**
- How a program gets executed (compilers, interpreters, the CPU)
- The memory hierarchy and caching
- Processes and threads
- Floating-point numbers, Unicode, and endianness

---

## 📖 Lecture 1: The True Nature of Spellcasting — How Programs Are Executed (10 XP)

The journey your code takes before it runs:

```
source code → [compiler] → machine code → [CPU] fetch → decode → execute → write back
```

- **Compiler**: translates everything to machine code ahead of time, all at once (C, C++, Rust, Go). Fast to run.
- **Interpreter**: interprets line by line at runtime (plain Python). Convenient but slow.
- **Hybrid / JIT**: converts to bytecode, which a virtual machine executes while compiling the hot paths into machine code (Java, JavaScript V8).

**A CPU's life is a four-beat rhythm, repeated**: it **fetches** an instruction, **decodes** it, **executes** it, and **writes back** the result.
Modern CPUs pipeline and parallelize this, repeating it billions of times per second.

📺 [How CPUs execute programs (video)](https://www.youtube.com/watch?v=XM4lGflQFvA) /
[Instructions and Programs (Richard Buckland)](https://www.youtube.com/watch?v=zltgXvg6r3k)

## 📖 Lecture 2: The City's Warehouse Network — Memory Hierarchy and Caching (10 XP)

From the CPU's point of view, every place to store data is a trade-off between "close but small" and "far but large."

| Warehouse | Rough capacity | Rough speed (felt-time conversion※) |
|---|---|---|
| Registers | a few hundred bytes | the desk in front of you (1 second) |
| L1 cache | ~64 KB | a shelf in the same room (a few seconds) |
| L2 / L3 cache | up to tens of MB | the building next door (tens of seconds to minutes) |
| Main memory (RAM) | tens of GB | a shopping trip to the next town over (a few hours) |
| SSD / disk | several TB | ordering from overseas (weeks to years) |

※ An analogy assuming one CPU cycle is stretched out to one second.

**The cache's gamble** — locality:
- **Temporal locality**: data you used just now, you'll probably use again soon
- **Spatial locality**: data right **next to** what you used, you'll probably use soon too → memory is carried in bulk, **in cache lines (about 64 bytes each)**

**So**: scanning an array from the front is blazing fast (the neighbors keep hitting), while traversing a linked list is slow (the pointer's target lives in a far-off warehouse).
This is exactly why we said back in World 4 that "quicksort is among the fastest in practice" —— it touches contiguous memory in order, so it's kind to the cache.

📺 [MIT 6.004 - The Memory Hierarchy](https://www.youtube.com/watch?v=vjYF_fAZI5E)

## 📖 Lecture 3: The City's Workers — Processes and Threads (10 XP)

| | Process | Thread |
|---|---|---|
| What it is | a running program | a flow of execution within a process |
| Memory space | **independent** (invisible to other processes) | **shared within the same process** |
| What it owns | address space, file handles, heap | its own stack and registers (+ program counter) |
| Creation / switch cost | heavy | light |
| When one dies | other processes are unharmed | can take the whole process down with it |

- **Context switch**: when the OS switches the CPU to a different unit of execution. It saves and restores state such as the registers.
- **Concurrency**: making progress on multiple tasks by switching between them / **parallelism**: physically executing them at the same time
- **The trap of shared memory — data races**: when two threads write to the same variable at the same time, the result gets corrupted.
  A **lock (mutex)** protects it, but now the danger of **deadlock** arises, where each waits forever on the other's lock.
- The 4 conditions for deadlock (mutual exclusion, hold and wait, no preemption, circular wait) — break even one and you prevent it.

📺 [The difference between processes and threads (video)](https://www.youtube.com/watch?v=4rLW7zg21gI)

## 📖 Lecture 4: The City's Strange Number Systems (10 XP)

### Floating-point numbers — the mystery of "0.1 + 0.2 ≠ 0.3"

IEEE 754 represents real numbers in binary as `sign × mantissa × 2^exponent`.
**In binary, 0.1 is an infinitely repeating fraction**, so it can't be stored exactly. That's why:

```python
>>> 0.1 + 0.2
0.30000000000000004
```

**An adventurer's law**: never compare floating-point numbers with `==`. Compare with `|a − b| < ε`. Hold money as integers (in cents) or a decimal type.

### Unicode and UTF-8 — the machinery that carries the world's characters

- **Unicode**: a table that assigns a number (code point) to every character in the world. "あ" is U+3042.
- **UTF-8**: a **variable-length** encoding that turns code points into byte sequences. ASCII is 1 byte; Japanese is roughly 3 bytes.
- **The law**: "character count ≠ byte count." At input/output boundaries, always be mindful of the encoding.

### Endianness — the custom for ordering bytes

When you place the 32-bit integer `0x12345678` into memory:
- **Big-endian**: `12 34 56 78` (most significant first) — the network byte order
- **Little-endian**: `78 56 34 12` (least significant first) — the mainstream order for CPUs like x86

Exchange raw byte sequences between machines of different customs and the numbers get garbled. Across a network you need conversion (htonl, etc.).

---

## ⚔️ Quests

### Quest 1: The Warehouse Keeper's Eye (20 XP)

The two snippets below both compute the sum of an n×n matrix. Which is faster, and why?

```c
// (a) row-major                       // (b) column-major
for (i = 0; i < n; i++)               for (j = 0; j < n; j++)
  for (j = 0; j < n; j++)               for (i = 0; i < n; i++)
    sum += A[i][j];                        sum += A[i][j];
```

<details>
<summary>📜 Answer</summary>

(a) is faster (C lays out 2D arrays in row-major order). (a) reads contiguous addresses in order, so cache lines are used effectively. (b) jumps n elements ahead every time, causing frequent cache misses. **Same O(n²), but measured times differ by several times over.**
</details>

### Quest 2: A Catechism of Workers (20 XP)

1. When one browser tab freezes, why are the other tabs still alive? (Answer in terms of processes/threads.)
2. Two threads each run `counter += 1` 1000 times, yet the result is sometimes not 2000. What's happening?
3. Name one practical way to break the "circular wait" condition among the 4 deadlock conditions.

<details>
<summary>📜 Answer</summary>

1. Modern browsers separate each tab into its own **process**. Because a process has an independent memory space, one runaway tab doesn't spill over into the others.
2. A **data race**. `counter += 1` is three steps — read → add → write back — and when two threads' reads interleave, one side's addition is lost (a lost update). You need a lock or an atomic instruction.
3. **Unify the lock acquisition order across all threads** (always take them in the order A → B). A cycle then can't form structurally.
</details>

### Quest 3: Observing the Strange Numbers (20 XP)

Verify the following in your language of choice, and explain the reason for each.

1. The result of `0.1 + 0.2 == 0.3`
2. The result of `0.5 + 0.25 == 0.75` (why is this one true?)
3. The character count and the UTF-8 byte count of the string `"こんにちは"`

<details>
<summary>📜 Answer</summary>

1. False. Both 0.1 and 0.2 are infinitely repeating fractions in binary and carry rounding error.
2. True. 0.5 = 2⁻¹ and 0.25 = 2⁻² can be represented exactly in binary, so there's no error.
3. 5 characters, 15 bytes (each hiragana is 3 bytes in UTF-8).
</details>

### Quest 4: 💻 Implementation Quest "Bit Training" (50 XP)

Implement the following with bit operations (everyone in World 7 speaks in binary):

1. Four functions to get / set / clear / toggle the i-th bit of an integer n
2. Count the number of 1s in an integer's binary representation (popcount)
3. Determine whether n is a power of two in a single line

<details>
<summary>📜 Hint</summary>

For 3, it's `n > 0 && (n & (n - 1)) == 0`. This exploits the fact that a power of two has exactly one bit set.
</details>

---

## 👹 Boss Battle: The Underground City's Heart, "The Machine Golem" (100 XP)

Close your notes and face it. Score 70% or more to win.

1. Explain the difference between a compiler and an interpreter, along with a diagram of the path to execution.
2. List at least 4 levels of the memory hierarchy from fastest, and explain why the cache works using the two kinds of "locality."
3. Name 3 differences between a process and a thread.
4. Why is a linear scan of an array measurably much faster than traversing a linked list? (Even though the complexity is the same O(n).)
5. Why should you avoid `==` when comparing floating-point numbers, and what's the alternative?
6. On a little-endian machine, how does `0xAABBCCDD` line up in a memory dump?

<details>
<summary>📜 Answers</summary>

1. A compiler translates the whole thing to machine code and saves it before execution; at runtime the machine code runs directly. An interpreter interprets the source (or bytecode) line by line at runtime.
2. Registers → L1 → L2/L3 → RAM → SSD/disk. Because temporal locality (reusing the same data) and spatial locality (using neighboring data) are high, simply keeping recent and nearby data in small, fast storage gives a high hit rate.
3. Memory space (independent / shared), creation and switch cost (heavy / light), fault propagation (isolated / affects the whole process).
4. An array is contiguous memory where cache-line prefetching works, whereas a linked list's nodes are scattered, so it's almost always a cache miss plus a pointer chase.
5. Because rounding error from values that can't be represented in binary means calculations that should be mathematically equal don't match bit for bit. Use `|a − b| < ε` (or a ULP comparison).
6. `DD CC BB AA` (the least significant byte is placed at the lowest address).
</details>

---

🏆 **Victory Reward**: badge "🔩 One Who Knows the Heart of the Machine" + 100 XP

➡️ On to the next world: [World 8: The Sky City of Communication](world-08-networking.md)
