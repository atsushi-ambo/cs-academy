# 📘 Appendix III: The Complete Computer Architecture Problem Bank — The Physics of Computation and Performance

> This is "The Training Ground of the Laws of All Things." Here you turn the knowledge learned in World 7 (Inside the Machine) and GRAD 4 (Architecture)
> into hands-on problems where you **calculate with numbers and estimate performance**.
> "The same amount of computation, yet the measured times differ," "Why is this code slow?" —
> you'll become able to answer these in the language of nanoseconds, cache lines, and pipelines.

## 📖 What You'll Gain from This Problem Set

The ability to compute by hand the "**performance that doesn't appear in asymptotic complexity**" that software engineers tend to overlook.
This is also the territory tested in interviews for low-level roles (systems, games, databases, ML infrastructure, embedded).

Each problem is structured as **problem → calculation process → answer → meaning in practice**. Build the habit of doing mental math / rough estimates without a calculator.

### The "Latency Staircase" You Should Memorize (1 CPU cycle ≈ 0.3 nanoseconds)

| Operation | Approximate time | In cycles |
|---|---|---|
| L1 cache reference | About 1 nanosecond | ~4 cycles |
| Branch misprediction | About 3–5 nanoseconds | ~15 cycles |
| L2 cache reference | About 4 nanoseconds | ~14 cycles |
| Main memory reference | About 100 nanoseconds | ~300 cycles |
| SSD random read | About 16 microseconds | ~50K cycles |
| Disk seek | About 10 milliseconds | ~30M cycles |

**The most important intuition**: there's a roughly **100× gap** between L1 and memory, and a **further ~100×** between memory and SSD.
"Which tier the data lives in" dominates performance.

---

## Chapter 1: The Memory Hierarchy and Caches

### Problem 1.1 — The Measured Difference Between Row-Major and Column-Major 🟡

**Problem**: Sum a 1024×1024 matrix of `double`s (8 bytes). The cache line is 64 bytes.
(a) Row-major access and (b) column-major access — how many cache misses occur in each? Why is (a) faster?

**Calculation process**:
- Cache line 64 bytes ÷ 8 bytes = **8 doubles fit in one line**
- **(a) Row-major**: read in consecutive memory order. One miss loads 8 elements, and the next 7 are hits.
  Number of misses = total elements ÷ 8 = 1024×1024 ÷ 8 = **about 130K**
- **(b) Column-major**: each element read jumps 1024×8 = 8192 bytes ahead. You touch a different line every time, using only 1 of the 8 before it's evicted.
  Number of misses = **all elements = about 1.05M** (about 8×)

**Answer**: (a) about 130K misses, (b) about 1.05M misses. **(a) is about 8× faster** (because it exploits spatial locality).

**Meaning in practice**: even with the same O(n²), the memory access order makes it several times faster or slower. A classic case of getting faster "just by changing the loop nesting order" (the quest of World 7). Sweep multidimensional arrays **in the order that follows the memory layout**.

---

### Problem 1.2 — Average Memory Access Time (AMAT) 🟡

**Problem**: L1 hit rate 95%, L1 hit time 1 nanosecond, and on a miss a memory reference of 100 nanoseconds. What is the average memory access time?

**Calculation process**:
```
AMAT = hit time + miss rate × miss penalty
     = 1 ns + 0.05 × 100 ns
     = 1 + 5 = 6 nanoseconds
```

**Answer**: 6 nanoseconds.

**Implication**: even with a 95% hit rate, a mere 5% of misses pushes the average up to **6×**.
Raising the hit rate to 99% gives AMAT = 1 + 0.01×100 = **2 nanoseconds**. **The last few % of hit rate is decisive** (the boss battle of GRAD 4).

---

### Problem 1.3 — Detecting False Sharing 🔴

**Problem**: Two threads each rapidly update a separate variable, `counter[0]` and `counter[1]` (each 8 bytes, laid out consecutively). Despite being parallel, it became slower than a single thread. Why? How do you fix it?

**Analysis**:
- `counter[0]` and `counter[1]` are within 16 bytes → they **share the same 64-byte cache line**
- Every time thread A writes `counter[0]`, the entire line becomes "modified," and the copy in thread B's cache is **invalidated** (the MESI protocol)
- When B tries to read `counter[1]`, it has to re-fetch the line even though it's logically unrelated → the invalidations keep bouncing back and forth (**false sharing**)

**How to fix**: **separate each thread's variable onto a different cache line** (insert padding to align it to a 64-byte boundary).

```c
struct PaddedCounter {
    long value;
    char padding[56];   // pad it to 64 bytes so it sits on a different line from its neighbor
};
```

