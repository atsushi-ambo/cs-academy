# 🃏 Appendix V: Concept Flashcard Deck — Burn It Into Memory with Active Recall

> Welcome to the Temple of Memory. Just reading the lectures isn't enough — concepts fade in a few days.
> The strongest study methods that memory research has uncovered are **active recall** and **spaced repetition** ——
> the very act of "trying to remember" is what strengthens memory.
> These cards are the tool for that. **Before you look at the answer, always say it out loud (or write it down).**

## 📖 How to Use

1. Once you've read the question, **answer in your own words** before opening the `<details>` (not just in your head — out loud or on paper)
2. Open it and check your answer. **Mark the cards you got wrong or stumbled on**
3. **Spaced repetition**: re-attempt the cards you missed the next day, 3 days later, a week later, and a month later
4. Aim for about one world's worth per day (10–15 cards). Don't do them all in one sitting
5. Record the cards you keep getting wrong on the retry list in your [character sheet](character-sheet.md)

> 💡 "I recognize it when I see it" is not memory. "I can say it with nothing in front of me" is memory. These cards close that gap.

---

## 🏔️ World 1: The Big-O Mountains

**Q1.** What "upper bound" does Big-O express? How does it differ from Θ (Theta)?
<details><summary>Answer</summary>Big-O is the upper bound on the growth rate (it won't get worse than this). Θ is both an upper and lower bound (exactly that growth rate).</details>

**Q2.** Order O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ) from fastest to slowest.
<details><summary>Answer</summary>O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) (slower the further right).</details>

**Q3.** What is the complexity of a loop that "keeps halving n"?
<details><summary>Answer</summary>O(log n).</details>

**Q4.** What's the difference between "worst-case complexity" and "amortized complexity"?
<details><summary>Answer</summary>Worst-case = the cost of one operation on the most adversarial input. Amortized = the average per-operation cost when occasionally-expensive operations are spread out (e.g., appending to a dynamic array is amortized O(1)).</details>

**Q5.** Why measure runtime by growth rate rather than in "seconds"?
<details><summary>Answer</summary>Seconds vary depending on the machine, but how the number of operations grows with input size is intrinsic to the algorithm.</details>

---

## 🏘️ World 2: The Data Structure Town

**Q1.** On which operations does an array beat a linked list, and on which does it lose?
<details><summary>Answer</summary>Wins: indexed access O(1). Loses: insertion/deletion at the front or middle O(n) (a linked list is O(1) at the front).</details>

**Q2.** What are the ordering rules of a stack and a queue?
<details><summary>Answer</summary>Stack = LIFO (last in, first out). Queue = FIFO (first in, first out).</details>

**Q3.** How does a hash table achieve average O(1) lookup?
<details><summary>Answer</summary>A hash function converts the key into a bucket number, so you look directly at that bucket. With no collision, it's a single computation.</details>

**Q4.** When does a hash table degrade to worst-case O(n)?
<details><summary>Answer</summary>When all keys collide into the same bucket (the chain becomes one long list).</details>

**Q5.** When you hear "duplicate check," "counting," or "lookup table," what should you suspect?
<details><summary>Answer</summary>A hash table (set/dictionary).</details>

**Q6.** How do you detect a cycle in a linked list using O(1) space?
<details><summary>Answer</summary>Floyd's "tortoise and hare." Run one pointer one step at a time and another two steps at a time; if they meet, there's a cycle.</details>

---

## 🌲 World 3: The Tree Labyrinth

**Q1.** State the BST invariant precisely.
<details><summary>Answer</summary>At any node, **every element** in the left subtree < the node < **every element** in the right subtree (not just the direct children).</details>

**Q2.** What does an inorder traversal of a BST produce?
<details><summary>Answer</summary>The values in ascending sorted order.</details>

**Q3.** On what input do BST operations fall from O(log n) to O(n)?
<details><summary>Answer</summary>When you insert an already-sorted sequence in order (the tree becomes a straight line). Balanced trees prevent this.</details>

**Q4.** What is the rule of a max-heap? What are the parent/child indices in an array?
<details><summary>Answer</summary>Parent ≥ child. The children of parent i are 2i+1 and 2i+2; the parent of child i is (i−1)//2.</details>

**Q5.** What's the complexity of heapify (building a heap from an array)? (Trick question)
<details><summary>Answer</summary>O(n). Not n log n (because most nodes are near the bottom where the height is small).</details>

