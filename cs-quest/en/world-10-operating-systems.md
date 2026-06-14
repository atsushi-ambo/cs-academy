# 🏛️ World 10: The OS Grand Temple — Operating Systems

> When you descend from the Observatory Tower, a colossal temple appears.
> This is where every program is born, lives, and dies.
> The lord of the temple is the "kernel" —— king of all apps and the sole spokesperson for the hardware.
> In World 7 you saw the underground city (the hardware).
> **This temple teaches the "machinery of governance" that stands atop it.**

**Corresponding university courses**: Berkeley **CS162 Operating Systems** / MIT **6.S081 (xv6)** / textbook [OSTEP (free online)](https://pages.cs.wisc.edu/~remzi/OSTEP/)
**Prerequisites**: Clear World 7

**What you'll learn in this chapter**
- The kernel and system calls
- The process lifecycle and scheduling
- Concurrency: locks, semaphores, condition variables (the continuation of World 7, this time for real)
- Virtual memory (paging, TLB, page faults)
- File systems and crash consistency

---

## 📖 Lecture 1: The Temple's Twin Doors — The Kernel and System Calls (15 XP)

The OS has 3 jobs: **virtualization** (give every program the illusion that "it has the machine all to itself"),
**concurrency management**, and **persistence** (files).

The CPU has 2 privilege levels: **user mode** and **kernel mode**.
Apps run inside a cage (user mode), and when they want to touch the hardware they pray to the temple via a **system call**:

```
App: calls read(fd, buf, 100)
  → a trap instruction transitions the CPU into kernel mode
  → the kernel checks and executes (reads from disk)
  → returns the result and goes back to user mode
```

`open / read / write / fork / exec / wait / exit` —— the prayer words of UNIX.
An **interrupt** is an oracle from the hardware (keypress, timer, disk completion),
and the kernel receives these too. The timer interrupt is precisely the source of the OS's power to "take the CPU away from an app."

## 📖 Lecture 2: The Reincarnation of Souls — Processes and Scheduling (15 XP)

**The life of a process**: creation (fork) → ready ⇄ running ⇄ blocked → terminated (zombie → reaped)

The birth rites of UNIX:
- **fork()** — makes a complete copy of itself (the parent gets the child's PID, the child gets 0)
- **exec()** — replaces its own contents with a different program
- The truth of how a shell runs a command is **fork, the child execs, and the parent waits**

### Scheduling — who gets the CPU

| Method | Mechanism | Pros / Cons |
|---|---|---|
| FIFO | First come, first served | Simple / everyone waits behind a long job (convoy effect) |
| SJF (Shortest Job First) | Shortest job first | Minimizes average wait time / you can't know future lengths |
| Round Robin | Take turns via time slices | Good responsiveness / context-switch overhead |
| **MLFQ (Multi-Level Feedback Queue)** | Automatically prioritizes short interactive jobs, demotes jobs that hog the CPU | The prototype of practical OSes. Predicts the future from past behavior |

## 📖 Lecture 3: Those Who Pray at the Same Time — The Inner Sanctum of Concurrency (15 XP)

In World 7 you saw data races and deadlock. The temple grants you the formal tools.

- **Lock (mutex)**: only 1 may enter the critical section. The implementation is rooted in hardware atomic instructions (test-and-set / compare-and-swap)
- **Condition variable**: "sleep until some condition holds, and get woken up once it holds."
  `wait(cond, lock)` **releases the lock and sleeps, then reacquires it on waking**.
  ⚠️ On waking, **re-check the condition in a `while` loop** (because of spurious wakeups and being beaten to it, an `if` is not enough prayer)
- **Semaphore**: an integer counter + a wait queue. Initial value 1 makes a lock; initial value n is a "capacity limit of n seats"

### A famous trial: the producer–consumer problem

Into a fixed-length buffer, a producer puts items and a consumer takes them out.
Write "if full, the producer waits" and "if empty, the consumer waits" using 2 condition variables (or the empty/full semaphores).
**If you can write this, you've earned your first dan in concurrent programming**. It is the prototype of message queues, thread pools, and pipelines.

## 📖 Lecture 4: The Temple's Greatest Illusion — Virtual Memory (15 XP)

Each process believes it "has a vast expanse of memory all to itself." It's an illusion.

- The translation from **virtual address → physical address** is done in units of **pages** (typically 4 KB)
- The translation table is the **page table** (one per process; multi-level structure to save memory)
- Consulting the table every time would be too slow, so translation results are kept in a dedicated cache called the **TLB** (locality from World 7, once again)

**Page fault** — when an accessed page is not in physical memory, the CPU raises an exception and the kernel steps in:
- The legitimate page is on disk (swap) → load it and re-execute (**demand paging**)
- An illegal access → **segmentation fault** (the true identity of that thing you saw in C)

When physical memory runs short, **page replacement** kicks in (an LRU approximation is the standard).
The hell where replacement can't keep up and everything becomes disk round-trips is called **thrashing**.

**The blessings of this machinery**: isolation between processes (you can't see others' memory), copy-on-write fork,
memory-mapped files, shared libraries —— nearly all the magic of modern OSes is an application of paging.

## 📖 Lecture 5: The Eternal Archive — File Systems (15 XP)

- **inode**: the body of a file (metadata + the location table of data blocks). **A filename is merely a reference to an inode** (which is why hard links can be made)
- **Directory**: a special file containing a table of "name → inode number"
- Path resolution `/home/user/quest.txt` = a journey from the root inode, consulting the table one level at a time

### Crash consistency — what if the power dies mid-write?

Appending to a file is multiple operations: "write the data block + update the inode + update the free bitmap."
If it dies partway, an inconsistent archive remains. The modern solution is **journaling (WAL)**:

> **"Write the change you're about to make to a log first, stamp a commit mark, and only then apply it to the real thing."**
> If it dies, on reboot you look at the log: redo what's committed, discard what's uncommitted.

This idea of "**write to the log first**" reappears **again and again, a theme running through all of CS**: in World 11's databases (WAL/ARIES)
and in the graduate chapter's distributed systems (Raft's log replication).

---

## ⚔️ Quests

### Quest 1: The Priest's Catechism (30 XP)

1. Why does `printf` print twice right after a call to `fork()`?
2. Without a timer interrupt, why can't the OS stop a process stuck in an infinite loop?
3. What is a "zombie process," and why does it need to exist?

<details>
<summary>📜 Answers</summary>

1. Because fork makes a complete copy at the moment of the call, and **both** parent and child continue execution from the line after fork.
2. Unless the user-mode process voluntarily makes a system call, control never returns to the kernel. The timer interrupt is the only guarantee that periodically forces control back to the kernel.
3. A process that has terminated but whose parent has not yet reaped its exit code with wait(). It must hold onto its PID and status until the exit code is delivered to the parent.
</details>

### Quest 2: 💻 Implementation Quest "The Rite of Producer and Consumer" (70 XP)

Using your language's threads, locks, and condition variables (in Python, `threading`; in Java, `synchronized`/`Condition`),
implement a fixed-length-buffer producer–consumer.

- With 2 producers, 2 consumers, and buffer length 5, confirm that 1000 items flow through **with no losses and no duplicates**
- Write a comment explaining what could happen if you wrote `wait` with an `if`

### Quest 3: Scheduler Paper Exercise (30 XP)

Job A (runtime 10ms, arrival 0ms), B (runtime 2ms, arrival 1ms), C (runtime 4ms, arrival 2ms).
Compute the completion order and average turnaround time for each of FIFO, SJF (chosen from those already arrived), and RR (slice 2ms).

<details>
<summary>📜 Answers</summary>

- FIFO: A(10), B(12), C(16) → turnaround (10 + 11 + 14)/3 ≈ 11.7ms
- SJF (non-preemptive): A(10), B(12), C(16) — while A runs, B and C arrive; after A completes it's B→C, the same result. With preemption (STCF), B interrupts: B(3), C(8?)… and it improves (draw each timeline yourself)
- RR: A, B, and C take turns 2ms at a time. Draw the timeline and confirm the interactive job (the short B) responds quickly
</details>

### Quest 4: Seeing Through the Illusion (30 XP)

1. With a 32-bit virtual address and a 4 KB page size, into "how many bits of page number + how many bits of offset" does a virtual address split?
2. Even with a 99% TLB hit rate, explain why it still matters for performance, in the vocabulary of World 7's memory hierarchy.
3. Explain "copy-on-write," the reason fork is fast.

<details>
<summary>📜 Answers</summary>

1. Offset 12 bits (2¹² = 4096) + page number 20 bits.
2. A single TLB miss costs a page-table lookup = several memory accesses (one per level, for a multi-level table). Memory is 1–2 orders of magnitude slower than cache, so even a 1% miss rate pushes the average access time up substantially.
3. On fork, only the page table is duplicated; the physical pages are shared between parent and child, and all pages are marked read-only. **The moment either one writes**, only that page is copied. This permanently avoids copying pages that are almost never written.
</details>

---

## 👹 Boss Battle: "Kernel Seraphim," Lord of the Temple (150 XP)

Close your notes and take it on. Win with 70% or more.

1. State the reason for separating user mode and kernel mode, and the 2 paths (voluntary, forced) for crossing that boundary.
2. Explain how fork / exec / pipe are used when the shell runs `ls | grep txt`.
3. Why is a condition variable's wait wrapped in a while loop?
4. Explain the flow of demand paging in the order "access → fault → resolve → re-execute."
5. By what mechanism can MLFQ prioritize "short interactive jobs" without knowing their runtimes in advance?
6. Explain, by the "log first" principle, why a journaling file system can recover consistency after a crash.
7. What is thrashing? Once detected, what should the OS do?

<details>
<summary>📜 Skeleton of the solutions</summary>

1. For isolation, to protect the hardware and other processes from a runaway or malicious app. Voluntary = system call (trap); forced = interrupt/exception.
2. The parent creates a pipe with pipe() and forks twice. Child 1 redirects standard output to the pipe's write end and execs("ls"); child 2 redirects standard input to the pipe's read end and execs("grep"). The parent waits on both.
3. Because there's no guarantee the condition holds on waking (spurious wakeups; the condition being snatched by another thread). A while lets you reacquire and re-check.
4. Access a page → its present bit is invalid so the CPU raises an exception → the kernel verifies legitimacy and secures a free frame (evicting via LRU if needed), loads from disk, updates the page table → re-execute the instruction.
5. New jobs start at the highest priority and are demoted each time they use up a time slice. A short interactive job enters I/O wait before using it up, so it stays at high priority. It's a mechanism that classifies by track record of behavior.
6. Write the change to the journal first, stamp a commit record, and only then update the body. On a crash, scan the journal and reapply only committed transactions (or roll back the incomplete ones), so the body is always either "all applied" or "all unapplied."
7. A state where, due to insufficient physical memory, page eviction and loading shuttle back and forth and the CPU is essentially always waiting on I/O. The only fixes are to reduce the number of processes (swap out / admission control) or add memory.
</details>

---

🏆 **Victory Reward**: Badge "🏛️ Priest of the Kernel" + 150 XP

➡️ Next: [World 11: The Great Library of Records (Databases)](world-11-databases.md)
