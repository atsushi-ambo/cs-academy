# 📙 Appendix IV: Complete Solution Set for the Implementation Quests — All Code Tested

> This is "The Forge of the Smithing God." For each world's **💻 implementation quests** ("implement ○○ yourself"),
> we have **deliberately withheld the solutions** until now. Writing them yourself is the greatest training of all.
> But in response to the cry of "I can't tell whether my own code is correct," we have
> prepared **reference solutions** for all of them here. Every one has actually been run and tested.

## ⚠️ How to Use This (Just Follow These Rules)

1. **First, always write everything yourself.** If you peek here right away, it won't be any training at all.
2. Only **after your own code works**, compare it against this.
3. The solutions are **not the only correct answers.** If it works and the complexity is right, your own style is fine.
4. At the end of each solution we've attached a "**Self-test.**" Check whether your code passes it.
5. The language is Python. Porting it to your own favorite language will deepen your understanding of the structure even further.

> 💡 "Understanding when you read it" and "being able to write it" are different things. **Even if it's just copying, type it out by hand at least once.**

---

## World 2 · Solution 1: Dynamic Array

Key point: double the capacity when full, halve it when the size drops to 1/4 of the capacity (to keep amortized O(1)).

```python
class DynamicArray:
    def __init__(self):
        self._cap = 1
        self._n = 0
        self._a = [None] * self._cap

    def __len__(self):    return self._n
    def is_empty(self):   return self._n == 0
    def capacity(self):   return self._cap

    def at(self, i):
        if not 0 <= i < self._n:
            raise IndexError("out of range")     # fail clearly on out-of-range access
        return self._a[i]

    def _resize(self, c):
        b = [None] * c
        for i in range(self._n):
            b[i] = self._a[i]
        self._a = b
        self._cap = c

    def push(self, x):
        if self._n == self._cap:
            self._resize(2 * self._cap)          # if full, double it
        self._a[self._n] = x
        self._n += 1

    def insert(self, i, x):
        if self._n == self._cap:
            self._resize(2 * self._cap)
        for j in range(self._n, i, -1):          # shift the back over by one
            self._a[j] = self._a[j - 1]
        self._a[i] = x
        self._n += 1

    def prepend(self, x):
        self.insert(0, x)

    def pop(self):
        x = self._a[self._n - 1]
        self._n -= 1
        if 0 < self._n <= self._cap // 4:        # shrink if too sparse
            self._resize(self._cap // 2)
        return x

    def delete(self, i):
        for j in range(i, self._n - 1):
            self._a[j] = self._a[j + 1]
        self._n -= 1
        if 0 < self._n <= self._cap // 4:
            self._resize(self._cap // 2)

    def find(self, x):
        for i in range(self._n):
            if self._a[i] == x:
                return i
        return -1

    def remove(self, x):
        i = self.find(x)
        if i >= 0:
            self.delete(i)
```

**Complexity**: push amortized O(1), at O(1), insert/delete O(n), find O(n).

<details>
<summary>🧪 Self-test</summary>

```python
da = DynamicArray()
for k in range(10): da.push(k)
assert len(da) == 10 and da.at(0) == 0 and da.at(9) == 9
da.insert(0, -1); assert da.at(0) == -1 and len(da) == 11
da.prepend(-2);   assert da.at(0) == -2
assert da.find(5) == 7
da.remove(5);     assert da.find(5) == -1 and len(da) == 11
assert da.pop() == 9
print("DynamicArray OK")
```
</details>

---

## World 2 · Solution 2: Singly Linked List

Key point: `reverse` uses 3 pointers. **Save the next node first**, then re-wire the pointers (the lesson of the World 2 blacksmith).

```python
class Node:
    def __init__(self, v, nxt=None):
        self.val = v
        self.next = nxt

class LinkedList:
    def __init__(self):
        self.head = None
        self._n = 0

    def size(self):  return self._n

    def push_front(self, v):
        self.head = Node(v, self.head)
        self._n += 1

    def pop_front(self):
        v = self.head.val
        self.head = self.head.next
        self._n -= 1
        return v

    def push_back(self, v):
        n = Node(v)
        if not self.head:
            self.head = n
        else:
            c = self.head
            while c.next:
                c = c.next
            c.next = n
        self._n += 1

    def front(self): return self.head.val

    def back(self):
        c = self.head
        while c.next:
            c = c.next
        return c.val

    def insert(self, i, v):
        if i == 0:
            self.push_front(v); return
        c = self.head
        for _ in range(i - 1):
            c = c.next
        c.next = Node(v, c.next)
        self._n += 1

    def erase(self, i):
        if i == 0:
            self.pop_front(); return
        c = self.head
        for _ in range(i - 1):
            c = c.next
        c.next = c.next.next
        self._n -= 1

    def reverse(self):
        prev, cur = None, self.head
        while cur:
            nxt = cur.next      # ① save the next node
            cur.next = prev     # ② flip the arrow
            prev = cur          # ③ advance
            cur = nxt           # ④ advance
        self.head = prev
```

