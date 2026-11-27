# 📕 Appendix I: The Complete Coding Problem Compendium — With Full Solutions

> This is the "Training Grounds of the Demon King's Castle." For you, who have learned how to fight in each World, here stand **practical problems with complete solutions**.
> We won't just throw problems at you and walk away. Every problem comes with **problem statement → approach → finished code → complexity derivation → common pitfalls**.
> Without searching any other site, you can reach a state where you can actually "solve" these right here.

## 📖 How to Use This Problem Set

1. **First, think for yourself for 20–30 minutes** (don't look at the answer right away — the experience of getting stuck is itself the learning)
2. Once you solve it, compare with the solution. Even if you can't solve it, read just the "approach" and try again
3. Code is shown in **Python** (it reads like pseudocode and is easy to follow). Porting it to your favorite language deepens your understanding
4. Use each problem's "Interview one-liner" to practice explaining complexity and strategy out loud

Problems are ordered from easiest to hardest. Difficulty is marked as 🟢 Easy / 🟡 Medium / 🔴 Hard.

---

## Chapter 1: Arrays and Strings (Corresponding World: World 2)

### Problem 1.1 — Two Sum 🟢

**Problem**: You are given an integer array `nums` and a target value `target`. Return the **indices** of the 2 elements whose sum equals `target`. You may assume each input has exactly one answer.

```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]   (nums[0] + nums[1] = 2 + 7 = 9)
```

**Approach**: Naively, try all pairs in O(n²). But if you query "has `target − x` appeared before?" in O(1) using a hash table, you only need a single pass over the array. **"I want to look up a value I've seen before" → hash table** (the watchword of World 2).

```python
def two_sum(nums, target):
    seen = {}                       # value -> its index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:            # has the partner already appeared?
            return [seen[need], i]
        seen[x] = i                 # record yourself (the trick: do it AFTER the lookup)
    return []                       # by assumption, we never reach here
```

**Complexity**: Time O(n) (each element processed once, dict operations are O(1) on average) / Space O(n) (at worst n entries recorded).

**Common pitfalls**:
- If you put `seen[x] = i` **before** the lookup, then when `target` is twice `x` you'd pair the element with itself. Always record after the lookup.
- Even if the same value appears multiple times, since you query before overwriting the index, it works correctly.

**Interview one-liner**: "By looking up the complement in a hash, you can drop the O(n²) double loop down to O(n), at the cost of O(n) space."

---

### Problem 1.2 — Contains Duplicate 🟢

**Problem**: Return `True` if any value appears in the array two or more times, and `False` if all are distinct.

**Approach**: Insert into a set, and return `True` immediately if it's already present. This too is "duplicate check → hash."

```python
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

**Complexity**: Time O(n) / Space O(n).

**Alternative and comparison**: Sorting first and then comparing adjacent elements uses O(1) space (with an in-place sort) but O(n log n) time. Being able to articulate the trade-off — "use space to be fast" versus "be slow but save memory" — makes you stand out.

---

### Problem 1.3 — Maximum Subarray Sum (Kadane's Algorithm) 🟡

**Problem**: Within an integer array (including negative numbers), return the maximum sum of a contiguous subarray.

```
Input:  [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6   (sum of subarray [4, -1, 2, 1])
```

**Approach**: Track "the maximum sum of a subarray ending here" as `cur`, updating from left to right. At each position there are 2 choices — **add the current element to the running sum**, or **start fresh from the current element**. This is a tiny bit of DP (World 6).

```python
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)       # continue, or restart from here?
        best = max(best, cur)       # update the overall maximum
    return best
```

**Complexity**: Time O(n) / Space O(1).

**Why is it correct?**: `cur` maintains the invariant "the maximum sum ending at position i." If `cur + x` is smaller than `x`, it's better to discard the past than to drag it along — so we restart. The DP state definition "dp[i] = maximum sum ending at i" and the transition "dp[i] = max(x, dp[i−1] + x)" map directly onto the update of `cur`.

**Common pitfalls**: When all elements are negative, you must not answer with an empty subarray (sum 0) — unless the problem says "the empty subarray is allowed." If you initialize to `nums[0]`, the largest negative number is returned correctly.

---

### Problem 1.4 — Anagram Check for Strings 🟢

**Problem**: Determine whether two strings are anagrams of each other (rearrangements of the same characters).

**Approach**: If the **frequency count** of each character matches exactly, they are anagrams. Count them with a hash (counter).

```python
from collections import Counter

def is_anagram(s, t):
    if len(s) != len(t):            # different lengths → immediately false (a shortcut)
        return False
    return Counter(s) == Counter(t)
```

**Complexity**: Time O(n) / Space O(k) (k is the number of distinct characters; for lowercase English letters, O(1)).

**Interview one-liner**: "I check whether the character frequency tables match. Counting in O(n) is faster than sorting and comparing in O(n log n)."

---

## Chapter 2: Two Pointers and Sliding Window (Corresponding: World 1 & 2)

### Problem 2.1 — Two Sum in a Sorted Array 🟢

**Problem**: In an **ascending sorted** array, return the indices (1-indexed) of the 2 numbers whose sum equals `target`.

**Approach**: If it's sorted, you can **squeeze in from both ends**. If the sum is too large, shrink from the right; if too small, extend from the left. No hash needed, so **O(1) space**.

```python
def two_sum_sorted(numbers, target):
    lo, hi = 0, len(numbers) - 1
    while lo < hi:
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]
        elif s < target:
            lo += 1                 # want it bigger → move left pointer right
        else:
            hi -= 1                 # want it smaller → move right pointer left
    return []