**Q6.** "I want to always keep the top k elements." What do you use?
<details><summary>Answer</summary>A min-heap of size k. O(log k) per element.</details>

---

## 🌋 World 4: The Sorting Volcano

**Q1.** What is a "stable sort"?
<details><summary>Answer</summary>A sort that preserves the original order of elements with equal keys.</details>

**Q2.** What are the worst-case complexities of merge sort and quicksort?
<details><summary>Answer</summary>Merge sort O(n log n) (always); quicksort O(n²) (worst case, avoided with a random pivot).</details>

**Q3.** What input makes quicksort worst-case O(n²), and how do you avoid it?
<details><summary>Answer</summary>Picking an end element as the pivot on already-sorted data is skewed. Avoid it with a random pivot or median-of-three.</details>

**Q4.** What lower bound can comparison sorts never beat? Why?
<details><summary>Answer</summary>Ω(n log n). Distinguishing the n! possible orderings via comparisons (each halving the possibilities) requires about log₂(n!) ≈ n log n comparisons.</details>

**Q5.** How do you sort integers from a small range in O(n)?
<details><summary>Answer</summary>Counting sort (it doesn't compare, so it breaks past the n log n wall).</details>

---

## 🌊 World 5: The Graph Ocean

**Q1.** For "shortest path (unweighted)," do you use BFS or DFS?
<details><summary>Answer</summary>BFS (it discovers nodes in order of distance 0, 1, 2, …, so the first arrival is the shortest).</details>

**Q2.** What data structures do BFS and DFS use?
<details><summary>Answer</summary>BFS uses a queue; DFS uses a stack (or recursion).</details>

**Q3.** What is the condition for a topological sort to exist?
<details><summary>Answer</summary>The graph must be a DAG (a directed acyclic graph).</details>

**Q4.** What kind of edge breaks Dijkstra's algorithm?
<details><summary>Answer</summary>Negative-weight edges (a finalized distance might later shrink, breaking the greedy premise).</details>

**Q5.** Between an adjacency list and an adjacency matrix, which suits a sparse graph?
<details><summary>Answer</summary>The adjacency list (memory O(V+E)). The adjacency matrix is O(V²) but checks edge existence in O(1).</details>

---

## 🏜️ World 6: The Recursion Desert & DP Ruins

**Q1.** What are the two conditions for a recursive function to terminate?
<details><summary>Answer</summary>A base case exists, and every recursion definitely moves closer to the base case.</details>

**Q2.** What are the two conditions under which DP applies?
<details><summary>Answer</summary>Overlapping subproblems and optimal substructure.</details>

**Q3.** What's the difference between memoization (top-down) and bottom-up DP?
<details><summary>Answer</summary>Memoization = stay recursive but cache results. Bottom-up = fill a table starting from the smallest problems. Both solve each subproblem exactly once.</details>

**Q4.** Why is naive recursive Fibonacci O(2ⁿ), and why does memoization make it O(n)?
<details><summary>Answer</summary>Because it re-solves the same subproblems an exponential number of times. There are actually only n+1 distinct subproblems, so memoizing solves each once for O(n).</details>

**Q5.** When do you need DP rather than a greedy approach?
<details><summary>Answer</summary>When a locally optimal choice doesn't guarantee a globally optimal one (the effect of a choice ripples downstream).</details>

---

## ⚙️ World 7: The Clockwork Underground

**Q1.** What's the difference between a compiler and an interpreter?
<details><summary>Answer</summary>A compiler translates the whole program into machine code before execution. An interpreter interprets it step by step at runtime.</details>

**Q2.** List four or more levels of the memory hierarchy from fastest to slowest.
<details><summary>Answer</summary>Registers → L1/L2/L3 cache → main memory → SSD/disk.</details>

**Q3.** What are the two kinds of locality that make caches effective?
<details><summary>Answer</summary>Temporal locality (reusing the same data) and spatial locality (using adjacent data).</details>

**Q4.** What's the memory difference between a process and a thread?
<details><summary>Answer</summary>Processes have independent memory spaces. Threads share memory within the same process (but each has its own stack).</details>

**Q5.** Why is `0.1 + 0.2 == 0.3` false?
<details><summary>Answer</summary>Because 0.1 and 0.2 become infinitely repeating fractions in binary and carry rounding error.</details>

**Q6.** Why is array traversal measurably faster than linked-list traversal in practice (even though both are O(n))?
<details><summary>Answer</summary>Arrays are in contiguous memory so cache-line prefetching works, whereas a linked list is scattered and misses the cache almost every time.</details>

---

## 📡 World 8: The Sky City of Communication

**Q1.** What is the biggest difference between TCP and UDP?
<details><summary>Answer</summary>TCP guarantees delivery and ordering (connection-oriented, heavy). UDP has no such guarantees (connectionless, light and fast).</details>

**Q2.** What are the three packets in TCP's three-way handshake?
<details><summary>Answer</summary>SYN → SYN+ACK → ACK (synchronizing both sides' initial sequence numbers).</details>

**Q3.** Name three mechanisms by which TCP creates reliability.
<details><summary>Answer</summary>Sequence numbers restore ordering, ACKs and timeouts trigger retransmission, and checksums detect corruption (plus flow/congestion control).</details>

**Q4.** What does DNS do? What data structure does it resemble?
<details><summary>Answer</summary>A distributed database that looks up domain name → IP address. A hierarchical tree structure plus caching at each level.</details>

**Q5.** What does it mean that HTTP is "stateless"? How is login state maintained?
<details><summary>Answer</summary>Each request is independent and the server doesn't remember the previous one. State is held via cookies (session IDs) or tokens.</details>

---

## 🌌 World 9: The Logic Observatory Tower

**Q1.** Which is equivalent to P → Q — the converse, the inverse, or the contrapositive?
<details><summary>Answer</summary>Only the contrapositive (¬Q → ¬P).</details>

**Q2.** What are the two steps of mathematical induction?
<details><summary>Answer</summary>Base case (show P(0)) and inductive step (assume P(k) and show P(k+1)).</details>

**Q3.** What is the recurrence and complexity of the Euclidean algorithm?
<details><summary>Answer</summary>gcd(a,b) = gcd(b, a mod b). O(log min(a,b)).</details>

**Q4.** Why is the linearity of expectation so powerful?
<details><summary>Answer</summary>Because E[X+Y] = E[X]+E[Y] holds **even when X and Y are not independent** (you can add them despite complex dependencies).</details>

**Q5.** What does Cantor's diagonal argument show?
<details><summary>Answer</summary>That the real numbers cannot be numbered by the natural numbers (they are uncountable). It reappears later in the undecidability of the halting problem.</details>

---

## 🏛️ World 10: The OS Grand Temple

**Q1.** Why separate user mode and kernel mode?
<details><summary>Answer</summary>For isolation — to protect the hardware and other processes from a runaway or malicious app.</details>

**Q2.** Right after `fork()`, where do the parent and child continue execution?
<details><summary>Answer</summary>Both continue from the line after the fork (the parent gets the child's PID returned, the child gets 0).</details>

**Q3.** Why wrap a condition variable's wait in a while loop?
<details><summary>Answer</summary>Because of spurious wakeups and other threads stealing the resource, waking up doesn't guarantee the condition holds (you must re-check).</details>

**Q4.** What is a page fault? How is it resolved?
<details><summary>Answer</summary>An exception when the accessed page isn't in physical memory. The kernel reads it from disk, updates the page table, and re-executes the instruction (demand paging).</details>

**Q5.** What is thrashing?
<details><summary>Answer</summary>A state where, due to insufficient physical memory, pages are evicted and reloaded back and forth, and the CPU is mostly waiting on I/O.</details>

**Q6.** What principle lets journaling (WAL) maintain crash consistency?
<details><summary>Answer</summary>"Write the log before writing the change to the main data." On restart, committed changes are reapplied and incomplete ones are discarded.</details>

---

## 🗄️ World 11: The Great Library of Records

**Q1.** What are the four letters of ACID?
<details><summary>Answer</summary>Atomicity, Consistency, Isolation, Durability.</details>

**Q2.** Why is a B+ tree, rather than a BST, the standard DB index?
<details><summary>Answer</summary>Because it packs hundreds of keys into one node = one page, keeping the tree shallow and minimizing the number of disk I/Os.</details>

**Q3.** Physically, what has happened at "the moment of commit"?
<details><summary>Answer</summary>The moment the log containing the commit record is durably persisted to disk (fsync). Writing the data pages can happen later.</details>

**Q4.** Why does "a read not blocking a write" hold under MVCC?
<details><summary>Answer</summary>Because a write merely creates a new version, so the reader can keep reading the snapshot (the old version) as of its own start time.</details>

**Q5.** How does a hash join work?
<details><summary>Answer</summary>Build an in-memory hash table from the smaller table, then stream the larger one row by row to match against it (O(M+N)).</details>

---

## 🐉 World 12: The Language Forge

**Q1.** What are the six main stages of a compiler?
<details><summary>Answer</summary>Lexical analysis → parsing → semantic analysis → IR generation → optimization → code generation.</details>

**Q2.** Lexical analysis can be written with regular expressions, so why does parsing need a CFG?
<details><summary>Answer</summary>Because arbitrarily deep nesting, such as matching parentheses, can't be counted by finite states, and you need a CFG that has a stack (recursion).</details>

**Q3.** What mechanism makes `1 + 2 * 3` interpreted as `1 + (2*3)`?
<details><summary>Answer</summary>Operator precedence is embedded in the grammar's hierarchy (the rule for `*` sits deeper than the rule for `+`).</details>

**Q4.** What is the weakness of reference-counting GC?
<details><summary>Answer</summary>It can't reclaim cyclic references (when objects reference each other, their counts never reach 0).</details>

**Q5.** On what empirical rule is generational GC based?
<details><summary>Answer</summary>"Most objects die young." So it frequently does small collections of just the young generation.</details>

---

## 🔮 World 13: The Oracle of Computation

**Q1.** What's the difference in memory among a DFA, a PDA, and a Turing machine?
<details><summary>Answer</summary>A DFA has only finite states, a PDA adds one stack, and a TM adds an infinite tape it can freely read and write.</details>

**Q2.** What is the pumping lemma used to prove?
<details><summary>Answer</summary>That a certain language is **not** regular (e.g., aⁿbⁿ).</details>

**Q3.** What is the conclusion of the halting problem?
<details><summary>Answer</summary>No program exists that can decide, for any program and input, whether it halts (it is undecidable).</details>

**Q4.** What are the definitions of P and NP?
<details><summary>Answer</summary>P = solvable in polynomial time. NP = a certificate for the answer can be verified in polynomial time.</details>

**Q5.** Once you discover your problem is NP-complete, what should you do next?
<details><summary>Answer</summary>Give up on an exact polynomial solution and switch to approximation algorithms, heuristics, special cases, or branch and bound.</details>

---

## ⚗️ World 14: The Algorithm Colosseum

**Q1.** In the master theorem T(n)=aT(n/b)+O(n^d), what is the solution for merge sort (a=2, b=2, d=1)?
<details><summary>Answer</summary>Since d = log_b a = 1, it's O(n^d log n) = O(n log n).</details>

**Q2.** What is the classic argument for proving the correctness of a greedy algorithm?
<details><summary>Answer</summary>The exchange argument (show that swapping the optimal solution's choice for the greedy choice doesn't make it worse).</details>

**Q3.** What data structure does Kruskal's algorithm use for cycle detection?
<details><summary>Answer</summary>Union-Find (the disjoint-set data structure).</details>

**Q4.** What are the "back edges" in a residual graph for?
<details><summary>Answer</summary>To undo flow once sent and reroute it along a different path (to atone for a greedy mistake).</details>

**Q5.** What's the difference between Las Vegas and Monte Carlo randomized algorithms?
<details><summary>Answer</summary>Las Vegas = the answer is always correct but the time varies. Monte Carlo = the time is fixed but the answer is occasionally wrong.</details>

---

## ☁️ GRAD 1: The Sky Parliament of Distribution

**Q1.** State the CAP theorem precisely.
<details><summary>Answer</summary>While a network partition (P) is occurring, consistency (C) and availability (A) cannot both be satisfied. In normal times you can provide both.</details>

**Q2.** Why is "it timed out, so the other side is dead" dangerous?
<details><summary>Answer</summary>The other side may be alive and just slow, and you can't tell the difference. A misjudgment can cause split-brain.</details>

**Q3.** With 5 Raft nodes, how many failures can it tolerate while continuing to accept writes?
<details><summary>Answer</summary>2 (a majority of 3 remains). That's why you make clusters odd-numbered.</details>

**Q4.** How does "overlapping majorities" support safety?
<details><summary>Answer</summary>Any two majorities necessarily overlap, so a candidate that lacks a committed entry can't be elected.</details>

**Q5.** Why is the consistency allowed for a "like count" different from that for an "inventory count"?
<details><summary>Answer</summary>A stale like count causes no real harm, so eventual consistency is enough. A stale inventory value read concurrently causes the real harm of double-selling, so it needs strong consistency.</details>

---

## 🛡️ GRAD 2: The Sky Fortress of Security

**Q1.** What is Kerckhoffs's principle?
<details><summary>Answer</summary>The algorithm may be public. Keep only the key secret (security through obscurity is fragile).</details>

**Q2.** Why store passwords "hashed" rather than "encrypted"?
<details><summary>Answer</summary>Encryption can be reversed if you have the key, but hashing is one-way and not even the server needs to know the original. Protect with a salt + a slow hash (bcrypt, etc.).</details>

**Q3.** On what mathematical hardness does RSA's security rely?
<details><summary>Answer</summary>The hardness of factoring large composite numbers (the quantum Shor's algorithm is a threat).</details>

**Q4.** What is the common root cause of SQL injection and buffer overflow?
<details><summary>Answer</summary>A blurred boundary between data and code (instructions/syntax). The defense is separation (prepared statements, bounds checking).</details>

**Q5.** What does forward secrecy protect?
<details><summary>Answer</summary>Even if the long-term key leaks in the future, past communications are protected thanks to disposable session keys.</details>

---

## 🔭 GRAD 3: The Observatory of Intelligence

**Q1.** What is the essential goal of machine learning?
<details><summary>Answer</summary>To do well on data it has never seen (generalization). Rote-memorizing the training data is not learning.</details>

**Q2.** What is the update rule of gradient descent?
<details><summary>Answer</summary>w ← w − η · ∂Loss/∂w (η is the learning rate = step size).</details>

**Q3.** What is overfitting? How do you detect it?
<details><summary>Answer</summary>The phenomenon of memorizing even the noise in the training data and missing on unseen data. Detect it by the gap between training accuracy and validation accuracy.</details>

**Q4.** Why is a nonlinear activation essential in a neural network?
<details><summary>Answer</summary>Because stacking any number of linear transformations collapses into a single linear transformation, adding no expressive power.</details>

**Q5.** What is backpropagation doing mathematically?
<details><summary>Answer</summary>It recursively applies the chain rule (the derivative of composite functions) over the computation graph from output toward input, computing the gradient of each weight.</details>

**Q6.** Why do LLMs "confidently get things wrong," and how do you cope?
<details><summary>Answer</summary>Because they're trained to pick probabilistically "plausible" words with no guarantee of factuality (hallucination). Cope by checking sources and human supervision.</details>

---

## ⚛️ GRAD 4: The Theory of Everything

**Q1.** The ISA (instruction set architecture) is a "contract" between what and what?
<details><summary>Answer</summary>A contract between hardware and software. As long as it's honored, the same program runs on different implementations.</details>

**Q2.** What is lost when branch prediction misses? Why are loops easy to predict?
<details><summary>Answer</summary>The cycles spent discarding the speculatively executed instructions and re-running the pipeline. Loops "continue" most of the time, so the prediction keeps being right.</details>

**Q3.** What is the formula and lesson of Amdahl's law?
<details><summary>Answer</summary>Speedup = 1/((1−p)+p/n). The sequential portion (1−p) sets the ceiling, so reducing the sequential bottleneck is more fundamental than adding cores.</details>

**Q4.** What does cache coherence guarantee?
<details><summary>Answer</summary>It keeps the copies of the same data across multiple cores' caches consistent so you don't read a stale value.</details>

**Q5.** Why does false sharing happen?
<details><summary>Answer</summary>Because logically unrelated variables share the same cache line (64B), and updating one invalidates the entire line.</details>

---

## 🏆 The Wisdom of Clearing the Temple of Memory

Once you can **say 80% of these cards with nothing in front of you**, your knowledge has shifted from "read" to "internalized."

| Study Method | Effectiveness |
|---|---|
| Just rereading | Weak (you only feel like you understand) |
| **Active recall** (these cards) | Strong (the act of recalling cements memory) |
| **Spaced repetition** (re-attempt after a gap) | Strongest (recalling right before you'd forget makes it stick) |

> Words of the elder: "One who has truly learned a concept can speak of it even with the textbook closed.
> These cards are the only bridge that carries you to that 'can speak even when closed' state.
> Don't solve them once and be done. **Do them again when you've forgotten.** That is the law of the Temple of Memory."

➡️ Back: [CS Quest Home](README.md) ・ [Implementation Quest Solutions](appendix-04-implementation-solutions.md)
