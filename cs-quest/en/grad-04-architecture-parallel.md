# ⚛️ GRAD 4: The Theory of Everything — Computer Architecture and Parallel Computing

> The deepest place in the Heavens, the wellspring of all magic.
> Here sleeps the ultimate truth that "computation is physics."
> The sage says: "In World 7 you peeked into the underground city (hardware).
> Here you learn **why modern computers have this shape,**
> and **why the march of speed hit the wall called 'parallelism.'**
> This is the final lecture of the graduate level —— the landing of the journey of abstraction onto physics."

**Graduate-level equivalent**: Berkeley **CS152/252 Computer Architecture** / CMU **15-418 Parallel Computing** / MIT **6.172 Performance Engineering** / textbook Hennessy & Patterson
**Prerequisites**: World 7 (inside the machine), World 10 (OS and concurrency), World 1 (complexity)

**What you'll learn in this chapter**
- Instruction sets and pipelining
- Hazards, speculation, and branch prediction
- The deep memory hierarchy and cache coherence
- Parallel computing: Amdahl's law and parallel patterns
- GPUs and modern compute accelerators

---

## 📖 Lecture 1: The Machine's Mother Tongue — ISA and Pipelining (20 XP)

The **Instruction Set Architecture (ISA)** is the **contract** between hardware and software.
It defines the vocabulary of instructions the CPU understands (add, load, branch...).
- **RISC** (ARM, RISC-V): simple instructions, fast. The modern mainstream of phones
- **CISC** (x86): also holds complex instructions. Historical legacy and compatibility

