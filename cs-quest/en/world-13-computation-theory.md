# 🔮 World 13: The Oracle of Computation — Automata, Computability, Complexity

> At the edge of the continent, an ancient oracle floats amid the mist.
> The question asked here is not "how do we compute?"
> It is **"can this even be solved by computation at all?" and "can it be solved in realistic time?"** ——
> A place inscribed with the prophecies of those who saw the limits of computers
> (Turing, Gödel, Cook) before computers even existed.

**Corresponding university courses**: MIT **6.045 / 18.404 (Sipser)** / textbook *Introduction to the Theory of Computation* (Sipser)
**Prerequisites**: World 9 (the diagonal argument & proof techniques), World 12 (the practical side of regular expressions and CFGs)

**What you'll learn in this chapter**
- Finite automata (DFA/NFA) and regular languages
- The pumping lemma — proving that something "can't be done"
- Context-free grammars and the Chomsky hierarchy
- Turing machines, computability, and the halting problem
- P and NP, NP-completeness

---

## 📖 Lecture 1: The Smallest Priest — Finite Automata (15 XP)

A **DFA (deterministic finite automaton)** is the smallest machine, having only a finite number of states and transition rules.
It has no memory. The "state" it is in right now is everything.

Example: a DFA that accepts "binary strings with an even number of 1s":

```
        1
  ●(even) ⇄ ○(odd)     ← ● is both the start and the accepting state
        1
  (reading a 0 returns to itself)
```

- The languages a DFA can accept = **regular languages** = **languages expressible by regular expressions** (the equivalence is provable)
- An **NFA (nondeterministic)** can "try multiple transitions at once," but its **expressive power is the same as a DFA's**
  (it can be converted to a DFA via the subset construction, though the number of states may blow up exponentially)
- It's thanks to this theory that World 12's lexer can be written with regular expressions. `grep`'s speed is also a gift of DFAs

## 📖 Lecture 2: The Prophecy "You Cannot" — The Pumping Lemma (15 XP)

One of the most important skills in CS is **proving that something can't be done**.

**Pumping lemma (intuitive version)**: since a DFA has finitely many states, reading a sufficiently long string
**must pass through some state twice** (the pigeonhole principle! a tool from World 9).
Repeating that loop part any number of times should not change the acceptance result.

**A classic: L = { aⁿbⁿ } is not a regular language**
If a DFA existed, it would also accept a string formed by repeating the loop part (the a-only segment) of a long aⁿbⁿ twice.
But that's a string where the number of a's and b's don't match — contradiction. ∎

In other words, **"counting matched parentheses" is fundamentally impossible with finite states**.
The reason we said in World 12 that "a parser needs a CFG" has now become a theorem here.

## 📖 Lecture 3: The Prophecy of the Hierarchy — The Chomsky Hierarchy (15 XP)

| Level | Language class | Recognizing machine | Example |
|---|---|---|---|
| 3 | Regular languages | DFA / NFA | Tokens, `aⁿ` |
| 2 | Context-free languages | Pushdown automaton (DFA + **stack**) | `aⁿbⁿ`, program syntax |
| 1 | Context-sensitive languages | Linear bounded automaton | `aⁿbⁿcⁿ` |
| 0 | Recursively enumerable languages | **Turing machine** | Everything computable |

The more memory you give the machine, the wider the class of languages it can recognize.
A single stack can count `aⁿbⁿ` but not `aⁿbⁿcⁿ` — the shape of the memory determines the capability.

## 📖 Lecture 4: The Universal God — Turing Machines and the Halting Problem (15 XP)

A **Turing machine (TM)** = finite states + an infinitely long tape + a read/write head.
With just this, your PC, and even a quantum computer (in the sense of computability), and all of "computation" can be reproduced.

- **Church-Turing thesis**: "computable by an algorithm" = "computable by a TM" (more a belief than a definition. But no counterexample in 90 years)
- **Universal TM**: it can take the description of another TM as input and simulate it — **treating a program as data**, the foundational idea of modern computers

### The Halting Problem — The Innermost Sanctum of the Oracle

> **"There is no program H that, for an arbitrary program P and input x, decides whether P(x) halts."**

**Proof (diagonal argument — paying off the setup from World 9)**:
Assume H exists, and build a contrarian D:
"D(P) **deliberately loops forever** if H says 'P(P) halts,' and **halts immediately** if H says 'it doesn't halt.'"
Now, does D(D) halt? — Either assumption leads to a contradiction. Therefore H does not exist. ∎