**Meaning in practice**: the hidden culprit when something is slow despite being parallelized. Suspect that "unrelated variables sit on the same line" (the quest of GRAD 4).

---

## Chapter 2: Pipelines and Branch Prediction

### Problem 2.1 — The Mystery of the Faster Sorted Array 🔴

**Problem**: For each element of an array, "if it's 128 or greater, add it," done 100 million times.
With a **sorted array**, this can be several times faster than with the **same array unsorted**. Why?

**Analysis**:
- Inside the loop there's a **branch**, `if (data[i] >= 128)`
- The CPU speculatively executes via branch prediction, guessing "the next one will probably go the same way" (GRAD 4)
- **Sorted**: the first half never satisfies the condition, the second half always does → the prediction **is almost always right** (miss rate near 0)
- **Unsorted**: whether it's ≥ 128 is random → the prediction is **wrong about 50% of the time**. Each time, it throws away the pipeline and refills (a 15-cycle penalty)

**Rough estimate**: 1 branch miss is 15 cycles × 50 million times (half are misses) = 750 million cycles ≈ a difference of hundreds of milliseconds.

**Answer**: the difference in branch-prediction accuracy. When sorted, predictions hit and no pipeline stalls occur.

**Meaning in practice**: a famous example where, even with "the same instruction count and the same complexity," the data arrangement changes the measured time. Reducing branches (going branchless, pre-sorting, `likely/unlikely` hints) becomes an optimization technique.

---

### Problem 2.2 — Pipeline Speedup Ratio 🟢

**Problem**: Execute 1000 instructions in a 5-stage pipeline (each stage 1 cycle). In the ideal case, how many times faster is it than non-pipelined?

**Calculation process**:
- Non-pipelined: 5 cycles per instruction × 1000 = **5000 cycles**
- Pipelined: 5 cycles to fill on the first instruction, then one completes per cycle = 5 + (1000−1) = **1004 cycles**
- Speedup ratio = 5000 ÷ 1004 ≈ **4.98×**

**Answer**: about 5× (the more instructions, the closer it approaches the stage count of 5).

**Implication**: if there are no hazards (data dependencies, branches), it gets faster by the number of stages. Reality has hazards, so it falls short of 5×.

---

## Chapter 3: Parallel Computing and Amdahl's Law

### Problem 3.1 — Amdahl's Ceiling 🟡

**Problem**: 90% of a program is parallelizable. What is the maximum speedup with (a) 8 cores and (b) infinite cores?

**Calculation process** (speedup = 1 / ((1−p) + p/n), p=0.9):
- (a) 8 cores: 1 / (0.1 + 0.9/8) = 1 / (0.1 + 0.1125) = 1/0.2125 ≈ **4.7×**
- (b) infinite cores: 1 / 0.1 = **10×** (the ceiling)

**Answer**: (a) about 4.7×, (b) 10× is the upper limit.

**The shocking implication**: even if 90% can be parallelized, stacking infinite cores yields **only 10×**. The sequential 10% constrains the whole.
"Reducing the sequential portion" is more fundamental than "adding cores" (GRAD 4).

---

### Problem 3.2 — Which Should You Invest In? 🔴

**Problem**: Currently p=0.7 (70% parallelizable), using 4 cores.
Your budget allows exactly one of: "improve the parallelization rate to 0.9" or "expand to 16 cores." Which makes it faster?

**Calculation process**:
- Current (p=0.7, n=4): 1/(0.3 + 0.7/4) = 1/(0.3+0.175) = 1/0.475 ≈ **2.1×**
- Plan A, improve parallelization rate (p=0.9, n=4): 1/(0.1 + 0.9/4) = 1/(0.1+0.225) = 1/0.325 ≈ **3.1×**
- Plan B, add cores (p=0.7, n=16): 1/(0.3 + 0.7/16) = 1/(0.3+0.044) = 1/0.344 ≈ **2.9×**

**Answer**: **Plan A (improving the parallelization rate) is faster** (3.1× vs 2.9×).

**Implication**: raising the parallelization rate raises **the ceiling itself** (1/(1−p)). Adding cores only approaches the ceiling.
Removing the sequential bottleneck is high ROI — an iron rule of architecture optimization.

---

## Chapter 4: The Representation of Numbers

### Problem 4.1 — The Floating-Point Trap 🟢

**Problem**: Of the following, which evaluate to `True` with `==`? State the reasons too.
(a) `0.1 + 0.2 == 0.3` (b) `0.5 + 0.25 == 0.75` (c) `0.1 + 0.1 + 0.1 == 0.3`