**Complexity**: push_front/pop_front O(1), push_back/insert/erase/reverse O(n).

<details>
<summary>🧪 Self-test</summary>

```python
ll = LinkedList()
for k in [1, 2, 3]: ll.push_back(k)
ll.push_front(0)
def to_list(l):
    out, c = [], l.head
    while c: out.append(c.val); c = c.next
    return out
assert to_list(ll) == [0, 1, 2, 3] and ll.front() == 0 and ll.back() == 3
ll.insert(2, 99); assert to_list(ll) == [0, 1, 99, 2, 3]
ll.erase(2);      assert to_list(ll) == [0, 1, 2, 3]
ll.reverse();     assert to_list(ll) == [3, 2, 1, 0]
print("LinkedList OK")
```
</details>

---

## World 2 · Solution 3: Hash Table (Open Addressing)

Key point: deletion places a **tombstone (a dead flag)**. Without it, a subsequent probe sequence gets cut off (the World 2 warning). Resize at a load factor of 0.7.

```python
class HashTable:
    def __init__(self, cap=8):
        self._cap = cap
        self._n = 0
        self._keys = [None] * cap
        self._vals = [None] * cap
        self._dead = [False] * cap          # tombstones

    def _hash(self, k):
        return hash(k) % self._cap

    def _resize(self, c):
        old = [(self._keys[i], self._vals[i]) for i in range(self._cap)
               if self._keys[i] is not None and not self._dead[i]]
        self._cap = c
        self._keys = [None] * c
        self._vals = [None] * c
        self._dead = [False] * c
        self._n = 0
        for k, v in old:
            self.add(k, v)

    def add(self, k, v):
        if (self._n + 1) / self._cap > 0.7:
            self._resize(2 * self._cap)
        i = self._hash(k)
        first_dead = -1
        while self._keys[i] is not None:
            if not self._dead[i] and self._keys[i] == k:
                self._vals[i] = v; return       # overwrite an existing key
            if self._dead[i] and first_dead < 0:
                first_dead = i                   # mark a tombstone as a reuse candidate
            i = (i + 1) % self._cap
        slot = first_dead if first_dead >= 0 else i
        self._keys[slot] = k
        self._vals[slot] = v
        self._dead[slot] = False
        self._n += 1

    def _find(self, k):
        i = self._hash(k); steps = 0
        while self._keys[i] is not None and steps < self._cap:
            if not self._dead[i] and self._keys[i] == k:
                return i
            i = (i + 1) % self._cap; steps += 1
        return -1

    def exists(self, k): return self._find(k) >= 0

    def get(self, k):
        i = self._find(k)
        return self._vals[i] if i >= 0 else None

    def remove(self, k):
        i = self._find(k)
        if i >= 0:
            self._dead[i] = True               # plant a tombstone (don't erase)
            self._n -= 1
```

**Complexity**: add/exists/get/remove are O(1) on average, O(n) in the worst case.

<details>
<summary>🧪 Self-test</summary>

```python
ht = HashTable()
for k in range(20): ht.add(f"k{k}", k * 10)
assert ht.exists("k5") and ht.get("k5") == 50 and ht.get("k19") == 190
ht.add("k5", 999); assert ht.get("k5") == 999          # overwrite
ht.remove("k5");   assert not ht.exists("k5") and ht.get("k7") == 70   # probing continues past the tombstone
print("HashTable OK")
```
</details>

---

## World 3 · Solution 1: Binary Search Tree (BST)

Key point: validation **carries a range (lo, hi) along.** For deletion, the two-child case is replaced with the **minimum value of the right subtree.**