```

**Complexity**: Time O(n) / Space O(1).

**Why is it OK to shrink?**: When `s < target`, the best left endpoint that can pair with the current `hi` is `lo` (anything further left is too small to reach). So even discarding `lo` won't miss the optimal solution — the same exchange argument as in World 14.

---

### Problem 2.2 — Longest Substring Without Repeating Characters 🟡

**Problem**: Within a string, return the **length** of the longest contiguous substring with no repeated characters.

```
Input: "abcabcbb"  →  Output: 3   ("abc")
Input: "pwwkew"    →  Output: 3   ("wke")
```

**Approach**: **Sliding window**. Extend the right edge, and when a duplicate appears, shrink the left edge. By holding each character's "last seen position" in a hash, you can jump the left edge forward in one leap.

```python
def longest_unique_substring(s):
    last = {}                       # character -> index where it last appeared
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:
            left = last[c] + 1      # jump the left edge past the duplicate character
        last[c] = right
        best = max(best, right - left + 1)
    return best
```

**Complexity**: Time O(n) (the right edge moves once each, and the left edge only advances monotonically) / Space O(k).

**Common pitfalls**: The condition `last[c] >= left` is the key. You must ignore old duplicates that are **outside** the window, otherwise the left edge moves backward and you get a bug.

**Interview one-liner**: "Both pointers advance monotonically to the right, so what looks like a double loop is actually O(n)."

---

## Chapter 3: Linked Lists (Corresponding: World 2)

### Problem 3.1 — Reverse a Linked List 🟢

**Problem**: Reverse a singly linked list and return the new head.

**Approach**: With 3 pointers (`prev`, `cur`, `next`), flip each node's arrow backward one at a time. **Order is everything** — if you don't save the next node first, you lose the rest of the chain (the blacksmith's teaching from World 2).

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next              # ① save the next (forget this and you get lost)
        cur.next = prev             # ② flip the arrow backward
        prev = cur                  # ③ advance prev
        cur = nxt                   # ④ advance cur
    return prev                     # the new head is the original tail
```

**Complexity**: Time O(n) / Space O(1).

**Trace with a diagram**:
```
Initial:    None   1 → 2 → 3 → None
            prev  cur
After 1:    None ← 1   2 → 3
                 prev  cur
Final:      None ← 1 ← 2 ← 3
                           prev (= new head)
```

---

### Problem 3.2 — Cycle Detection 🟡

**Problem**: Determine whether a linked list has a cycle, using **O(1) extra memory**.

**Approach**: **Floyd's "tortoise and hare."** `slow` advances 1 step, `fast` advances 2 steps. If there's a cycle, they're guaranteed to meet (the technique foreshadowed in the World 2 boss battle).

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next            # 1 step
        fast = fast.next.next       # 2 steps
        if slow is fast:            # caught up = cycle exists
            return True
    return False                    # fast reached the tail = no cycle
