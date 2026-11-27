# 📙 付録 IV: 実装クエスト完全解答集 — 全部テスト済みのコード

> ここは「鍛冶神の工房」。各ワールドの **💻 実装クエスト**(「○○を自分で実装せよ」)には、
> これまで**あえて解答を載せなかった**。自力で書くことが最大の修行だからだ。
> だがそれでは「自分のコードが正しいか確かめられない」という声に応え、
> ここに**参考解答**をすべて用意した。すべて実際に実行してテスト済みだ。

## ⚠️ 使い方(これだけは守れ)

1. **まず必ず自分で全部書く。** いきなりここを見たら修行にならない
2. 自分のコードが**動いてから**、ここと照らし合わせる
3. 解答は **唯一の正解ではない**。動いて計算量が合っていれば、君の書き方でよい
4. 各解答の末尾に「**自己テスト**」を付けた。自分のコードでこれが通るか確かめよ
5. 言語は Python。自分の得意言語に移植すると、構造の理解がさらに深まる

> 💡 「読んで分かる」と「書ける」は別物だ。**写経でもいいから一度は自分の手で打ち込め。**

---

## World 2 ・ 解答 1: 動的配列(Dynamic Array)

ポイント: 満杯で容量 2 倍、サイズが容量の 1/4 で半減(償却 O(1) を保つ)。

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
            raise IndexError("out of range")     # 範囲外は明確に失敗させる
        return self._a[i]

    def _resize(self, c):
        b = [None] * c
        for i in range(self._n):
            b[i] = self._a[i]
        self._a = b
        self._cap = c

    def push(self, x):
        if self._n == self._cap:
            self._resize(2 * self._cap)          # 満杯なら倍に
        self._a[self._n] = x
        self._n += 1

    def insert(self, i, x):
        if self._n == self._cap:
            self._resize(2 * self._cap)
        for j in range(self._n, i, -1):          # 後ろを 1 つずつずらす
            self._a[j] = self._a[j - 1]
        self._a[i] = x
        self._n += 1

    def prepend(self, x):
        self.insert(0, x)

    def pop(self):
        x = self._a[self._n - 1]
        self._n -= 1
        if 0 < self._n <= self._cap // 4:        # スカスカなら縮小
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

**計算量**: push 償却 O(1)、at O(1)、insert/delete O(n)、find O(n)。

<details>
<summary>🧪 自己テスト</summary>

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

## World 2 ・ 解答 2: 単方向連結リスト

ポイント: `reverse` は 3 ポインタ。**先に次を退避**してから付け替える(World 2 の鍛冶屋の教え)。

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
            nxt = cur.next      # ① 次を退避
            cur.next = prev     # ② 矢印を逆に
            prev = cur          # ③ 前進
            cur = nxt           # ④ 前進
        self.head = prev
```

**計算量**: push_front/pop_front O(1)、push_back/insert/erase/reverse O(n)。

<details>
<summary>🧪 自己テスト</summary>

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

## World 2 ・ 解答 3: ハッシュテーブル(オープンアドレス法)

ポイント: 削除は**墓石(dead フラグ)**を置く。置かないと後続の探査が途切れる(World 2 の警告)。負荷率 0.7 でリサイズ。

```python
class HashTable:
    def __init__(self, cap=8):
        self._cap = cap
        self._n = 0
        self._keys = [None] * cap
        self._vals = [None] * cap
        self._dead = [False] * cap          # 墓石

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
                self._vals[i] = v; return       # 既存キーは上書き
            if self._dead[i] and first_dead < 0:
                first_dead = i                   # 墓石を再利用候補に
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
            self._dead[i] = True               # 墓石を立てる(消さない)
            self._n -= 1
```

**計算量**: add/exists/get/remove は平均 O(1)、最悪 O(n)。

<details>
<summary>🧪 自己テスト</summary>

```python
ht = HashTable()
for k in range(20): ht.add(f"k{k}", k * 10)
assert ht.exists("k5") and ht.get("k5") == 50 and ht.get("k19") == 190
ht.add("k5", 999); assert ht.get("k5") == 999          # 上書き
ht.remove("k5");   assert not ht.exists("k5") and ht.get("k7") == 70   # 墓石後も探査継続
print("HashTable OK")
```
</details>

---

## World 3 ・ 解答 1: 二分探索木(BST)

ポイント: 検証は**範囲 (lo, hi) を引き回す**。削除の 2 子ケースは**右部分木の最小値**で置換。

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
        return out                              # BST なら昇順になる

    def contains(self, v):
        n = self.root
        while n:
            if v == n.val: return True
            n = n.left if v < n.val else n.right
        return False

    def height(self, n="__root__"):
        if n == "__root__": n = self.root
        if not n: return -1                     # 空は -1、葉は 0
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
        if not lo < n.val < hi: return False    # 範囲外なら違反
        return self.is_bst(n.left, lo, n.val) and self.is_bst(n.right, n.val, hi)

    def delete(self, v):
        self.root = self._del(self.root, v)

    def _del(self, node, v):
        if not node: return None
        if v < node.val:
            node.left = self._del(node.left, v)
        elif v > node.val:
            node.right = self._del(node.right, v)
        else:                                   # 発見
            if not node.left:  return node.right    # 子 0 or 1
            if not node.right: return node.left
            succ = node.right                   # 子 2:右部分木の最小値で置換
            while succ.left: succ = succ.left
            node.val = succ.val
            node.right = self._del(node.right, succ.val)
        return node
```