```python
class BSTNode:
    def __init__(self, v):
        self.val = v
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
        self._n = 0

    def insert(self, v):
        self.root = self._ins(self.root, v)
        self._n += 1

    def _ins(self, node, v):
        if not node:
            return BSTNode(v)
        if v < node.val:
            node.left = self._ins(node.left, v)
        else:
            node.right = self._ins(node.right, v)
        return node

    def count(self): return self._n

    def inorder(self):
        out = []
        def go(n):
            if n:
                go(n.left); out.append(n.val); go(n.right)
        go(self.root)
        return out                              # for a BST this comes out in ascending order

    def contains(self, v):
        n = self.root
        while n:
            if v == n.val: return True
            n = n.left if v < n.val else n.right
        return False

    def height(self, n="__root__"):
        if n == "__root__": n = self.root
        if not n: return -1                     # empty is -1, a leaf is 0
        return 1 + max(self.height(n.left), self.height(n.right))

    def get_min(self):
        n = self.root
        while n.left: n = n.left
        return n.val

    def get_max(self):
        n = self.root
        while n.right: n = n.right
        return n.val

    def is_bst(self, n="__r__", lo=float('-inf'), hi=float('inf')):
        if n == "__r__": n = self.root
        if not n: return True
        if not lo < n.val < hi: return False    # out of range means a violation
        return self.is_bst(n.left, lo, n.val) and self.is_bst(n.right, n.val, hi)

    def delete(self, v):
        self.root = self._del(self.root, v)

    def _del(self, node, v):
        if not node: return None
        if v < node.val:
            node.left = self._del(node.left, v)
        elif v > node.val:
            node.right = self._del(node.right, v)
        else:                                   # found
            if not node.left:  return node.right    # 0 or 1 child
            if not node.right: return node.left
            succ = node.right                   # 2 children: replace with min of right subtree
            while succ.left: succ = succ.left
            node.val = succ.val
            node.right = self._del(node.right, succ.val)
        return node
```

**Complexity**: O(log n) if balanced, O(n) in the worst case (a straight line).

<details>
<summary>🧪 Self-test</summary>

```python
bst = BST()
for v in [50, 30, 70, 20, 40, 60, 80]: bst.insert(v)
assert bst.inorder() == [20, 30, 40, 50, 60, 70, 80]
assert bst.contains(60) and not bst.contains(99)
assert bst.get_min() == 20 and bst.get_max() == 80 and bst.is_bst()
bst.delete(40); assert bst.inorder() == [20, 30, 50, 60, 70, 80]
bst.delete(50); assert bst.inorder() == [20, 30, 60, 70, 80] and bst.is_bst()
print("BST OK")
```
</details>

---

## World 3 · Solution 2: Max-Heap (Array-Based)

Key point: parent `(i-1)//2`, children `2i+1, 2i+2`. `heapify` sifts down from the last parent backward in O(n).

```python
class MaxHeap:
    def __init__(self):
        self.a = []

    def _up(self, i):
        while i > 0 and self.a[(i - 1) // 2] < self.a[i]:
            self.a[(i - 1) // 2], self.a[i] = self.a[i], self.a[(i - 1) // 2]
            i = (i - 1) // 2

    def _down(self, i):
        n = len(self.a)
        while True:
            l, r, big = 2 * i + 1, 2 * i + 2, i
            if l < n and self.a[l] > self.a[big]: big = l
            if r < n and self.a[r] > self.a[big]: big = r
            if big == i: break
            self.a[i], self.a[big] = self.a[big], self.a[i]
            i = big

    def insert(self, x):
        self.a.append(x)
        self._up(len(self.a) - 1)

    def get_max(self): return self.a[0]

    def extract_max(self):
        top = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self._down(0)
        return top

    @staticmethod
    def heapify(arr):
        h = MaxHeap(); h.a = arr[:]
        for i in range(len(h.a) // 2 - 1, -1, -1):   # sift down from the last parent backward = O(n)
            h._down(i)
        return h

    @staticmethod
    def heap_sort(arr):                          # returns ascending order
        h = MaxHeap.heapify(arr); out = []
        while h.a:
            out.append(h.extract_max())
        return out[::-1]
```

**Complexity**: insert/extract_max O(log n), heapify O(n), heap_sort O(n log n).

<details>
<summary>🧪 Self-test</summary>

```python
h = MaxHeap()
for x in [3, 1, 4, 1, 5, 9, 2, 6]: h.insert(x)
assert h.get_max() == 9 and h.extract_max() == 9 and h.get_max() == 6
assert MaxHeap.heap_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]
print("MaxHeap OK")
```
</details>

---

## World 4 · Solution: Merge Sort and Quicksort