```

**Complexity**: Time O(n) / Space O(1).

**Why are they guaranteed to meet?**: Inside the cycle, `fast` gets 1 closer to `slow` every step (relative speed 1). Since the distance is finite, it must reach 0. There's an alternative using a hash to record visited nodes with O(n) space, but this O(1)-space version is the elegant one.

---

## Chapter 4: Stacks and Queues (Corresponding: World 2)

### Problem 4.1 — Valid Parentheses 🟢

**Problem**: Determine whether the bracket matching in a string made of `()[]{}` is correct.

**Approach**: Push opening brackets onto a stack, and for closing brackets, pop the matching opener and verify the type matches. If the stack is empty at the end, it's OK (the complete version of World 2's Quest 5).

```python
def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s:
        if c in pairs.values():     # opening bracket
            stack.append(c)
        elif c in pairs:            # closing bracket
            if not stack or stack.pop() != pairs[c]:
                return False        # empty pop, or type mismatch
    return not stack                # if nothing is left over, it's valid
```

**Complexity**: Time O(n) / Space O(n).

**Common pitfalls**: "A closing bracket arrives but the stack is empty" mid-way is also invalid (e.g. `")("`). If you only check the final `not stack`, you'll miss it, so check both.

---

### Problem 4.2 — Stack That Returns the Minimum in O(1) 🟡

**Problem**: Design a stack that, in addition to `push` / `pop` / `top`, has a `get_min` that **returns the current minimum in O(1)**.

**Approach**: Run "the minimum at each point in time" alongside on **a second stack**. If you push the "current minimum" together on each push, then even after a pop the past minimum is restored.

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []              # the minimum at each point in time, running alongside

    def push(self, x):
        self.stack.append(x)
        m = x if not self.mins else min(x, self.mins[-1])
        self.mins.append(m)

    def pop(self):
        self.mins.pop()
        return self.stack.pop()

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return self.mins[-1]        # O(1)!
```

**Complexity**: All operations O(1) / Space O(n).

**Interview one-liner**: "By having the stack hold the history of minimums, rolling back the minimum on a pop also becomes O(1)."

---

## Chapter 5: Trees (Corresponding: World 3)

### Problem 5.1 — Maximum Depth of a Binary Tree 🟢

**Problem**: Return the depth from the root of a binary tree to its deepest leaf.

**Approach**: Tree problems are usually **recursion**. "My depth = 1 + the deeper of my left and right." The base case is the empty node (depth 0). A combination of World 6's recursion and World 3's trees.

```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

**Complexity**: Time O(n) (visiting all nodes) / Space O(h) (recursion stack, where h is the tree height; worst case O(n), balanced case O(log n)).

---

### Problem 5.2 — Validate a BST 🟡

**Problem**: Determine whether a given binary tree is a valid BST.

**Approach**: The trap foreshadowed in World 3 — "just yourself and your direct children" is not enough. Carry down **the range of values (lo, hi) each subtree may take** from above.

```python
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root:
        return True
    if not (lo < root.val < hi):    # out of range = violation
        return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))