### Pipelining — Processing Instructions on an Assembly Line
Like laundry: don't do wash → dry → fold one outfit at a time; while the washer washes the next load, the previous one goes to the dryer.
The classic 5 stages: **Fetch → Decode → Execute → Memory → Write-back** (the precise version of World 7's four beats).
The ideal is "one instruction completed per cycle." But in reality, **hazards** disrupt the flow.

## 📖 Lecture 2: The Disruptors of Flow — Hazards and Speculation (20 XP)

| Hazard | Cause | Fix |
|---|---|---|
| Structural hazard | Two instructions want the same unit at once | Add more units |
| Data hazard | The next instruction waits on the previous one's result | Forwarding (route the result straight after computing), stall |
| **Control hazard** | The next can't be fetched until the branch target is known | **Branch prediction** |

### Branch Prediction and Speculative Execution
The CPU **predicts "this if probably succeeds" and executes ahead**. If right, it's blazing fast; if wrong, it discards and rolls back.
Modern CPUs predict correctly over 95% of the time —— yet this very speculation gave rise to **Spectre/Meltdown**
(stealing secrets from the traces of speculative execution), a security problem from GRAD 2.
A living lesson in **leaky abstractions** ("abstraction leaks").

**Connection to practice**: why can "a loop over a sorted array" be faster? → Branch prediction hits more often.
Combined with World 7's caches, this is the core of why "the same O(n) varies in measured speed."

## 📖 Lecture 3: The True Depth of Memory — Cache Coherence (20 XP)

You learned caches in World 7. But with **multiple cores**, a new nightmare arises:
core A and core B each hold the same variable in their own cache, and when A overwrites it, B's copy becomes **an old lie.**

- **Cache coherence protocols (MESI, etc.)**: give each cache line a state (Modified/Exclusive/Shared/Invalid) and invalidate other copies when someone writes. The hardware is desperately maintaining consistency behind the scenes
- **False sharing**: even unrelated variables, if they share the same cache line (64 bytes), cause invalidations to fly back and forth and slow things down dramatically. A hidden performance killer in parallel programs
- **Memory consistency model**: the rules for how reads and writes appear on multicore. GRAD 1's distributed consistency lives inside a single chip too

## 📖 Lecture 4: The End of Speed and the Dawn of Parallelism — Amdahl's Law (20 XP)

CPUs once raised their clock speed year over year. But the **power and heat wall** (the end of Dennard scaling) limited "making one core faster."
Since then, progress has gone toward **adding cores (parallelism)**. The moment the programmer's era changed.

### Amdahl's Law — The Cold Ceiling of Parallelization
If only a fraction p of a program can be parallelized, and you use n cores, the speedup is:

```
speedup = 1 / ((1−p) + p/n)
```

Even with p = 0.95 (95% parallelizable), as n → ∞ the speedup tops out at **20×**.
**The serial portion (5%) shackles the whole.** "Stack 1000 cores for 1000× speedup" is a fantasy.
—— World 1's asymptotic analysis revives in the parallel world as the analysis of "the part that can't be parallelized."

### Parallel Patterns (the parallel version of World 14's algorithm design)
- **Data parallelism**: the same operation on many data (map. The GPU's specialty)
- **Task parallelism**: different operations at once
- **Parallelizing divide and conquer**: sort the left and right halves of a mergesort on different cores (World 4 + World 14)
- **Synchronization traps**: lock contention, false sharing, and load imbalance steal the theoretical gains (GRAD 1 / World 10's concurrency returns in physics)

## 📖 Lecture 5: An Army of Ten Thousand Dwarves — GPUs and Accelerators (20 XP)

If the CPU is "a few clever giants," the GPU is "**thousands of simple dwarves.**"
It's frighteningly good at applying the same instruction to massive amounts of data at once (SIMT).

- Matrix products and convolutions —— the computations of GRAD 3's deep learning are exactly the GPU's stage (so the AI boom and GPUs are inseparable)
- **Memory bandwidth** tends to be the bottleneck: "moving the data" is slower than computing (World 7's locality matters at a vastly larger scale)
- Dedicated accelerators like TPUs specialize "only a specific computation (tensor products) to blazing speed"

**The closing of the final lecture**: having descended from abstraction (high-level languages) to physics (transistors and power), you can now **explain why code is fast or slow at every layer.**
That is the vantage point of a computer scientist.

---

## ⚔️ Quests

### Quest 1: The Eye for Pipelines (40 XP)

1. If a 5-stage pipeline runs ideally, roughly how many cycles for N instructions (compared to naive non-pipelined)?
2. Explain how "forwarding" resolves a data hazard.
3. What is lost when a branch prediction misses? Why are loops easy to predict?

<details>
<summary>📜 Answers</summary>

1. Non-pipelined ≈ 5N cycles. An ideal pipeline is 1 cycle/instruction after fill, so ≈ N + 4 (stages−1). For large N, about 5× faster.
2. Route the previous instruction's computed result directly to the later instruction's execute stage, without waiting for write-back to the register, reducing stalls.
3. The cycles spent discarding speculatively executed instructions and refilling the pipeline (branch misprediction penalty). Loops are easy because most iterations "continue (taken)," so the same prediction keeps hitting.
</details>

### Quest 2: 💻 Implementation Quest "Measure the Ceiling of Parallelization" (80 XP)

Implement summing a large array (or matrix multiplication) with 1 thread and N threads, and measure:

1. Time the run with 1, 2, 4, 8 threads and graph the speedup ratio
2. Observe where it deviates from ideal linear speedup, and reason about it with Amdahl's law, synchronization cost, and memory bandwidth
3. If you have time, write a version where multiple threads update the same variable, and reproduce the phenomenon of **false sharing** or contention making it slower instead

### Quest 3: The Amdahl Calculation (40 XP)

1. 80% of a program is parallelizable. What is the maximum speedup on 4 cores and on infinite cores?
2. Which helps speedup more: "raising the parallel fraction from 80% to 95%" or "increasing cores from 4 to 16"? (Compare numerically.)
3. Why does this lead to the lesson "first crush the serial bottleneck"?

<details>
<summary>📜 Answers</summary>

1. 4 cores: 1/(0.2 + 0.8/4) = 1/0.4 = **2.5×**. Infinite cores: 1/0.2 = **5×** ceiling.
2. p=0.8,n=16: 1/(0.2+0.05)=4×. p=0.95,n=4: 1/(0.05+0.2375)≈3.4×. p=0.95,n=16: 1/(0.05+0.059)≈9.2×. Raising the parallel fraction is more effective because it lifts the ceiling 1/(1−p) itself.
3. Because the serial portion (1−p) sets the speedup ceiling 1/(1−p), reducing the serial bottleneck is more fundamental than adding cores.
</details>

### Quest 4: Riddles of Physics (40 XP)

1. Why did the CPU clock race stop and shift to multicore?
2. What does cache coherence guarantee? Why does false sharing occur?
3. Explain why GPUs suit deep learning, in terms of the nature of the computation.

<details>
<summary>📜 Answers</summary>

1. Raising the clock sharply increases power and heat (the end of Dennard scaling), hitting the physical limits of cooling and power. Performance gains shifted to core count (parallelism).
2. It keeps the copies of the same memory across multiple cores' caches consistent, guaranteeing one core's write is correctly reflected to others (no reading stale values). False sharing happens when logically unrelated variables co-reside on the same cache line (64B), so updating one invalidates the whole line.
3. Deep learning's core is matrix products and convolutions, with high data parallelism (the same op applied independently to massive data). GPUs are optimal for executing the same instruction across thousands of simple cores at once (SIMT).
</details>

---

## 👹 Boss Battle: The Source of All Things, "Architect Prime" (200 XP)

Close your notes and fight. Win with 70% or more. **This is the final boss of the graduate level.**

1. Explain the meaning of the ISA as "the contract between hardware and software." How do the RISC and CISC design philosophies differ?
2. Name the three kinds of pipeline hazards and the fix for each.
3. Describe the impact of speculative execution of branch prediction on both performance and security (touching on Spectre).
4. Explain the need for cache coherence on multicore, and how it resembles the consistency problem of distributed systems (GRAD 1).
5. State Amdahl's law and quantitatively refute the claim "add more cores and it gets arbitrarily faster."
6. Explain why the same O(n) algorithm can differ greatly in measured speed, from the three angles of cache, branch prediction, and parallelism.
7. Trace the abstraction hierarchy (high-level language → compiler → ISA → microarchitecture → circuits), and give one example each of how a layer hides the layer below and where the abstraction leaks.

<details>
<summary>📜 Answer outline</summary>

1. The ISA is the spec of instructions, registers, and memory model that software may rely on; as long as it's honored, different implementations (microarchitectures) run the same programs. RISC favors simple, fast, low-power instructions; CISC favors complex instructions and backward compatibility.
2. Structural (resource conflict → add resources), data (dependency → forwarding/stall), control (branch → branch prediction/delay slot).
3. Performance: speculation hides branch-wait stalls for large speedups. Security: speculatively executed instructions leave cache traces from which secrets that shouldn't be accessible can be inferred (Spectre/Meltdown). An example of a leaked abstraction (speculation was supposed to be invisible).
4. Multiple caches' copies of the same data must be kept consistent — essentially isomorphic to keeping replicated data across multiple nodes consistent in a distributed system (invalidation/update propagation, consistency models). The only difference is scale: within one chip vs. geographically distributed.
5. speedup = 1/((1−p)+p/n). The serial part (1−p) remains, so even as n→∞ the ceiling is 1/(1−p). Example: p=0.95 caps at 20×, unreachable no matter how many cores.
6. Cache: contiguous access raising hit rate is several times faster. Branch prediction: easy-to-predict patterns reduce stalls. Parallelism: if it decomposes into data parallelism, multiple cores cut wall time. None of these appears in asymptotic complexity; they shape the constant factors.
7. High-level language (hides memory management → leaks via GC pauses), compiler (hides instruction selection → leaks as performance changes from optimization), ISA (hides implementation → leaks via speculative-execution side channels), microarchitecture (hides timing → leaks via cache timing), circuits (hides physics → leaks via power-consumption analysis).
</details>

---

🏆 **Victory Reward**: Badge "⚛️ One Who Reached the Theory of Everything" + 200 XP

🎓 **The Heavens conquered!** You have toured the whole domain of computer science, from undergraduate to graduate level.
For the final words, see the [Graduate Commencement (grad-finale)](grad-finale.md).
