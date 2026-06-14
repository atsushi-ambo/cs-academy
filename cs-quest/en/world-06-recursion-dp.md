# 🏜️ World 6: The Recursion Desert & DP Ruins — Recursion and Dynamic Programming

> Beyond the great ocean lies desert as far as the eye can see.
> The dunes are self-similar without end — a large dune is made of small dunes,
> and each small dune is made of still smaller dunes.
> Deep in the desert sleep the ruins of an ancient civilization. Carved into the wall is this:
> "**Whoever solves the same question twice perishes in the desert. Carve down the answer (memoize it).**"

**What you'll learn in this chapter (the university equivalent of "Algorithms, Lectures 10–12")**
- Designing recursion (base case and recursive case)
- Its relationship to divide and conquer
- Memoization (top-down DP)
- The standard playbook of dynamic programming (bottom-up DP)

---

## 📖 Lecture 1: The Self-Similarity of Dunes — Recursion (10 XP)

**Recursion** means "solving a problem with smaller problems of the same shape." There are only 2 rules of design:

1. **Base case**: directly return the answer to a problem that can't be made any smaller
2. **Recursive case**: call a problem that is **definitely smaller** than itself, then assemble the result

```python
def factorial(n):
    if n <= 1: return 1          # base case
    return n * factorial(n - 1)  # recursive case (n definitely decreases)
```

**Watch the call stack**: every recursive call pushes a stack frame (arguments, return address).
Recursion of depth d eats O(d) memory. Too deep and you get a stack overflow — swallowed by the sand.