```python
def mergesort(a):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    L, R = mergesort(a[:m]), mergesort(a[m:])
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):            # merge two sorted sequences
        if L[i] <= R[j]:                        # use <= to preserve stability
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    out.extend(L[i:]); out.extend(R[j:])
    return out

import random
def quicksort(a):
    a = a[:]                                    # non-destructive
    def qs(lo, hi):
        if lo >= hi: return
        p = random.randint(lo, hi)              # random pivot to avoid the worst case
        a[p], a[hi] = a[hi], a[p]
        pivot, i = a[hi], lo
        for j in range(lo, hi):                 # Lomuto partition
            if a[j] <= pivot:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        qs(lo, i - 1); qs(i + 1, hi)
    qs(0, len(a) - 1)
    return a
```

**Complexity**: merge is always O(n log n), stable, O(n) space. Quick is O(n log n) on average, O(n²) worst case, in-place.

<details>
<summary>🧪 Self-test</summary>

```python
t = [5, 2, 9, 1, 7, 2, 8, 3]
assert mergesort(t) == sorted(t) and quicksort(t) == sorted(t)
assert mergesort([]) == [] and quicksort([1]) == [1]      # empty / single-element boundaries
print("Sorts OK")
```
</details>

---

## World 5 · Solution: Graph (BFS / DFS / Shortest Path / Connected Components / Topological Sort)

```python
from collections import deque

class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v, directed=False):
        self.adj.setdefault(u, []).append(v)
        self.adj.setdefault(v, [])
        if not directed:
            self.adj[v].append(u)

    def bfs(self, s):
        seen, q, order = {s}, deque([s]), []
        while q:
            u = q.popleft(); order.append(u)
            for w in self.adj[u]:
                if w not in seen:
                    seen.add(w); q.append(w)
        return order

    def shortest_path(self, s, t):              # unweighted shortest path (fewest edges)
        if s == t: return [s]
        prev, q = {s: None}, deque([s])
        while q:
            u = q.popleft()
            for w in self.adj[u]:
                if w not in prev:
                    prev[w] = u
                    if w == t:                  # follow parents to reconstruct the path
                        path = [t]
                        while prev[path[-1]] is not None:
                            path.append(prev[path[-1]])
                        return path[::-1]
                    q.append(w)
        return None

    def dfs(self, s):
        seen, order = set(), []
        def go(u):
            seen.add(u); order.append(u)
            for w in self.adj[u]:
                if w not in seen: go(w)
        go(s)
        return order

    def components(self):                       # number of connected components
        seen, c = set(), 0
        for u in self.adj:
            if u not in seen:
                c += 1; stack = [u]
                while stack:
                    x = stack.pop()
                    if x in seen: continue
                    seen.add(x)
                    stack.extend(self.adj[x])
        return c

def topo_sort(n, edges):                        # Kahn's algorithm. None if there's a cycle
    adj = [[] for _ in range(n)]; indeg = [0] * n
    for a, b in edges:
        adj[a].append(b); indeg[b] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for w in adj[u]:
            indeg[w] -= 1
            if indeg[w] == 0: q.append(w)
    return order if len(order) == n else None   # if not everything is removed, there's a cycle
```

**Complexity**: BFS/DFS/topological sort are all O(V + E).

<details>
<summary>🧪 Self-test</summary>

```python
g = Graph()
for u, v in [('A','B'),('A','C'),('B','D'),('C','D')]: g.add_edge(u, v)
assert g.bfs('A')[0] == 'A' and set(g.bfs('A')) == {'A','B','C','D'}
assert len(g.shortest_path('A','D')) == 3        # A-B-D or A-C-D
assert set(g.dfs('A')) == {'A','B','C','D'}
g.add_edge('X','Y'); assert g.components() == 2
assert topo_sort(4, [(0,1),(0,2),(1,3),(2,3)])[0] == 0
assert topo_sort(2, [(0,1),(1,0)]) is None       # the cycle is detected
print("Graph OK")
```
</details>

---

## World 6 · Solution: DP (Climbing Stairs / Coin Change / Longest Common Subsequence)