**Analysis**:
- What can be represented exactly in binary is only **sums of powers of 2**. 0.5 = 2⁻¹, 0.25 = 2⁻², 0.75 = 2⁻¹+2⁻² → exact
- 0.1, 0.2, 0.3 are infinitely repeating fractions in binary → they contain rounding error

**Answer**: only (b) is `True`. (a) and (c) are `False` due to rounding error.

**Meaning in practice**: `==` comparison is forbidden for amounts of money or coordinates. Compare with `abs(a−b) < ε`, or use integers (smallest unit) or a decimal type (World 7).

---

### Problem 4.2 — Decoding Endianness 🟡

**Problem**: The 32-bit integer `0x12345678` is written to memory on a **little-endian** machine.
If you arrange the bytes in order from the lowest address, what do you get? What about big-endian?

**Answer**:
- Little-endian (least significant byte at the lowest address): `78 56 34 12`
- Big-endian (most significant byte at the lowest address): `12 34 56 78`

**Meaning in practice**: if you send a raw byte sequence between machines of different endianness, the numbers get garbled. On the network, you convert to **big-endian (network byte order)** before sending (`htonl` etc. World 7 & 8).

---

## Chapter 5: Synthesis — Diagnosing "Why Is It Slow?"

### Problem 5.1 — Linked-List Traversal vs Array Traversal 🔴

**Problem**: Sum 10 million elements in order. Both an array and a linked list are O(n), yet the array is several times faster.
Estimate the difference using the nanosecond staircase.

**Analysis**:
- **Array**: contiguous layout. One cache miss (100 ns) loads 64 bytes = 16 ints, and the remaining 15 are L1 hits (1 ns).
  10 million elements ÷ 16 ≈ 625K misses × 100 ns ≈ **62.5 milliseconds** (the hit portion is negligible)
- **Linked list**: nodes are scattered across the heap. At each node you jump to where the pointer leads → **almost always a cache miss**.
  10 million × 100 ns ≈ **1000 milliseconds = 1 second**

**Answer**: the array is about 60 milliseconds, the linked list about 1 second. **About a 16× difference** (the difference in how many fit on a cache line).

**Meaning in practice**: even with the same complexity, the measured time differs by orders of magnitude depending on a data structure's memory layout.
"If there's a lot of sequential access, use an array (or place nodes together)" is an iron rule of optimization. This is also why "quicksort is among the fastest in practice" in World 4 (it's kind to contiguous memory).

---

### Problem 5.2 — Which Tier Is the Bottleneck? 🔴

**Problem**: A server's processing is slow. State guidelines for diagnosing which of the following is the bottleneck.
(a) CPU utilization 100% (b) memory shortage causing swapping (c) high disk I/O wait (d) many network round trips

**Diagnostic guidelines**:
- **(a) CPU 100%**: computation is heavy. Improve the algorithm (complexity), parallelize, improve cache efficiency
- **(b) Swapping**: physical memory shortage causes round trips to disk (the thrashing of World 10). Add memory, shrink data structures, reduce paging
- **(c) Disk I/O**: DB queries or logging. Add indexes (the B+ tree of World 11), a caching layer, batch writes, move to SSD
- **(d) Network**: intercontinental 100 ms round trips pile up. Batch requests, use a CDN, place data closer, reduce the number of round trips

**Iron rule**: **measure, don't guess**. Use a profiler, `top`, `iostat`, etc. to pinpoint "at which tier the time is being spent" before acting. If you've memorized the latency staircase, you can guess the answer the moment you see the numbers.

---

## 🏆 Tips for Clearing the Training Ground

Architecture problems all boil down to **"where the data is, and how far away it is."**

| Symptom | Suspected cause | Countermeasure |
|---|---|---|
| Slow despite the same complexity | Cache misses (poor locality) | Sequential access, reconsider data placement |
| Slow despite parallelizing | False sharing, lock contention | Cache-line separation, lock granularity |
| Slow due to many data-dependent branches | Branch mispredictions | Going branchless, sorting, hints |
| Doesn't improve even with more cores | Amdahl's ceiling (the sequential portion) | Remove the sequential bottleneck |
| Suddenly slow while eating memory | Swapping/thrashing | Reduce memory, address paging |
| Numerical computation occasionally goes wrong | Floating-point rounding error | ε comparison, integer/decimal types |

Finally, the words of the elder of GRAD 4 once more: **You can now explain why code is fast or slow, at every layer.**

➡️ Return to the entrance: [CS Quest Home](README.md) ・ [The Complete Coding Problem Bank](appendix-01-coding-problems.md) ・ [The Complete System Design Problem Bank](appendix-02-system-design.md)
