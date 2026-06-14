# 🗄️ World 11: The Great Library of Records — Database Systems

> At the heart of the continent stands a great library holding all the world's records.
> The head librarian declares proudly: "This library produces the one book you seek in an instant,
> even with **hundreds of millions** of volumes. Records never break, even when many patrons write at once.
> And **even if lightning strikes and everyone collapses**, not a single character of the ledger goes wrong.
> —— Come, let me show you the mechanism."

**University equivalent**: Berkeley **CS186 Database Systems** / CMU **15-445** / MIT **6.5830**
**Prerequisites**: World 3 (the trees that B+ trees build on), World 10 (a feel for disk and logs)

**What you'll learn in this chapter**
- The relational model and SQL
- Storage and indexing (B+ trees)
- Query processing and join algorithms
- Transactions (ACID, serializability, 2PL, MVCC)
- Crash recovery (WAL)

---

## 📖 Lecture 1: The Library's Cataloging Rules — The Relational Model and SQL (15 XP)

In 1970, Codd proclaimed: "Separate how data is physically stored from the application."
All data is represented as **relations (tables)**, and operations are written as set operations. **The system figures out how to fetch it** —— that's the philosophy of a declarative language.

```sql
SELECT s.name, AVG(e.score)
FROM students s JOIN exams e ON s.id = e.student_id
WHERE e.year = 2026
GROUP BY s.name
HAVING AVG(e.score) >= 80
ORDER BY AVG(e.score) DESC;
```

- **Primary key**: a column that uniquely identifies a row. **Foreign key**: a reference to another table's primary key
- **JOIN**: matching two tables on a condition (the difference between INNER and LEFT OUTER is a frequent interview topic)
- **Normalization**: decomposition so "the same fact isn't written in two places" (preventing inconsistencies on update — update anomalies).
  In practice, you sometimes deliberately break it for performance (denormalization) — learn to discuss it as a trade-off

## 📖 Lecture 2: The Structure of the Stacks — Storage and B+ Trees (15 XP)

The library's books live on disk, and disk can only be read **in pages (4–16 KB)** — a slow warehouse (the bottom layer from World 7).
DB performance is almost entirely determined by "**how many disk I/Os you do**."

### B+ Tree — The Heart of the Database

The big sibling of World 3's BST. Each node = one page packs in **hundreds of keys**, making the tree as **short** as possible.

```
              [100 | 200]              ← internal nodes are just signposts
             /     |      \
   [10|40|70]  [120|150]  [210|260]    ← leaves hold the data (or row locations)
      ↔            ↔           ↔       ← leaves are linked sideways (range scans are blazing fast)
```

- Fan-out f ≈ hundreds → height is log_f(N). **Even a billion rows means height 3–4 = 3–4 disk reads**
- Leaves form a linked list, so **range queries** like `BETWEEN 100 AND 500` are easy (a feat a hash index cannot do)
- When an insert fills a node, **split the node** to preserve height

**The Law of Indexes**: searches get faster, but **every write also updates the index**.
"You buy read speed with write cost and storage" —— it's not free magic, it's a bargain.

## 📖 Lecture 3: The Librarian's Plan — Query Processing and Optimization (15 XP)

SQL only states "what you want." The optimizer decides **how to fetch it** (the execution plan).

### The Three Musketeers of Join Algorithms

| Method | Complexity (pages M, N) | Good for |
|---|---|---|
| Nested-loop join | O(M × N) | One side tiny, or an index exists (index nested-loop) |
| Sort-merge join | O(M log M + N log N) | Both already sorted / want sorted output |
| **Hash join** | O(M + N) | The workhorse for equality joins. Build a hash table on the smaller table, then stream the larger one through it |

World 2's hash table and World 4's sorting are working away like this on the library floor.

The optimizer estimates cost from statistics (row counts, value distributions) and picks a plan.
`EXPLAIN` lets you peek at its reasoning —— the first incantation you cast when fighting a slow query in practice.

## 📖 Lecture 4: The Library's Iron Law — Transactions (15 XP)

A **transaction** = a unit of work that is "all or nothing." A transfer is an indivisible "withdraw + deposit."

### ACID

| Letter | Meaning |
|---|---|
| **A**tomicity | Either fully executed or as if it never happened (no half-states remain) |
| **C**onsistency | Constraints (balance ≥ 0, etc.) are not violated |
| **I**solation | Concurrent execution looks the same as running transactions one at a time |
| **D**urability | Once committed, it survives even a power loss |

### Realizing Isolation — Concurrency Control

When a concurrent schedule is **equivalent to some serial execution**, we call it "serializable." That is the criterion of correctness.

- **Two-Phase Locking (2PL)**: split into "a growing phase that only acquires locks → a shrinking phase that only releases" and serializability is guaranteed (it can be proved; the intuition is "release midway and someone else's change sneaks in"). Deadlocks can occur → detect them and forcibly abort one side
- **MVCC (Multi-Version Concurrency Control)**: keep old versions of rows, and **readers read the snapshot as of their start time**. Reads don't block writes. The real workhorse of PostgreSQL and MySQL (InnoDB)
- Isolation levels (Read Committed / Repeatable Read / Serializable) are a dial for "how many anomalies you tolerate to buy speed"

