# 🏔️ World 1: The Big-O Mountains — Big-O and Asymptotic Analysis

> The sign standing at the entrance to the mountains reads:
> "Those who cannot cross this mountain are not worthy to travel the worlds beyond.
> For **every algorithm is spoken in the language of this mountain**."

**What you'll learn in this chapter (the university lecture equivalent of "Introduction to Algorithms, Lecture 1")**
- The idea of evaluating an algorithm's efficiency by "how its running time grows"
- Big-O, Big-Θ, Big-Ω notation
- The representative complexity classes and the intuition behind them
- Worst-case, average-case, and amortized complexity

---

## 📖 Lecture 1: Why Don't We Measure in "Seconds"? (10 XP)

Suppose a program takes 3 seconds on your PC. Is this a good measure of performance?
No. **The number of seconds changes when the machine changes.** In CS, we evaluate algorithms by
**how the number of operations grows** (the growth rate) as the input size *n* gets large. This is called **asymptotic analysis**.

### The Definition of Big-O (this part alone is university math)

A function f(n) is **O(g(n))** when:

> there exist constants c > 0 and n₀ such that for all n ≥ n₀, f(n) ≤ c·g(n) holds

Intuitively, "**when n is sufficiently large, f does not exceed a constant multiple of g**."
In other words, Big-O represents an **upper bound on growth**.

- **O(g)** … upper bound (it gets no worse than this)
- **Ω(g)** … lower bound (it gets no better than this)
- **Θ(g)** … both upper and lower bound (exactly this growth rate)

### Rules of Calculation

1. **Ignore constant factors**: 3n² + 5 → O(n²)
2. **Ignore lower-order terms**: n² + n + 1 → O(n²)
3. **Sequential execution adds**: O(n) followed by O(m) → O(n + m)
4. **Nested loops multiply**: an n-iteration loop inside an n-iteration loop → O(n²)

### The Representative Complexity Classes (the Mountain's Elevation Chart)

| Elevation | Notation | Name | Representative Example | Approx. operations at n = 1,000,000 |
|---|---|---|---|---|
| 🟢 Plains | O(1) | constant time | array index access, hash table lookup (average) | 1 |
| 🟢 Hills | O(log n) | logarithmic time | binary search | about 20 |
| 🟡 Mountain Path | O(n) | linear time | full scan of an array | 1,000,000 |
| 🟡 Ridge | O(n log n) | linearithmic | merge sort, heap sort | about 20,000,000 |
| 🟠 Cliff | O(n²) | quadratic time | bubble sort, double loop | 10¹² (already rough) |
| 🔴 Above the Clouds | O(2ⁿ) | exponential time | enumerating all subsets | won't finish within the lifetime of the universe |
| 💀 Another Dimension | O(n!) | factorial time | enumerating all permutations | pointless to even think about |

**Memory aid**: log is "keep halving it," n log n is "divide-and-conquer sort," 2ⁿ is "every pattern of choose/don't-choose."

### Worst-Case · Average-Case · Amortized

- **Worst-case complexity**: performance on the most malicious input. When an interviewer asks "what's the complexity?", this is usually what they mean
- **Average-case complexity**: the expected value assuming random input (e.g., quicksort is O(n log n) on average)
- **Amortized complexity**: the value when occasionally expensive operations are smoothed out (e.g., appending to a dynamic array is O(n) when it resizes, but O(1) when smoothed)

### 📺 Recommended Drop Items (the original's curated videos)

