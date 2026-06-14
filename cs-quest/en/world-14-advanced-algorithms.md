# ⚗️ World 14: The Algorithm Colosseum — Advanced Algorithm Design

> The last trial of the Second Continent is the great colosseum where heroes of every age competed.
> In Worlds 1–6 you learned individual techniques. Here you learn **schools of style** ——
> divide and conquer, greedy, randomized, approximation.
> And every school comes with **a proof of why it is correct.**
> You may not enter without the sword you forged in World 9 (proof techniques).

**University equivalent**: MIT **6.046 Design and Analysis of Algorithms** / Berkeley **CS170** / textbook CLRS
**Prerequisites**: Worlds 1–6, World 9

**What you'll learn in this chapter**
- The Master Theorem and analysis of divide and conquer
- Greedy algorithms and correctness via exchange arguments
- Minimum spanning trees (Kruskal / Prim)
- Maximum flow / minimum cut
- Randomized algorithms
- Approximation algorithms (the practical art of "how to give up" from World 13)

---

## 📖 Lecture 1: The Secret of the Divide-and-Conquer School — The Master Theorem (15 XP)

The divide-and-conquer recurrence **T(n) = a·T(n/b) + O(n^d)** (a subproblems, size 1/b, combine cost n^d) has the solution:

| Condition | Solution | Intuition |
|---|---|---|
| d > log_b a | T(n) = O(n^d) | The root (combine cost) dominates |
| d = log_b a | T(n) = O(n^d log n) | Every level pays the same amount |
| d < log_b a | T(n) = O(n^(log_b a)) | The leaves (number of subproblems) dominate |

**Instant verdict**: Mergesort T(n)=2T(n/2)+O(n) → a=2,b=2,d=1, log₂2=1=d → **O(n log n)** ✓
Binary search T(n)=T(n/2)+O(1) → **O(log n)** ✓

**Karatsuba's algorithm (a divide-and-conquer monument)**: multiplying two n-digit numbers naively needs four half-size multiplications,
T(n)=4T(n/2)+O(n)=O(n²). But an algebraic trick reduces it to **3 multiplications**,
giving T(n)=3T(n/2)+O(n)=O(n^log₂3)≈**O(n^1.585)**.
"Just removing one subproblem" wins asymptotically —— burn the divide-and-conquer mindset into your body.

## 📖 Lecture 2: The Greedy School — "Greed With a Proof" (15 XP)

Greedy = make the locally best choice at each step and never look back.
**Fast, but correctness is not obvious.** The classic proof tool is the **exchange argument**:

> "If the optimal solution differs from the greedy one, show that **swapping the optimum's choice for the greedy choice does not make it worse.**
> Repeated swaps transform the optimum into the greedy solution. Hence the greedy solution is also optimal."

