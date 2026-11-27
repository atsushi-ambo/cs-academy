# 🌌 World 9: The Logic Observatory Tower — Discrete Math and Proofs

> At the entrance to the Second Continent, a tower piercing the starry sky rises up.
> The tower's sage says: "On the continents beyond here, **'code that runs' alone won't earn you passage.
> I demand what can be *proven correct*.** A proof is an argument that no one, however they read it, can refute."
>
> This is the tower where every CS scholar holes up at least once — the place to learn mathematics, the mother tongue of computer science.

**Corresponding university courses**: MIT **6.042J Mathematics for Computer Science** / Berkeley **CS70**
**Prerequisites**: Clear Worlds 1–8

**What you'll learn in this chapter**
- Propositional and predicate logic
- The four proof techniques (direct, contrapositive, contradiction, mathematical induction)
- Sets, relations, functions, countable and uncountable
- Number theory (mod, greatest common divisor) — foreshadowing cryptography
- Combinatorics and discrete probability

---

## 📖 Lecture 1: The Language of the Stars — Logic (15 XP)

A **proposition** is a statement that has a definite truth value. We build them up with logical connectives:

| Symbol | Read as | Meaning |
|---|---|---|
| ¬P | NOT | not P |
| P ∧ Q | AND | both true |
| P ∨ Q | OR | at least one is true |
| P → Q | implies | false only when P is true but Q is false |
| P ↔ Q | iff | truth values match |

**The relatives of P → Q (mix them up and you fall off the tower)**:
- **Converse** Q → P …… does not necessarily hold
- **Inverse** ¬P → ¬Q …… does not necessarily hold
- **Contrapositive** ¬Q → ¬P …… **completely equivalent to the original** (a star player in proofs)

**Predicate logic**: ∀x (for all x), ∃x (there exists an x such that).
Rule for negation: ¬∀x P(x) ≡ ∃x ¬P(x). "Not everyone is correct" = "there is at least 1 person who is wrong."