**計算量**: 平衡なら O(log n)、最悪(一直線)O(n)。

<details>
<summary>🧪 自己テスト</summary>

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

## World 3 ・ 解答 2: 最大ヒープ(配列ベース)

ポイント: 親 `(i-1)//2`、子 `2i+1, 2i+2`。`heapify` は後ろの親から沈下で O(n)。

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
        for i in range(len(h.a) // 2 - 1, -1, -1):   # 後ろの親から沈下 = O(n)
            h._down(i)
        return h

    @staticmethod
    def heap_sort(arr):                          # 昇順を返す
        h = MaxHeap.heapify(arr); out = []
        while h.a:
            out.append(h.extract_max())
        return out[::-1]
```

**計算量**: insert/extract_max O(log n)、heapify O(n)、heap_sort O(n log n)。

<details>
<summary>🧪 自己テスト</summary>

```python
h = MaxHeap()
for x in [3, 1, 4, 1, 5, 9, 2, 6]: h.insert(x)
assert h.get_max() == 9 and h.extract_max() == 9 and h.get_max() == 6
assert MaxHeap.heap_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]
print("MaxHeap OK")
```
</details>

---

## World 4 ・ 解答: マージソート と クイックソート

```python
def mergesort(a):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    L, R = mergesort(a[:m]), mergesort(a[m:])
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):            # 2 つのソート済み列を混ぜる
        if L[i] <= R[j]:                        # <= で安定性を保つ
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    out.extend(L[i:]); out.extend(R[j:])
    return out

import random
def quicksort(a):
    a = a[:]                                    # 非破壊
    def qs(lo, hi):
        if lo >= hi: return
        p = random.randint(lo, hi)              # ランダムピボットで最悪を回避
        a[p], a[hi] = a[hi], a[p]
        pivot, i = a[hi], lo
        for j in range(lo, hi):                 # Lomuto パーティション
            if a[j] <= pivot:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        qs(lo, i - 1); qs(i + 1, hi)
    qs(0, len(a) - 1)
    return a
```

**計算量**: マージ 常に O(n log n)・安定・空間 O(n)。クイック 平均 O(n log n)・最悪 O(n²)・in-place。

<details>
<summary>🧪 自己テスト</summary>

```python
t = [5, 2, 9, 1, 7, 2, 8, 3]
assert mergesort(t) == sorted(t) and quicksort(t) == sorted(t)
assert mergesort([]) == [] and quicksort([1]) == [1]      # 空・単一の境界
print("Sorts OK")
```
</details>

---

## World 5 ・ 解答: グラフ(BFS / DFS / 最短経路 / 連結成分 / トポロジカルソート)

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

    def shortest_path(self, s, t):              # 重みなし最短経路(辺数最小)
        if s == t: return [s]
        prev, q = {s: None}, deque([s])
        while q:
            u = q.popleft()
            for w in self.adj[u]:
                if w not in prev:
                    prev[w] = u
                    if w == t:                  # 親をたどって経路復元
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

    def components(self):                       # 連結成分の数
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

def topo_sort(n, edges):                        # Kahn 法。閉路があれば None
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
    return order if len(order) == n else None   # 全部消えなければ閉路あり
```

**計算量**: BFS/DFS/トポロジカルソート すべて O(V + E)。

<details>
<summary>🧪 自己テスト</summary>

```python
g = Graph()
for u, v in [('A','B'),('A','C'),('B','D'),('C','D')]: g.add_edge(u, v)
assert g.bfs('A')[0] == 'A' and set(g.bfs('A')) == {'A','B','C','D'}
assert len(g.shortest_path('A','D')) == 3        # A-B-D or A-C-D
assert set(g.dfs('A')) == {'A','B','C','D'}
g.add_edge('X','Y'); assert g.components() == 2
assert topo_sort(4, [(0,1),(0,2),(1,3),(2,3)])[0] == 0
assert topo_sort(2, [(0,1),(1,0)]) is None       # 閉路は検出
print("Graph OK")
```
</details>

---

## World 6 ・ 解答: DP(階段・コイン両替・最長共通部分列)