- [Harvard CS50 - Asymptotic Notation (video)](https://www.youtube.com/watch?v=iOq5kSKqeR4)
- [UC Berkeley CS61B - Asymptotic Analysis (video)](https://archive.org/details/ucberkeley_webcast_VIS4YDpuP98)
- [Big-O Cheat Sheet](http://bigocheatsheet.com/) — the portable map for your adventure. Print it and pin it to your wall

---

## ⚔️ Quests

### Quest 1: The Order Appraiser (10 XP)

State the time complexity of the following code.

```python
# (a)
def q1a(arr):
    total = 0
    for x in arr:
        total += x
    return total

# (b)
def q1b(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            print(arr[i], arr[j])

# (c)
def q1c(n):
    count = 0
    while n > 1:
        n = n // 2
        count += 1
    return count

# (d)
def q1d(arr):           # arr has length n
    arr.sort()          # built-in sort
    for x in arr:
        print(x)
```

<details>
<summary>📜 Answers (open after solving them yourself)</summary>

- (a) **O(n)** — each element once
- (b) **O(n²)** — the number of pairs is n(n-1)/2 ≈ n²/2; ignore the constant factor
- (c) **O(log n)** — the number of times you keep halving n
- (d) **O(n log n)** — sort O(n log n) + scan O(n); the larger one dominates
</details>

### Quest 2: Spot the Lying Sign (20 XP)

Among the following signs standing along the mountain path, point out all the ones that are **wrong** and state why.

1. "O(2n) is slower than O(n)"
2. "An O(n²) algorithm is always slower than an O(n log n) algorithm"
3. "Binary search is O(log n) on a sorted array"
4. "f(n) = n² + 1000000n is O(n²)"

<details>
<summary>📜 Answers</summary>

1. **False** — constant factors are ignored, so O(2n) = O(n). The same.
2. **False** — asymptotically n² is slower, but not "always." When n is small, the n² one can be faster depending on constant factors (in fact, practical sorts switch to insertion sort for small ranges).
3. **Correct**
4. **Correct** — no matter how large the coefficient on the lower-order term n, it will eventually be overtaken by n².
</details>

### Quest 3: The Law of Amortization (20 XP)

You append n elements to an empty dynamic array (capacity 1). When the capacity fills up, you double the capacity and copy all elements.
Explain that the total number of copies is at most 2n, and show that the amortized complexity per append is O(1).

<details>
<summary>📜 Answer</summary>

Capacity expansions happen until the capacity reaches 1→2→4→…→n, and the number of copies at each expansion is 1, 2, 4, …, n/2.
The total is 1 + 2 + 4 + … + n/2 < n (the sum of a geometric series). Since the insertions themselves are n in number, the total operations are at most n + n = 2n.
Across n operations the total is O(n), so per operation it's O(n)/n = **O(1) (amortized)**.
</details>

---

## 👹 Boss Battle: The Summit Guardian "Order Dragon" (100 XP)

**Rules**: Close your notes. Time limit 30 minutes. 70% (3.5 questions) or more to win.

1. State the definition of Big-O precisely, using the constants c and n₀.
2. Arrange the following in order of slowest-growing (fastest to finish): `n!`, `n log n`, `2ⁿ`, `n`, `log n`, `n²`, `1`
3. Explain the difference between "this algorithm is O(n²)" and "this algorithm is Θ(n²)."
4. What is the complexity of a loop that counts up to n while tripling with `i = i * 3`?
5. In some sequence of operations, most operations are O(1), but once every k operations costs O(k). What is the amortized complexity?

<details>
<summary>📜 Solutions (open after the battle is over)</summary>

1. f(n) = O(g(n)) when ∃c>0, ∃n₀, ∀n≥n₀: f(n) ≤ c·g(n).
2. `1` < `log n` < `n` < `n log n` < `n²` < `2ⁿ` < `n!`
3. O is an upper bound only (it might actually be faster). Θ is both upper and lower bound (it grows exactly as n²).
4. **O(log₃ n) = O(log n)** — the base of the logarithm differs only by a constant factor, so it's ignored.
5. Across k operations the total is O(k) + O(k) = O(k) → **O(1) amortized** per operation.
</details>

---

🏆 **Victory Reward**: the badge "📏 Order Appraiser" + 100 XP

➡️ To the next world: [World 2: The Data Structure Town](world-02-data-structures.md)