**Prophecy for practice**: a perfect infinite-loop detector, a perfect static analyzer, a perfect virus detector are **fundamentally impossible to build**
(Rice's theorem: deciding any semantic property of programs is undecidable).
So real-world tools fight with "approximations" — accepting false positives and false negatives.

## 📖 Lecture 5: The Last Unsolved Prophecy — P vs NP (15 XP)

- **P**: problems a deterministic TM can solve in **polynomial time** (= the theoretical definition of "realistically solvable")
- **NP**: problems where, given a candidate answer (a certificate), you can **verify it in polynomial time**
  - Example: Sudoku — solving it seems hard, but checking the answer sheet is instant
- **P ⊆ NP** is obvious (if you can solve it you can verify it). **Is P = NP?** is the million-dollar open problem

### NP-complete — The Equivalence Class of "the Hardest"

**Cook-Levin theorem**: SAT (is there an assignment that makes a logical formula true?) can be **reduced** in polynomial time
from any problem in NP (NP-complete).
That means **if SAT can be solved in P, then all of NP becomes P**.

Through a chain of reductions from SAT, the traveling salesman, vertex cover, 3-coloring, knapsack (its decision version),
subset sum… thousands of practical problems have turned out to be NP-complete.

**Prophecy for practice**: once you can show your problem is NP-complete, stop searching for an exact polynomial solution and
switch to **approximation algorithms, heuristics, exponential-but-clever search (branch and bound), or special cases**.
"Knowing how to give up" is the value of the degree.

---

## ⚔️ Quests

### Quest 1: Designing the Priest (30 XP)

Draw a DFA (as a state-transition diagram) that accepts each of the following languages.

1. Strings of 0s and 1s that end in `01`
2. Binary strings representing multiples of 3 (hint: state = "the value so far mod 3")

<details>
<summary>📜 Hint (2)</summary>

States q0, q1, q2 (the remainder mod 3). Reading a bit b makes the value 2× + b, so the transition is qᵣ →(b)→ q₍₂ᵣ₊ᵦ₎ ₘₒ𝒹 ₃. The accepting state is q0.
</details>

### Quest 2: Training in Proving "It Can't Be Done" (30 XP)

Using the pumping lemma (the argument about the finiteness of states and loops),
prove that **"the set of all correctly matched parenthesis strings" is not a regular language**.
(Hint: consider `(ⁿ)ⁿ`. Just trace the proof for aⁿbⁿ.)

### Quest 3: 💻 Implementation Quest — "Build the Priest" (50 XP)

Implement the "multiple-of-3 DFA" from Quests 1-2 in code
(a state-transition table + a loop that reads one character at a time. Be amazed that this alone decides divisibility without doing any division).
Then generalize it into a **general-purpose DFA simulator** that takes an arbitrary transition table.

### Quest 4: Decoding the Prophecy (30 XP)

1. Correct your junior's misconception that "NP = problems that take exponential time" (what is the correct definition of NP?).
2. To show that a problem X is NP-complete, what two things must you show?
3. Even though the halting problem is undecidable, "does this program halt within 10⁶ steps?" is decidable. Why?

<details>
<summary>📜 Answer</summary>

1. NP is the class of "polynomial time on a nondeterministic TM" = "**a certificate can be verified in polynomial time**." It has not been proven to take exponential time to solve (that's exactly P vs NP).
2. ① X ∈ NP (polynomial-time verification of a certificate) ② a polynomial-time reduction to X from a known NP-complete problem (such as SAT).
3. Just actually simulating 10⁶ steps always produces an answer in finite time. What's undecidable is when you ask about an "unbounded future."
</details>

---

## 👹 Boss Battle: The Oracle Master "Oracle, High Priest of Truth" (150 XP)

Close your notes and challenge it. 70%+ to win.

1. State the difference in power among DFA, PDA, and TM, along with the difference in their memory.
2. Write the proof, via the pumping lemma, that "aⁿbⁿ is not regular."
3. Write the proof of the undecidability of the halting problem, from the construction of the contrarian D to the contradiction.
4. Define the four terms "P," "NP," "NP-complete," and "NP-hard" precisely.
5. What does the Cook-Levin theorem assert? Why does it become "the starting point for reductions"?
6. A colleague is fretting, "I just can't solve this optimization problem in polynomial time." Propose three correct courses of action using knowledge of NP-completeness.
7. What lesson does Rice's theorem give for the design of static analysis tools?

<details>
<summary>📜 Skeleton of the answer</summary>

1. DFA: finite states only (regular languages). PDA: + a single stack (context-free languages). TM: + an infinite tape it can read and write freely (everything computable).
2. As in Lecture 2. Feed a^p b^p to a DFA with p states, and a state must repeat within the a-segment; pumping the loop, a^(p+k) b^p is also accepted — contradiction.
3. As in Lecture 4. Assume H exists → construct D → both assumptions about D(D) halting/not-halting contradict H's answer → H does not exist.
4. P: solvable in deterministic polynomial time. NP: a certificate can be verified in polynomial time. NP-hard: every problem in NP reduces to it in polynomial time (it need not belong to NP). NP-complete: NP-hard and in NP.
5. The assertion that SAT is NP-complete (the computation of any problem in NP can be encoded as a logical formula). Once the first NP-complete problem was established, from then on you can show a new problem's NP-completeness just by "a reduction from SAT (or a known NP-complete problem)."
6. ① Confirm the problem's NP-completeness by reduction and abandon the search for an exact polynomial solution ② Consider approximation algorithms or heuristics (local search, simulated annealing) ③ Consider exact methods or branch and bound that exploit special structure of the input (small size, tree structure, planarity, etc.).
7. You can't build a tool that "always correctly decides the semantic property of an arbitrary program." You must explicitly choose a trade-off at design time: either sound but over-warning (false positives), or complete but with misses (false negatives).
</details>

---

🏆 **Victory reward**: Badge "🔮 One Who Sees the Limits" + 150 XP

➡️ Next: [World 14: The Algorithm Colosseum](world-14-advanced-algorithms.md)
