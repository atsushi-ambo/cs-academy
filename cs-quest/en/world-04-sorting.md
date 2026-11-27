# 🌋 World 4: The Sorting Volcano — Sorting Algorithms

> At the foot of the volcano live five blacksmiths.
> Each forges blades using a "sorting technique" in their own distinct style.
> Only the one who apprentices under them all and masters every technique
> can draw the legendary sword sleeping in the crater —
> **"The Sword of N-Log-N."**

**What you'll learn in this chapter (the university equivalent of "Algorithms, Lectures 3–5")**
- How 5 comparison sorts work, their complexity, and their characteristics
- The comparison axes of stability and in-place behavior
- The divide-and-conquer design paradigm
- The theoretical lower bound Ω(n log n) for comparison sorts

---

## 📖 Lecture 1: Wisdom Before Apprenticeship — The 3 Eyes for Measuring a Sort (10 XP)

| Perspective | Meaning |
|---|---|
| Time complexity | How many comparisons/swaps in the worst and average cases |
| Space complexity / in-place | Whether O(1) extra memory suffices (in-place) or O(n) is needed |
| **Stability (stable)** | Whether elements with equal keys **keep their original order** |

Example of stability: if you sort a roster by "name" and then do a stable sort by "grade year,"
**within the same grade, name order is preserved.** This is the foundation of multi-key sorting, and it comes up often in interviews.

## 📖 Lecture 2: The Five Blacksmiths (10 XP)

### 🔨 Selection Sort — the "Pick the Smallest and Move It Front" style

From the unsorted portion, **select** the minimum and swap it to the front. Repeat.
- Always **O(n²)**. However, the **number of swaps is at most n−1** (not bad when writes are expensive)
- in-place / unstable

### 🔨 Insertion Sort — the "Slot It Into Your Hand" style

Like tidying a hand of playing cards, **insert** each element into its correct position within the sorted portion.
- Worst case O(n²), but **O(n) on nearly-sorted input**
- in-place / stable
- **Among the fastest on small arrays** — still in active use today as the "finishing touch" in practical sorts

### 🔨 Merge Sort — the "Split in Half and Blend" style (divide and conquer)

```
mergesort(A):
    if |A| ≤ 1: return A
    L = mergesort(first half)
    R = mergesort(second half)
    return merge(L, R)   # blend two sorted sequences in O(n)
```

- **Always O(n log n)** (log n levels × O(n) merge per level)
- stable / but requires O(n) working space
- Strong for sorting linked lists and external sorting (huge files)

### 🔨 Quicksort — the "Sort by Smaller-or-Larger-Than-Pivot" style (divide and conquer)