```

**Complexity**: Time O(n) / Space O(h).

**Common pitfalls**: The left child must be not only "smaller than its parent" but also "greater than the lower bound set by an ancestor." Narrowing the range as you descend is the crux. As an alternative, you can also check whether "the in-order traversal forms a sorted sequence."

---

### Problem 5.3 — Lowest Common Ancestor (LCA) 🟡

**Problem**: On a BST, return the lowest common ancestor of 2 nodes `p` and `q`.

**Approach**: Use the BST's ordering property. If both are smaller than the current node, go left; if both are larger, go right; **the point where they split is the LCA**.

```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root             # the branching point = LCA
```

**Complexity**: Time O(h) / Space O(1).

---

## Chapter 6: Graphs (Corresponding: World 5)

### Problem 6.1 — Number of Islands 🟡

**Problem**: In a grid of `'1'` (land) and `'0'` (water), count the number of clusters of land (islands) connected up, down, left, and right.

**Approach**: A grid is an **implicit graph** (each cell is a vertex, adjacent cells are edges). Every time you find unvisited land, sink the whole island (mark it visited) with DFS/BFS, and count how many times you do this. This is exactly the connected-component counting of World 5.

```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(r, c):                 # sink the island with DFS
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'            # mark as visited (prevent revisiting)
        sink(r+1, c); sink(r-1, c); sink(r, c+1); sink(r, c-1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                sink(r, c)          # erase this island entirely
    return count
```

**Complexity**: Time O(rows × cols) (each cell visited once) / Space O(rows × cols) (worst-case recursion depth).

**Common pitfalls**: If you don't record visited cells, you get an infinite loop. If you don't want to modify the original grid, use a separate `visited` set.

---

### Problem 6.2 — Course Schedule Feasibility (Cycle Detection) 🟡

**Problem**: You are given `n` courses and prerequisites `[a, b]` (a is required before taking b). Determine whether you can take all courses (= whether the dependency graph has no cycle).

**Approach**: **Determining the existence of a topological sort**. With World 5's Kahn's algorithm (remove from in-degree 0), if you can remove all nodes, there's no cycle.

```python
from collections import deque

def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:      # dependency b → a
        graph[b].append(a)
        indegree[a] += 1

    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    done = 0
    while queue:
        node = queue.popleft()
        done += 1
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return done == num_courses      # removed everything = no cycle
```

**Complexity**: Time O(V + E) / Space O(V + E).

**Interview one-liner**: "Dependencies should form a DAG, and whether it can be topologically sorted is equivalent to whether it has no cycle. If you keep removing from in-degree 0 and everything disappears, all courses are takeable."

---

## Chapter 7: Dynamic Programming (Corresponding: World 6)

### Problem 7.1 — Coin Change (Minimum Number of Coins) 🟡

**Problem**: You are given coin denominations `coins` and an amount `amount`. Return the minimum number of coins to make `amount` (or −1 if it can't be made).

**Approach**: The standard DP move. State "dp[x] = minimum number of coins to make amount x," transition "dp[x] = min over each coin c of dp[x−c] + 1."

```python
def coin_change(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount       # dp[0] = 0 (0 yen takes 0 coins)
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x and dp[x - c] + 1 < dp[x]:
                dp[x] = dp[x - c] + 1
    return dp[amount] if dp[amount] != INF else -1
```

**Complexity**: Time O(amount × len(coins)) / Space O(amount).

**Why doesn't greedy work?**: "Greedily take the largest coin first" breaks down for coins=[1,3,4], amount=6 (greedy gives 4+1+1 = 3 coins, the optimum is 3+3 = 2 coins). Since the effect of a choice ripples into the future, you need DP that compares all options — exactly the answer to the World 6 boss battle.

---

### Problem 7.2 — Longest Increasing Subsequence (LIS) 🔴

**Problem**: Within an array, return the maximum length of a strictly increasing subsequence (it need not be contiguous).

```
Input: [10, 9, 2, 5, 3, 7, 101, 18]  →  Output: 4   ([2, 3, 7, 18], etc.)
```

**Approach (O(n²) DP)**: "dp[i] = length of the LIS ending at i," transition "for j before i with a smaller value, dp[i] = max(dp[j]) + 1."

```python
def length_of_lis(nums):
    if not nums:
        return 0
    dp = [1] * len(nums)            # each element alone has length 1
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**Complexity**: Time O(n²) / Space O(n).

**Even faster (O(n log n))**: Keep "the minimum tail value of an increasing sequence of length k" in an array `tails`, and replace each element via binary search (World 4's binary search + greedy). If the interviewer asks "can you do it faster?", being able to state this is advanced-level.

```python
import bisect

def length_of_lis_fast(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)         # extend to a new longest
        else:
            tails[i] = x            # update the tail to be smaller (widen future room)
    return len(tails)
```

The length of `tails` is the answer. Note that `tails` itself is not the LIS (only its length is correct).

---

### Problem 7.3 — Edit Distance (Levenshtein) 🔴

**Problem**: Return the minimum number of operations to change string `word1` into `word2`. The operations are insertion, deletion, and substitution of a single character, each with cost 1.

**Approach**: The 2D DP formulated in the World 6 boss battle. State "dp[i][j] = minimum cost to change the first i characters of word1 into the first j characters of word2."

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                # to empty out word1, delete i times
    for j in range(n + 1):
        dp[0][j] = j                # to build word2 from empty, insert j times
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]         # match → no operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],     # deletion
                    dp[i][j-1],     # insertion
                    dp[i-1][j-1],   # substitution
                )
    return dp[m][n]
```

**Complexity**: Time O(m × n) / Space O(m × n) (since each row uses only the previous row, you can drop it to O(n)).

**Applications**: Spell checkers, DNA sequence comparison, and the foundation of diff tools. You can speak of it as a representative example of "DP used in practice."

---

## Chapter 8: Heaps and Binary Search (Corresponding: World 3 & 1)

### Problem 8.1 — Kth Largest Element in an Array 🟡

**Problem**: Without sorting, find the kth largest value in the array.

**Approach**: Maintain a **min-heap of size k**. When it exceeds k, discard the minimum. The root of the heap is the answer (an application of the World 3 boss battle).

```python
import heapq

def find_kth_largest(nums, k):
    heap = []                       # min-heap of size k
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)     # discard the minimum → the top k remain
    return heap[0]                  # root = the kth largest value