**Tail recursion**: if the recursive call is the function's last operation, it can be rewritten as a loop
(some languages optimize this automatically; many don't, so consider turning deep recursion into a loop).

📺 [How recursion works internally (video)](https://www.youtube.com/watch?v=wMNrSM5RFMc)

## 📖 Lecture 2: The Desert's Trap — The Explosion of Naive Recursion (10 XP)

Compute the Fibonacci number F(n) = F(n−1) + F(n−2) by naive recursion and you get:

```
                    F(5)
                  /      \
              F(4)        F(3)
             /    \      /    \
          F(3)   F(2)  F(2)  F(1)
          /  \
       F(2) F(1)   ← F(3) and F(2) are solved over and over!
```

The number of calls is **O(2ⁿ)** — exponential explosion. The cause is **overlapping subproblems**.
The same question is solved again and again. This is the fate of those who "perish in the desert."

## 📖 Lecture 3: Wisdom of the Ruins, Part One — Memoization (Top-Down DP) (10 XP)

**Once you've carved an answer, never solve it again.**

```python
memo = {}
def fib(n):
    if n <= 1: return n
    if n in memo: return memo[n]   # use the carved answer if it exists
    memo[n] = fib(n-1) + fib(n-2)  # otherwise solve it and carve it
    return memo[n]
```

There are only n + 1 subproblems, so it plummets to **O(n)**. The advantage: you can speed it up while keeping the recursive shape.

## 📖 Lecture 4: Wisdom of the Ruins, Part Two — Bottom-Up DP (10 XP)

Stop recursing and **fill a table from the smallest problems upward**.

```python
def fib(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

### The 2 Conditions for DP

1. **Overlapping subproblems**: the same small problem appears repeatedly
2. **Optimal substructure**: the optimal solution of a large problem is assembled from optimal solutions of smaller problems

### The Standard DP Playbook (the steps carved into the ruins' stone tablet)

1. **Define the state**: state outright "dp[i] = the answer to ___" in plain words (most important!)
2. **Write the transition**: how to express dp[i] in terms of smaller states
3. Decide the **base case**
4. Decide the **fill order** (so that the states you depend on are filled first)
5. Confirm which cell holds the answer

### The Classic DP Quests (the road every adventurer travels once)

| Problem | State definition | Transition |
|---|---|---|
| Climbing stairs (1 or 2 steps) | dp[i] = number of ways to reach step i | dp[i] = dp[i−1] + dp[i−2] |
| Coin change (minimum count) | dp[x] = minimum coins to make amount x | dp[x] = min(dp[x−c] + 1) for each coin c |
| Longest common subsequence (LCS) | dp[i][j] = LCS length of the first i chars of s and the first j chars of t | if they match dp[i−1][j−1]+1, otherwise max(dp[i−1][j], dp[i][j−1]) |
| 0/1 knapsack | dp[i][w] = max value with up to item i and capacity w | max of include / exclude |

📺 Recommended video: the original [Dynamic Programming section](https://github.com/jwasham/coding-interview-university#dynamic-programming) —
MIT 6.006's 4 back-to-back DP lectures are the complete walkthrough guide to the ruins.

---

## ⚔️ Quests

### Quest 1: Basic Training on the Dunes (20 XP)

Write these with recursion (no DP yet). Make each function's base case explicit.

1. `sum_list(arr)` — the sum of an array
2. `power(x, n)` — xⁿ (n a non-negative integer). Also try the O(log n) version (exponentiation by squaring)
3. `reverse_string(s)` — reversing a string

<details>
<summary>📜 Hint (the O(log n) version of #2)</summary>

xⁿ = (x^(n/2))² (n even) / x · xⁿ⁻¹ (n odd). The key is to solve the half-problem **only once** and square it.
</details>

### Quest 2: Observing the Explosion (20 XP)

Implement both the naive recursive fib(n) and the memoized fib(n), and compare their running times at n = 35.
The goal is to feel it. Learn the terror of the desert in your body.

### Quest 3: 💻 Implementation Quest "The Three Chambers of the Ruins" (50 XP × 3)

**Write the DP playbook (state → transition → base → order) in comments first**, then implement.

1. **Climbing stairs**: the number of ways to climb an n-step staircase 1 or 2 steps at a time
2. **Coin change**: the minimum number of coins to make amount n with coin types `[1, 5, 10, 25]`
3. **Longest common subsequence (LCS)**: find the **length** of the LCS of two strings, and if possible go as far as **reconstructing the string**

### Quest 4: The Stone Tablet's Catechism (20 XP)

1. Compare the pros and cons of memoization and bottom-up DP.
2. What's the difference between "problems solvable by greedy" and "problems that need DP"?
3. How do you cut Fibonacci DP's memory from O(n) to O(1)?

<details>
<summary>📜 Answer</summary>

1. Memoization: you can write it in recursive form, which is intuitive, and it only solves the subproblems it needs. But it incurs stack consumption and function-call overhead. Bottom-up: easy to make fast and memory-light, but you must design the fill order yourself.
2. Greedy applies when you can prove the property (the greedy-choice property) that "a locally optimal choice always leads to the global optimum." When that doesn't hold and a choice's effect ripples downstream, use DP to compare all options.
3. dp[i] depends only on the previous two, so rotating two variables gives O(1).
</details>

---

## 👹 Boss Battle: The Ruins' Guardian Deity "The Sphinx" (100 XP)

Close your notes and face it. Win with 70% or more. The Sphinx loves riddles.

1. What are the 2 conditions that guarantee a recursive function terminates?
2. Explain, in terms of "the number of subproblems," why naive recursive Fibonacci is O(2ⁿ) and why memoization makes it O(n).
3. State the 2 properties under which DP applies.
4. We defined the state as "dp[i][j] = the edit distance between the first i chars of string s and the first j chars of t." Write the transition (insert, delete, and replace each cost 1).
5. In the 0/1 knapsack, if "you may put in any number of the same item," how does the transition change?
6. Formulate with DP the number of paths from the top-left to the bottom-right of a grid moving only right and down.

<details>
<summary>📜 Solution</summary>

1. A base case exists, and each recursion gets definitely closer to the base case.
2. The naive version solves the same subproblems redundantly an exponential number of times. There are in fact only n+1 subproblems, and memoization solves each only once, so it's O(n).
3. Overlapping subproblems, and optimal substructure.
4. If s[i] == t[j], dp[i][j] = dp[i−1][j−1]. Otherwise dp[i][j] = 1 + min(dp[i−1][j] (delete), dp[i][j−1] (insert), dp[i−1][j−1] (replace)).
5. In the "include" transition, reference **dp[i][w−wt]** instead of dp[i−1][w−wt] (reusing the same item's row).
6. dp[i][j] = number of paths to cell (i,j) = dp[i−1][j] + dp[i][j−1], with base cases of 1 for the top row and leftmost column.
</details>

---

🏆 **Victory Reward**: the badges "🪞 Returnee of the Infinite Corridor" and "🧩 Decipherer of the Ruins" + 100 XP

➡️ On to the next world: [World 7: The Clockwork Underground](world-07-inside-the-machine.md)