This is familiar to programmers: `!(a && b) == (!a || !b)` (De Morgan's laws).
Logic is the very grammar of conditional expressions, loop invariants, and specifications in code.

## 📖 Lecture 2: The Sage's Four Swords — Proof Techniques (15 XP)

### 🗡️ Direct Proof
Assume P, and walk all the way to Q using only definitions and known theorems.
Example: "even + even = even" — 2a + 2b = 2(a+b). Done.

### 🗡️ Proof by Contrapositive
Instead of P → Q, show ¬Q → ¬P.
Example: "if n² is even then n is even" ← the contrapositive "if n is odd then n² is odd" falls right out of (2k+1)² = 2(2k²+2k)+1.

### 🗡️ Proof by Contradiction
Negate the conclusion and derive a contradiction.
**A masterpiece: √2 is irrational** — assume √2 = a/b (a fraction in lowest terms). Then a² = 2b² means a is even; setting a = 2c, we get b² = 2c², so b is even too. This contradicts the fraction being in lowest terms. ∎

### 🗡️ Mathematical Induction — CS's Strongest Sword
1. **Base case**: show P(0)
2. **Inductive step**: assume P(k) and show P(k+1)
3. Then P(n) holds for all n

**Strong induction** is a variant where you may assume "all of P(0) through P(k)."
Proofs of the correctness of recursive algorithms, of loop invariants, and of data-structure invariants are almost all induction.
The recursion and induction of World 6 are two sides of the same coin (base case = base case, recursive case = inductive step).

## 📖 Lecture 3: Gatherings of Stars — Sets, Functions, Infinity (15 XP)

- **Sets**: union ∪, intersection ∩, difference \, complement, power set P(S) (the set of all subsets; |P(S)| = 2^|S|)
- **Relations**: a relation satisfying reflexivity, symmetry, and transitivity all at once is an **equivalence relation** (e.g., congruence mod 5). It **partitions a set into equivalence classes**
- **Functions**: injective (nothing collapses) / surjective (covers everything) / bijective (a perfect one-to-one correspondence)
- **Cardinality**: sets between which a bijection can be built are "the same size." The naturals and the even numbers are the same size (n ↔ 2n)!

**Cantor's diagonal argument**: the real numbers cannot be numbered by the naturals (they are uncountable).
However you arrange the infinite sequences of 0s and 1s, the sequence obtained by "flipping the i-th digit of the i-th row" appears nowhere in the table.
—— This argument reappears in World 13 as the **undecidability of the halting problem**. Remember this foreshadowing.

## 📖 Lecture 4: The Constellations of Integers — Introduction to Number Theory (15 XP)

- **Congruences**: a ≡ b (mod m) ⟺ m divides a − b. "Clock arithmetic in the world of mod"
- **Greatest common divisor**: the **Euclidean algorithm** gcd(a, b) = gcd(b, a mod b). O(log min(a,b)) — the fastest algorithm, still in active service since antiquity
- **Extended Euclidean algorithm**: finds integers x, y such that gcd(a, b) = ax + by → used to compute the **modular inverse**
- **Fermat's little theorem**: if p is prime and gcd(a,p)=1, then a^(p−1) ≡ 1 (mod p)

These are not decorations. **RSA encryption (which you'll conquer in the graduate chapter) can be assembled from nothing but the tools of this lecture.**
The design of hash functions, random number generation, and error-correcting codes all stand on number theory.

## 📖 Lecture 5: The Star Chart of Counting and Wagers — Combinatorics and Probability (15 XP)

### The four tools of counting
- **Product rule**: independent choices multiply
- **Permutations** P(n,k) = n!/(n−k)! / **Combinations** C(n,k) = n!/(k!(n−k)!)
- **Pigeonhole principle**: put n+1 pigeons into n holes and some hole must contain 2 (simple yet powerful: "in Tokyo there must be 2 people with exactly the same number of hairs")
- **Inclusion–exclusion**: |A ∪ B| = |A| + |B| − |A ∩ B|

### Discrete probability
- **Conditional probability** P(A|B) = P(A∩B)/P(B), **Bayes' theorem** P(A|B) = P(B|A)P(A)/P(B)
- **Linearity of expectation**: E[X+Y] = E[X] + E[Y] holds **even without independence** —— the ultimate weapon for analyzing randomized algorithms
- **The birthday paradox**: with 23 people, the probability of a shared birthday is > 50%.
  This is why hash collisions happen "far sooner than you'd think," and why cryptographic hashes need as many as 256 bits (a collision can be found in √N = 2^128 tries)

---

## ⚔️ Quests

### Quest 1: Training with the Four Swords (30 XP)

Prove each one with the designated sword.

1. (Direct) The square of an odd number is odd
2. (Contrapositive) For an integer n, if 3n + 2 is odd then n is odd
3. (Contradiction) There are infinitely many primes (Hint: assume there are finitely many p₁…pₖ and consider p₁p₂…pₖ + 1)
4. (Induction) 1 + 2 + ⋯ + n = n(n+1)/2

<details>
<summary>📜 Skeleton of the solutions</summary>

1. (2k+1)² = 4k² + 4k + 1 = 2(2k² + 2k) + 1 — the form of an odd number.
2. Contrapositive "n even ⇒ 3n + 2 is even": if n = 2k then 3n + 2 = 2(3k + 1).
3. Assuming finitely many, form N = p₁⋯pₖ + 1; then N is divisible by none of the pᵢ (remainder 1). A prime factor of N is a newcomer not on the list — contradiction.
4. Base n=1: 1 = 1·2/2 ✓. Induction: 1+⋯+k+(k+1) = k(k+1)/2 + (k+1) = (k+1)(k+2)/2 ✓.
</details>

### Quest 2: Prove an Algorithm Correct (30 XP)

Prove that the "binary search" you implemented in World 2 is correct, using the **loop invariant**
"if the value being searched for exists, it is always within the interval [lo, hi]"
(write it in 3 parts: initialization, maintenance, termination. This is the real way of CS).

### Quest 3: 💻 Implementation Quest "The Art of Stellar Computation" (50 XP)

1. Implement the Euclidean algorithm and the extended Euclidean algorithm
2. Implement `mod_pow(a, n, m)` (aⁿ mod m in O(log n)) using repeated squaring
3. Using #2, find 7⁻¹ mod 26 (check: 7 × your answer ≡ 1 (mod 26))

### Quest 4: The Gambler's Catechism (30 XP)

1. When you roll 2 dice, what is the probability the sum is 7?
2. A test flags a sick person as positive 99% of the time, and also wrongly flags a healthy person as positive 1% of the time. If 0.1% of the population is afflicted, use Bayes to find the probability that someone who tested positive is actually sick (be amazed at the gap from intuition).
3. At a party of n people, everyone randomly exchanges presents. Use linearity of expectation to find the expected number of people whose own present comes back to them.

<details>
<summary>📜 Solutions</summary>

1. 6 out of 36 outcomes = **1/6**.
2. P(sick|positive) = (0.99 × 0.001) / (0.99 × 0.001 + 0.01 × 0.999) ≈ **9%**. Even when positive, 90% are healthy! (a sea of false positives)
3. For each person i, the indicator variable Xᵢ for "comes back to me" has E[Xᵢ] = 1/n. By linearity, E[ΣXᵢ] = n × 1/n = **1 person**. Independent of n!
</details>

---

## 👹 Boss Battle: "Logic Dragon, the Proof Wyrm" at the Tower's Summit (150 XP)

Close your notes and take it on. Win with 70% or more.

1. Write the converse, inverse, and contrapositive of P → Q, and state which one is equivalent to the original proposition.
2. Prove by contradiction that √3 is irrational.
3. Use induction to prove "2ⁿ > n when n ≥ 1."
4. Explain the core of Cantor's diagonal argument (why the new sequence is necessarily not in the table) in 3 sentences or fewer.
5. Compute gcd(252, 105) via the Euclidean algorithm, showing every step.
6. Critique the claim "with a 64-bit hash, collisions basically never happen" using the birthday paradox.
7. State, with one example, why the fact that linearity of expectation "assumes no independence" is so powerful in algorithm analysis.

<details>
<summary>📜 Skeleton of the solutions</summary>

1. Converse Q→P, inverse ¬P→¬Q, contrapositive ¬Q→¬P. The equivalent one is **only the contrapositive**.
2. Assume √3 = a/b (lowest terms). Then a² = 3b² → a is a multiple of 3 (since 3 is prime) → a=3c → b² = 3c² → b is also a multiple of 3 → contradiction with lowest terms.
3. Base: 2¹ = 2 > 1. Induction: 2^(k+1) = 2·2ᵏ > 2k ≥ k+1 (for k ≥ 1).
4. Form the sequence D by flipping the i-th digit of row i; then D differs from every row i in its i-th digit. Hence it matches no row, and the table fails to cover all the reals (infinite sequences).
5. gcd(252,105) = gcd(105,42) = gcd(42,21) = gcd(21,0) = **21**.
6. A collision occurs with 50% probability after about √(2⁶⁴) = 2³² ≈ 4.3 billion tries. With a modern computer that count is reachable in seconds to minutes, so "basically never happens" is wrong.
7. Example: the expected-comparisons analysis of quicksort. The events of individual comparisons happen in intricately dependent ways, but by linearity you can just add up "the probability each pair is compared" independently to derive O(n log n).
</details>

---

🏆 **Victory Reward**: Badge "🌌 Swordsman of Proofs" + 150 XP

➡️ Next: [World 10: The OS Grand Temple](world-10-operating-systems.md)