```python
def climb(n):                                   # ways to climb stairs (1 or 2 steps)
    if n <= 2: return n
    a, b = 1, 2                                 # keeping just the previous 2 means O(1) space
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

def coin_change(coins, amount):                 # minimum number of coins
    INF = float('inf')
    dp = [0] + [INF] * amount                   # dp[x] = min coins for amount x
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x:
                dp[x] = min(dp[x], dp[x - c] + 1)
    return dp[amount] if dp[amount] != INF else -1

def lcs(s, t):                                  # length of the longest common subsequence
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

**Complexity**: climb O(n) / O(1) space, coin_change O(amount × number of coin types), lcs O(mn).

<details>
<summary>🧪 Self-test</summary>

```python
assert climb(5) == 8
assert coin_change([1, 5, 10, 25], 30) == 2      # 25 + 5
assert lcs("ABCBDAB", "BDCAB") == 4              # "BCAB"
print("DP OK")
```
</details>

---

## World 12 · Solution: Calculator-Language Interpreter (lexer → parser → evaluation)

Key point: embed precedence in the **grammar's hierarchy** (`expr` calls `term`, `term` calls `factor`). Recursive descent.

```python
def calc(expr, env=None):
    env = {} if env is None else env

    # --- ① Lexical analysis: string → token sequence ---
    toks, i = [], 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1; continue
        if c.isdigit() or c == '.':
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'): j += 1
            toks.append(('num', float(expr[i:j]))); i = j
        elif c.isalpha():
            j = i
            while j < len(expr) and expr[j].isalnum(): j += 1
            toks.append(('id', expr[i:j])); i = j
        else:
            toks.append((c, c)); i += 1

    # --- ② Parsing + ③ Evaluation (recursive descent) ---
    pos = 0
    def peek(): return toks[pos][0] if pos < len(toks) else None
    def eat():
        nonlocal pos; t = toks[pos]; pos += 1; return t

    def factor():
        t = peek()
        if t == '(':
            eat(); v = expression(); eat(); return v   # parentheses
        if t == '-':
            eat(); return -factor()                    # unary minus
        tok = eat()
        if tok[0] == 'num': return tok[1]
        if tok[0] == 'id':  return env[tok[1]]         # variable reference

    def term():                                        # * / bind tighter than + -
        v = factor()
        while peek() in ('*', '/'):
            op = eat()[0]; r = factor()
            v = v * r if op == '*' else v / r
        return v

    def expression():
        v = term()
        while peek() in ('+', '-'):
            op = eat()[0]; r = term()
            v = v + r if op == '+' else v - r
        return v

    # assignment (id = ...) or an expression
    if len(toks) >= 2 and toks[0][0] == 'id' and toks[1][0] == '=':
        name = toks[0][1]; pos = 2
        env[name] = expression()
        return env[name]
    return expression()
```

**Confirming the key point**: `1 + 2 * 3` evaluates to 7 because `expression` first evaluates `term` (= `2*3`) and then adds. The precedence emerges naturally from the **structure of the grammar**, not from the code.

<details>
<summary>🧪 Self-test</summary>

```python
env = {}
assert calc("1 + 2 * 3") == 7        # precedence
assert calc("(1 + 2) * 3") == 9      # parentheses
assert calc("x = 3 + 4", env) == 7   # assignment
assert calc("x * 2", env) == 14      # variable reference
assert calc("-5 + 2") == -3          # unary minus
print("Calculator OK")
```
</details>

---

## World 13 · Solution: DFA Simulator (Divisibility-by-3 Test)

Key point: state = "the value so far mod 3." Reading a bit b makes the value `2*value + b`. You can test divisibility without any division.

```python
def dfa_mult3(bits):
    state = 0                                   # state = remainder mod 3
    trans = {
        (0, '0'): 0, (0, '1'): 1,               # qᵣ --b--> q_(2r+b mod 3)
        (1, '0'): 2, (1, '1'): 0,
        (2, '0'): 1, (2, '1'): 2,
    }
    for b in bits:
        state = trans[(state, b)]
    return state == 0                           # accepting state = remainder 0

# generic DFA simulator (takes any transition table)
def run_dfa(transitions, start, accept, string):
    state = start
    for c in string:
        state = transitions[(state, c)]
    return state in accept
```

<details>
<summary>🧪 Self-test</summary>

```python
assert dfa_mult3(bin(9)[2:])  is True            # 9 is a multiple of 3
assert dfa_mult3(bin(0)[2:])  is True
assert dfa_mult3(bin(7)[2:])  is False
assert dfa_mult3(bin(123)[2:]) == (123 % 3 == 0)
print("DFA OK")
```
</details>

---

## 🏆 Tips for Clearing the Forge

Once you can **write these solutions yourself**, you have gone from a "user" of data structures and algorithms to a "builder" of them.
Every application (the B+ tree of the World 11 database, the GRAD systems) is built from combinations of these fundamentals.

One last time: **understanding when you read it and being able to write it are different. Type it out by hand yourself at least once.**

➡️ Back: [CS Quest Home](README.md) · [Complete Coding Problems](appendix-01-coding-problems.md) · [Concept Flashcards](appendix-05-flashcards.md)