### Realizing Durability — WAL (Write-Ahead Logging)

The same philosophy as World 10's journaling, here in its complete form:

> **Before writing changes to data pages, always write the log to disk first.**
> Commit = the instant the commit record is durably written to the log.

If a crash happens, read the log and **redo** (replay committed work) and **undo** (roll back uncommitted work).
This is the skeleton of the ARIES method, and the reason the world's bank ledgers survive lightning strikes.

---

## ⚔️ Quests

### Quest 1: The Librarian's SQL Training (30 XP)

For `students(id, name)`, `exams(student_id, subject, score)`, write:

1. Names of students who scored 80+ in math (subject = 'math')
2. Each student's average score (highest average first)
3. Names of students who **never took any exam** (LEFT JOIN's moment to shine)
4. The top score per subject and the student who got it (correlated subquery or window function)

<details>
<summary>📜 Sample answer (only #3 — work out the rest by running them yourself)</summary>

```sql
SELECT s.name FROM students s
LEFT JOIN exams e ON s.id = e.student_id
WHERE e.student_id IS NULL;
```
</details>

### Quest 2: 💻 Implementation Quest "Build a Mini-Library" (70 XP)

Using SQLite (bundled with nearly every language), actually create the schema above, insert data, and run all of Quest 1's SQL.
Then use `EXPLAIN QUERY PLAN` to observe how the execution plan changes **before and after** adding an index on `score`,
and explain the difference in a sentence or two.

### Quest 3: B+ Tree Desk Exercise (30 XP)

1. For a B+ tree holding 200 keys per page, estimate the page reads needed to search a billion rows.
2. How does the same search differ with a hash index? What about a range query?
3. Correct a junior who claims "the more indexes you add, the faster everything gets."

<details>
<summary>📜 Answers</summary>

1. log₂₀₀(10⁹) ≈ 3.9 → about 4 reads (the root and upper nodes stay in cache, so it's really 1–2).
2. Equality search is slightly faster with a hash at O(1), but range queries are impossible with a hash (values scatter). A B+ tree can walk a range in order via its linked leaves.
3. Indexes carry maintenance cost on every insert/update/delete and consume storage. The right answer is the minimal set that matches your read patterns.
</details>

### Quest 4: Riddles of the Iron Law (30 XP)

1. A transfer (withdraw from A, deposit to B) crashes midway. Which mechanism preserves Atomicity?
2. What breaks if two transactions read each other's uncommitted values (dirty read)?
3. Why does MVCC let "reads not block writes"?

<details>
<summary>📜 Answers</summary>

1. WAL. If there is no commit record in the log, the withdrawal is rolled back via undo during recovery.
2. If the other transaction later aborts, work based on a "value that never existed" becomes final, breaking serializability.
3. A write just creates a new version, so the reader can keep reading the old version as of its snapshot.
</details>

---

## 👹 Boss Battle: The Library's Master, "The Archive Sphinx" (150 XP)

Close your notes and fight. Win with 70% or more.

1. State the four ACID properties, each with an example of what happens when it breaks.
2. Explain, from disk characteristics, why a B+ tree (not the BST of World 3) is the standard database index.
3. Explain the hash join algorithm and say when a sort-merge join is chosen instead.
4. Explain intuitively why 2PL guarantees serializability.
5. What physically happens at "the moment of commit" (in WAL terms)?
6. To which transactions do crash-recovery redo and undo apply, respectively?
7. Dropping the isolation level from Serializable to Read Committed — what do you lose and what do you gain?

<details>
<summary>📜 Answer outline</summary>

1. A: half-states remain on abort (only one side of a transfer). C: constraint-violating data enters. I: concurrent execution stops adding up (lost updates, etc.). D: committed data is lost.
2. Disk is accessed in pages, each read costly. A BST has one key per node and needs log₂N I/Os, but a B+ tree packs hundreds of keys per page, compressing height to log_f N and minimizing I/O count.
3. Build an in-memory hash table over the entire smaller table, then stream the larger table row by row to match (O(M+N)). Sort-merge is favored when both inputs are already sorted, sorted output is needed, or memory is insufficient.
4. There exists a moment (the lock point) when all locks have been acquired, and the result equals a serial execution ordered by lock points. Releasing midway lets others' changes interleave and break the order.
5. The instant the log record containing the commit record is durably written to disk (fsync). The data-page writes can come later.
6. redo: transactions with a commit record in the log (definitely reflect the result). undo: transactions with no commit record (erase their traces).
7. Lose: the serializability guarantee (allowing anomalies like non-repeatable reads and phantoms). Gain: throughput and lower latency from reduced lock contention.
</details>

---

🏆 **Victory Reward**: Badge "🗄️ Librarian of the Great Library" + 150 XP

➡️ Next: [World 12: The Language Forge (Compilers)](world-12-compilers.md)