```python
def climb(n):                                   # 階段の上り方(1 or 2 段)
    if n <= 2: return n
    a, b = 1, 2                                 # 直前 2 つだけ持てば O(1) 空間
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

def coin_change(coins, amount):                 # 最小枚数
    INF = float('inf')
    dp = [0] + [INF] * amount                   # dp[x] = 金額 x の最小枚数
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x:
                dp[x] = min(dp[x], dp[x - c] + 1)
    return dp[amount] if dp[amount] != INF else -1

def lcs(s, t):                                  # 最長共通部分列の長さ
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

**計算量**: climb O(n)/空間 O(1)、coin_change O(amount × 種類)、lcs O(mn)。

<details>
<summary>🧪 自己テスト</summary>

```python
assert climb(5) == 8
assert coin_change([1, 5, 10, 25], 30) == 2      # 25 + 5
assert lcs("ABCBDAB", "BDCAB") == 4              # "BCAB"
print("DP OK")
```
</details>

---

## World 12 ・ 解答: 電卓言語インタプリタ(lexer → parser → 評価)

ポイント: 優先順位を**文法の階層**に埋め込む(`expr` が `term` を、`term` が `factor` を呼ぶ)。再帰下降。

```python
def calc(expr, env=None):
    env = {} if env is None else env

    # --- ① 字句解析: 文字列 → トークン列 ---
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

    # --- ② 構文解析 + ③ 評価(再帰下降) ---
    pos = 0
    def peek(): return toks[pos][0] if pos < len(toks) else None
    def eat():
        nonlocal pos; t = toks[pos]; pos += 1; return t

    def factor():
        t = peek()
        if t == '(':
            eat(); v = expression(); eat(); return v   # 括弧
        if t == '-':
            eat(); return -factor()                    # 単項マイナス
        tok = eat()
        if tok[0] == 'num': return tok[1]
        if tok[0] == 'id':  return env[tok[1]]         # 変数参照

    def term():                                        # * / は + - より優先
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

    # 代入 (id = ...) か式か
    if len(toks) >= 2 and toks[0][0] == 'id' and toks[1][0] == '=':
        name = toks[0][1]; pos = 2
        env[name] = expression()
        return env[name]
    return expression()
```

**ポイントの確認**: `1 + 2 * 3` が 7 になるのは、`expression` が先に `term`(= `2*3`)を評価してから足すから。優先順位がコードでなく**文法の構造**から自然に出ている。

<details>
<summary>🧪 自己テスト</summary>

```python
env = {}
assert calc("1 + 2 * 3") == 7        # 優先順位
assert calc("(1 + 2) * 3") == 9      # 括弧
assert calc("x = 3 + 4", env) == 7   # 代入
assert calc("x * 2", env) == 14      # 変数参照
assert calc("-5 + 2") == -3          # 単項マイナス
print("Calculator OK")
```
</details>

---

## World 13 ・ 解答: DFA シミュレータ(3 の倍数判定)

ポイント: 状態 = 「ここまでの値 mod 3」。ビット b を読むと値は `2*値 + b`。割り算なしで倍数判定できる。

```python
def dfa_mult3(bits):
    state = 0                                   # 状態 = 余り mod 3
    trans = {
        (0, '0'): 0, (0, '1'): 1,               # qᵣ --b--> q_(2r+b mod 3)
        (1, '0'): 2, (1, '1'): 0,
        (2, '0'): 1, (2, '1'): 2,
    }
    for b in bits:
        state = trans[(state, b)]
    return state == 0                           # 受理状態 = 余り 0

# 汎用 DFA シミュレータ(任意の遷移表を受け取る)
def run_dfa(transitions, start, accept, string):
    state = start
    for c in string:
        state = transitions[(state, c)]
    return state in accept
```

<details>
<summary>🧪 自己テスト</summary>

```python
assert dfa_mult3(bin(9)[2:])  is True            # 9 は 3 の倍数
assert dfa_mult3(bin(0)[2:])  is True
assert dfa_mult3(bin(7)[2:])  is False
assert dfa_mult3(bin(123)[2:]) == (123 % 3 == 0)
print("DFA OK")
```
</details>

---

## 🏆 工房クリアの心得

ここにある解答が**自分でも書けるようになったら**、君はデータ構造とアルゴリズムを「使う側」から「作れる側」になった。
すべての応用(World 11 のデータベースの B+木、GRAD のシステム)は、この基礎の組み合わせでできている。

最後にもう一度: **読んで分かることと、書けることは違う。一度は必ず自分の手で打て。**

➡️ 戻る: [CS Quest ホーム](README.md) ・ [コーディング問題大全](appendix-01-coding-problems.md) ・ [概念フラッシュカード](appendix-05-flashcards.md)