```

**Complexity**: Time O(n log k) / Space O(k).

**Alternative**: Quickselect (World 14) is O(n) on average. If asked "what's the fastest?", being able to state this is good.

---

### Problem 8.2 — Search in a Rotated Sorted Array 🔴

**Problem**: From an array that was ascending sorted and then rotated at some point (e.g. `[4,5,6,7,0,1,2]`), find the index of value `target` in O(log n).

**Approach**: A variant of binary search. If you look at the middle, **at least one of the left half or the right half is always sorted**. Decide by range whether the target is in the sorted side, and halve the search range.

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:           # the left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                # target is in the left half
            else:
                lo = mid + 1
        else:                               # the right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1                # target is in the right half
            else:
                hi = mid - 1
    return -1
```

**Complexity**: Time O(log n) / Space O(1).

**Common pitfalls**: Whether it's `<=` or `<` at the boundary is everything. The equality in `nums[lo] <= nums[mid]` is needed when there are few elements (mid == lo). Verify boundaries with test cases like `[3,1]` target=1.

---

## Chapter 9: Bit Manipulation (Corresponding: World 7)

### Problem 9.1 — Single Number 🟢

**Problem**: In an array where every element appears exactly twice except for one, find the number that appears only once, using **O(1) space**.

**Approach**: **The magic of XOR**. `a ^ a = 0`, `a ^ 0 = a`. XOR everything together, the pairs cancel out, and only the lonely number remains.

```python
def single_number(nums):
    result = 0
    for x in nums:
        result ^= x                 # the pairs cancel each other out
    return result
```

**Complexity**: Time O(n) / Space O(1).

**Interview one-liner**: "Since XOR cancels equal values, you can solve it in O(1) space with no hash and no sort."

---

## 🏆 The Creed for Clearing the Training Grounds

Once you can solve the problems up to here **without looking at anything**, you have acquired real combat ability for technical interviews. As a parting gift, here is a map of the patterns:

| The scent of the problem | The tool to suspect |
|---|---|
| "Duplicate," "count," "look up the complement" | Hash table (Chapters 1 & 2) |
| "Sorted," "find 2 numbers," "pair" | Two pointers (Chapter 2) |
| "Longest/maximum contiguous substring/subarray" | Sliding window / Kadane (Chapters 1 & 2) |
| "Last in, first out," "matching," "Undo" | Stack (Chapter 4) |
| "Tree," "hierarchy," "recursive structure" | DFS recursion (Chapter 5) |
| "Shortest (unweighted)," "level by level" | BFS (Chapter 6) |
| "Connectivity," "islands," "connected components," "dependencies" | DFS/BFS/topological sort (Chapter 6) |
| "Minimum/maximum combination," "number of ways," "optimal" | Dynamic programming (Chapter 7) |
| "Top k," "always the minimum/maximum" | Heap (Chapter 8) |
| "Sorted," "find in O(log n)" | Binary search (Chapter 8) |

➡️ Next, on to designing real systems: [Appendix II: The Complete System Design Problem Compendium](appendix-02-system-design.md)