Choose one pivot, **partition into a smaller group and a larger group**, and recursively sort each.
- Average **O(n log n)**, worst O(n²) (when the pivot is always an extreme value — e.g., picking the first element as pivot on sorted input)
- Countermeasure: choosing the pivot at random makes the worst case practically never happen
- in-place / unstable
- **Cache-efficient and among the fastest in practice** (you'll learn why in World 7)

### 🔨 Heapsort — the "Pull From the Heap in Order" style

heapify the array (O(n)), then place the max at the end and run extract_max n times.
- **Always O(n log n)** / in-place / unstable
- The choice when you want a worst-case O(n log n) guarantee with zero extra memory

### 📊 The Five Techniques at a Glance

| Technique | Worst | Average | Extra Memory | Stable | In a word |
|---|---|---|---|---|---|
| Selection | O(n²) | O(n²) | O(1) | ✗ | Few swaps |
| Insertion | O(n²) | O(n²) | O(1) | ✓ | O(n) if nearly sorted |
| Merge | O(n log n) | O(n log n) | O(n) | ✓ | The always-stable honor student |
| Quick | O(n²) | O(n log n) | O(log n)※ | ✗ | Fastest in practice ※recursion stack |
| Heap | O(n log n) | O(n log n) | O(1) | ✗ | Guarantee plus low memory |

## 📖 Lecture 3: The Volcano's Truth — The Limit of Comparison Sorts (10 XP)

**Theorem**: Any sort that rearranges using only comparisons needs at worst **Ω(n log n)** comparisons.

**Intuition behind the proof**: there are n! possible orderings of n elements. A single comparison can at best halve the possibilities.
To narrow n! possibilities down to one requires log₂(n!) ≈ n log n comparisons (the decision-tree height argument).

But this is the limit *for comparisons*. **Sorts that don't compare** break past the wall:
- **Counting sort**: O(n + k) if the value range k is small
- **Radix sort**: stable sort digit by digit, O(d·(n + k))

📺 Recommended video: the [Sorting section](https://github.com/jwasham/coding-interview-university#sorting) of the original list — especially
the [visualization of 15 sorts](https://www.youtube.com/watch?v=kPRA0W1kECg), a classic you can memorize through sound and motion.

---

## ⚔️ Quests

### Quest 1: Sizing Up the Blacksmiths (20 XP)

Choose the best sort and state your reasoning.

1. You want to sort 10 million log entries stably. Memory is plentiful.
2. A nearly-sorted array has just a few new data items mixed in.
3. An embedded device. You want a worst-case O(n log n) guarantee with almost zero extra memory.
4. You want to sort 1 million integers from 0 to 100.

<details>
<summary>📜 Answer</summary>

1. **Merge sort** (stable + always O(n log n))
2. **Insertion sort** (O(n) if nearly sorted)
3. **Heapsort** (in-place + worst-case O(n log n))
4. **Counting sort** (small value range → O(n + k))
</details>

### Quest 2: Training by Hand (20 XP)

For the array `[5, 2, 9, 1, 7]`:
1. Write the array after each pass of selection sort.
2. Draw the split-and-merge process of merge sort as a tree diagram.
3. Write the result of the first partition of quicksort using the first element as the pivot.

<details>
<summary>📜 Answer (example)</summary>

1. `[1,2,9,5,7]` → `[1,2,9,5,7]` → `[1,2,5,9,7]` → `[1,2,5,7,9]`
2. `[5,2,9,1,7]` → `[5,2]` `[9,1,7]` → … → merging gives `[2,5]` `[1,7,9]` → `[1,2,5,7,9]`
3. Pivot 5: smaller group `[2,1]` + 5 + larger group `[9,7]` (the ordering may differ depending on implementation)
</details>

### Quest 3: 💻 Implementation Quest "The Two Famous Blades" (50 XP × 2)

1. Implement **merge sort** (recursion + a merge function).
2. Implement **quicksort** (in-place partition; pick the pivot at random).

For both, test on random arrays, sorted arrays, reverse-sorted arrays, and arrays full of duplicates.

### Quest 4: The Blacksmith's Catechism (20 XP)

1. What input makes quicksort hit its worst case O(n²), and how do you avoid it?
2. What is the recursion depth of merge sort? How much work per level?
3. Give one concrete example where "a stable sort is required."

<details>
<summary>📜 Answer</summary>

1. An already-sorted array where you always pick an extreme as the pivot (the split skews to 1 : n−1). Avoid it with a random pivot or median-of-three.
2. Depth O(log n), and the merges at each level total O(n). Therefore O(n log n).
3. Example: sort a transaction history by amount, then stably sort by date so that "within the same day, amount order is preserved."
</details>

---

## 👹 Boss Battle: The Crater's Guardian Dragon "Sort Dragon" (100 XP)

Close your notes and face it. Win with 70% or more.

1. Write a table of the worst-case complexity, stability, and in-place behavior of the 5 comparison sorts (from memory).
2. Use a decision tree to explain why comparison sorts cannot beat Ω(n log n).
3. Write quicksort's partition (either Lomuto or Hoare) in pseudocode.
4. Why does merge sort pair well with linked lists?
5. Explain why production-language sorts (e.g., Python's Timsort) are "merge + insertion" hybrids.

<details>
<summary>📜 Solution</summary>

1. See the table in Lecture 2.
2. A comparison sort can be seen as a binary decision tree that branches on comparison results. Its leaves must correspond to all n! orderings, so its height (= worst-case comparison count) is log₂(n!) = Ω(n log n).
3. (Lomuto example) pivot = A[hi]; i = lo−1; for j in lo..hi−1: if A[j] ≤ pivot: i++; swap(A[i], A[j]); finally swap(A[i+1], A[hi]); return i+1.
4. Merge needs only sequential access, no random access. Re-linking pointers also keeps extra memory low.
5. The big picture uses O(n log n) merging to ensure stability, while small ranges are faster with insertion sort, which has a lighter constant factor. This also exploits the "already-ordered consecutive runs (runs)" common in real data.
</details>

---

🏆 **Victory Reward**: the badge "🌀 Stormbringer" + the Sword of N-Log-N + 100 XP

➡️ On to the next world: [World 5: The Graph Ocean](world-05-graphs.md)