### Masterpiece 1: Interval Scheduling
From n talks, pick the largest non-overlapping set. **"Pick the one that finishes earliest"** is optimal.
(Exchange argument: swapping the optimum's first talk for the "earliest finishing" one only widens, never narrows, the remaining room.)

### Masterpiece 2: Huffman Coding
Build an optimal variable-length code (tree) from frequencies: **repeatedly merge the two least-frequent items** (with World 3's min-heap, O(n log n)).
The foundational compression theory still working inside ZIP and JPEG today.

### Masterpiece 3: Minimum Spanning Tree (MST)
A tree connecting all vertices at minimum cost.

- **Kruskal's algorithm**: scan edges lightest first and **accept if it forms no cycle** — cycle detection is Union-Find (the resident of Hidden Dungeon 5 promoted to the regular army). O(E log E)
- **Prim's algorithm**: start at one vertex and keep choosing the lightest edge connecting the tree to the outside with a min-heap (Dijkstra's sibling)
- Correctness is the **cut property**: "no matter how you split the vertices into two sets, the lightest edge crossing between them belongs to some MST"

## 📖 Lecture 3: The Martial Art of Flow — Max Flow and Min Cut (15 XP)

Each edge of a directed graph has a capacity. How much can you push from source s to sink t?

**Ford–Fulkerson method**: on the **residual graph** (remaining capacity + reverse "push-back" edges),
repeatedly find an augmenting s→t path and push flow, until no augmenting path remains.
The reverse edges allow "undoing a previous decision" —— a mechanism that atones for greedy's mistakes in flow.

**Max-Flow Min-Cut Theorem**: the maximum flow value = the minimum capacity of an edge set separating s and t.
"The network's weak point (bottleneck)" and "the limit you can push" are two sides of the same coin.

**The breadth of applications is the real point**: bipartite matching (assigning students to labs), image segmentation,
baseball-league championship feasibility —— the eye that notices "this can be solved with flow" is your 6.046 diploma.

## 📖 Lecture 4: The Randomized School — Making Dice a Weapon (15 XP)

- **Las Vegas type**: the answer is always correct, the running time is up to luck (e.g. randomized quicksort — **expected** O(n log n) on any input, denying the adversary a worst-case input)
- **Monte Carlo type**: the time is fixed, the answer is occasionally wrong (e.g. Miller–Rabin primality testing — error probability drops to 4⁻ᵏ with repetition, used every day in cryptographic key generation)

**Randomized quickselect**: get "the k-th value" in expected O(n) without sorting.
The star of the analysis is World 9's **linearity of expectation** —— watch the sword of mathematics cut through an algorithm.

**Universal hashing**: pick a hash function randomly from a family and you can guarantee expected O(1) against any adversarial key set.
World 2's "average O(1)" now has a theoretical foundation.

## 📖 Lecture 5: The Approximation School — The Art of Giving Up Correctly (15 XP)

The sequel to World 13's oracle: "if it's NP-complete, give up on an exact polynomial solution."
**Approximation algorithms** = solutions that **guarantee** "within a factor α of the optimum" in polynomial time.

### Masterpiece: 2-Approximation for Vertex Cover
Just pick an arbitrary edge, **take both endpoints**, delete the covered edges, and repeat.
Proof: the edges you picked share no endpoints (a matching), so the optimum must take at least one point from each edge.
We took two points each → at most twice as many. ∎ —— the elegance is **proving the ratio without knowing the optimum's size.**

### Masterpiece: 2-Approximation for Metric TSP (triangle inequality holds)
Build an MST (Lecture 2!), walk its perimeter, skip repeated vertices.
Tour ≤ 2 × MST ≤ 2 × optimal tour.

**Summary of design styles**: exact DP / divide-and-conquer → greedy (fastest if provable) → randomized → approximation → heuristics.
Being able to look at a problem and **choose which school to take a stance in** is the mark of an advanced player.

---

## ⚔️ Quests

### Quest 1: Master Theorem Practice Swings (30 XP)

Solve the following recurrences.

1. T(n) = 4T(n/2) + O(n)
2. T(n) = 2T(n/2) + O(n²)
3. T(n) = 3T(n/3) + O(n)
4. Why is Karatsuba's recurrence T(n) = 3T(n/2) + O(n)? Write out the three partial products.

<details>
<summary>📜 Answers</summary>

1. log₂4 = 2 > 1 → **O(n²)** (leaves dominate)
2. d=2 > log₂2=1 → **O(n²)** (root dominates)
3. log₃3 = 1 = d → **O(n log n)**
4. For x = a·2^(n/2) + b, y = c·2^(n/2) + d, computing xy needs ac, bd, and (ad+bc); since ad+bc = (a+b)(c+d) − ac − bd, only three multiplications (ac, bd, (a+b)(c+d)) are required.
</details>

### Quest 2: Exchange Argument Training (30 XP)

Prove, **in your own words**, the correctness of the "pick the earliest finish time" greedy for interval scheduling, using an exchange argument.
(The flow: "swapping the optimum's first choice for the greedy first choice causes no contradiction" → inductively swap them all.)

### Quest 3: 💻 Implementation Quest "Match of the Three Schools" (70 XP)

1. Implement **Kruskal's algorithm** with Union-Find and find the MST of a ~5-vertex graph
2. Implement **randomized quickselect** (the k-th smallest, expected O(n))
3. Implement the **vertex cover 2-approximation** and compare its ratio to the brute-force optimum on a small graph

### Quest 4: The Eye for Flow (30 XP)

1. "n applicants and m jobs, each person has a set of jobs they can apply to. How many pairs can be matched at most?" Formulate this as a flow problem (with a diagram: source, sink, capacities).
2. Using the max-flow min-cut theorem, the maximum matching is upper-bounded by "the size of some set." Which set?

<details>
<summary>📜 Answers</summary>

1. Source s → each applicant (capacity 1), applicant → each applicable job (capacity 1), each job → sink t (capacity 1). Max flow value = maximum matching count.
2. The minimum cut. For example, the size of "an edge set separating s/t by choosing some applicants and some jobs." König's theorem (in a bipartite graph, max matching = min vertex cover) is this special case.
</details>

---

## 👹 Boss Battle: The Colosseum Champion, "Grandmaster Algo" (150 XP)

Close your notes and fight. Win with 70% or more.

1. State the three cases of the Master Theorem, with intuition for "where in the tree the cost dominates."
2. Describe the exchange-argument skeleton that justifies greedy algorithms in three sentences.
3. Describe Kruskal's algorithm and the data structure used for cycle detection, with its complexity.
4. Why do "reverse edges" exist in the residual graph? Draw a graph where naive greedy (without reverse edges) fails.
5. Explain the difference between Las Vegas and Monte Carlo types, with examples.
6. Reproduce the proof of the vertex cover 2-approximation.
7. When you meet a new problem, in what order do you consider exact methods through approximation/heuristics, and by what criteria?

<details>
<summary>📜 Answer outline</summary>

1. See Lecture 1's table. d > log_b a: the root's combine cost dominates / equal: every level contributes equally across log n levels / d < log_b a: the leaf count a^(log_b n) = n^(log_b a) dominates.
2. Take the first choice where the optimum OPT differs from the greedy solution G, and show that swapping OPT's choice for G's does not degrade quality. Repeating this transforms OPT into G, so G is optimal.
3. Sort edges by ascending weight; if the two endpoints are in different sets, accept and union them. Cycle detection uses Union-Find (path compression + union by rank), about O(α(n)) ≈ constant per operation, O(E log E) overall (dominated by the sort).
4. To partially undo a previously routed flow and reroute it along a different path. Example: s→a→t and s→b→t each capacity 1, plus a→b capacity 1; routing s→a→b→t first gets stuck at 1 without reverse edges, but the true max flow is 2.
5. Las Vegas: output is always correct but time is a random variable (randomized quicksort). Monte Carlo: time is deterministic but there's an error probability (Miller–Rabin); error probability can be driven down exponentially by repetition.
6. The accepted edge set is a matching (endpoint-disjoint). The optimal cover must include at least one endpoint per edge, so |OPT| ≥ matching size k. Our solution is 2k, hence 2k ≤ 2|OPT|.
7. ① Check problem size and structure (small → brute force / even exponential is fine) ② Seek a polynomial exact solution via DP/divide-and-conquer/greedy (with proof) ③ If it looks NP-complete, confirm by reduction ④ If an approximation ratio guarantee is needed, use an approximation algorithm; otherwise heuristics like local search ⑤ If there's special structure (tree, planar, small integers), use pseudo-polynomial DP or a specialized solver.
</details>

---

🏆 **Victory Reward**: Badge "⚗️ Master of All Schools" + 150 XP — **Second Continent conquered!**

➡️ Ascend to the Heavens (Graduate Level): [GRAD 1: The Sky Parliament of Distribution](grad-01-distributed-systems.md)
