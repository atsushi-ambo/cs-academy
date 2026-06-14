# 📕 付録 I: コーディング問題大全 — 完全解説つき

> ここは「魔王城の修練場」。各ワールドで戦い方を学んだ君のための、**実戦問題と完全な解答**が並ぶ場所だ。
> 出題だけで放り出さない。**問題文 → 考え方 → 完成コード → 計算量の導出 → つまずきポイント**を全問に用意した。
> 他のサイトを調べなくても、ここだけで「解ける」状態になる。

## 📖 この問題集の使い方

1. **まず自分で 20〜30 分考える**(すぐ答えを見ない。詰まる経験そのものが学びだ)
2. 解けたら解答と比べる。解けなくても「考え方」だけ読んでもう一度挑戦する
3. コードは **Python** で示す(疑似コードに近く読みやすいため)。自分の得意言語に移植すると理解が深まる
4. 各問の「面接での一言」は、口頭で計算量や方針を説明する練習に使う

問題は易しい順に並んでいる。難易度は 🟢 易 / 🟡 中 / 🔴 難 で示す。

---

## 第1章: 配列と文字列(対応ワールド: World 2)

### 問題 1.1 — 二数の和 (Two Sum) 🟢

**問題**: 整数配列 `nums` と目標値 `target` が与えられる。和が `target` になる 2 要素の**添字**を返せ。各入力にはちょうど 1 組の答えがあると仮定してよい。

```
入力: nums = [2, 7, 11, 15], target = 9
出力: [0, 1]   (nums[0] + nums[1] = 2 + 7 = 9)
```

**考え方**: 素朴には全ペアを試す O(n²)。だが「`target − x` が過去に出たか」をハッシュテーブルで O(1) 照会すれば、配列を 1 回なめるだけで済む。**「過去に見た値を引きたい」→ ハッシュテーブル**(World 2 の合言葉)。

```python
def two_sum(nums, target):
    seen = {}                       # 値 -> その添字
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:            # 相方が既に出ていたか
            return [seen[need], i]
        seen[x] = i                 # 自分を記録(照会の後に入れるのが肝)
    return []                       # 仮定上ここには来ない
```

**計算量**: 時間 O(n)(各要素を 1 回処理、辞書操作は平均 O(1))/ 空間 O(n)(最悪 n 個記録)。

**つまずきポイント**:
- `seen[x] = i` を照会の**前**に置くと、`target` が `x` の 2 倍のとき自分自身を相方にしてしまう。必ず照会の後に記録する。
- 同じ値が複数あっても、添字を上書きする前に照会するので正しく動く。

**面接での一言**: 「ハッシュで相補値を引けば、二重ループの O(n²) を O(n) に落とせます。空間 O(n) と引き換えです。」

---

### 問題 1.2 — 重複の検出 (Contains Duplicate) 🟢

**問題**: 配列に同じ値が 2 回以上現れるなら `True`、すべて異なれば `False` を返せ。

**考え方**: 集合(set)に入れながら、既出なら即 `True`。これも「重複チェック → ハッシュ」。

```python
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

**計算量**: 時間 O(n) / 空間 O(n)。

**別解と比較**: ソートしてから隣接比較すると空間 O(1)(in-place ソート時)だが時間 O(n log n)。「空間を使ってでも速く」か「遅くてもメモリ節約」かのトレードオフを言えると強い。

---

### 問題 1.3 — 最大部分配列和 (Kadane のアルゴリズム) 🟡

**問題**: 整数配列(負数を含む)の中で、連続する部分配列の和の最大値を返せ。

```
入力: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
出力: 6   (部分配列 [4, -1, 2, 1] の和)
```

**考え方**: 「ここで終わる部分配列の最大和」を `cur` として左から更新する。各位置で選択肢は 2 つ —— **これまでの和に今の要素を足す**か、**今の要素から新しく始める**か。これは小さな DP(World 6)だ。

```python
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)       # 続けるか、ここから始め直すか
        best = max(best, cur)       # 全体の最大を更新
    return best
```

**計算量**: 時間 O(n) / 空間 O(1)。

**なぜ正しい?**: `cur` は「位置 i で終わる最大和」という不変条件を保つ。`cur + x` が `x` より小さいなら、過去を引きずるより捨てた方が得 —— だから始め直す。DP の状態定義「dp[i] = i で終わる最大和」、遷移「dp[i] = max(x, dp[i−1] + x)」がそのまま `cur` の更新になっている。

**つまずきポイント**: 全要素が負のとき空配列(和 0)を答えにしてはいけない(問題が「空も許す」と言わない限り)。初期値を `nums[0]` にしておけば最大の負数が正しく返る。

---

### 問題 1.4 — 文字列のアナグラム判定 🟢

**問題**: 2 つの文字列が互いのアナグラム(文字の並べ替え)かを判定せよ。

**考え方**: 各文字の**出現回数**が完全に一致すればアナグラム。ハッシュ(カウンタ)で数える。

```python
from collections import Counter

def is_anagram(s, t):
    if len(s) != len(t):            # 長さが違えば即否定(高速化)
        return False
    return Counter(s) == Counter(t)
```

**計算量**: 時間 O(n) / 空間 O(k)(k は文字種数。英小文字なら O(1))。

**面接での一言**: 「文字の頻度表が一致するかを見ます。ソートして比較する O(n log n) より、カウントの O(n) が速いです。」

---

## 第2章: 二ポインタとスライディングウィンドウ(対応: World 1・2)

### 問題 2.1 — ソート済み配列の二数の和 🟢

**問題**: **昇順ソート済み**の配列で、和が `target` になる 2 数の添字(1-indexed)を返せ。

**考え方**: ソート済みなら**両端から挟み撃ち**できる。和が大きすぎれば右を縮め、小さすぎれば左を伸ばす。ハッシュ不要で**空間 O(1)**。

```python
def two_sum_sorted(numbers, target):
    lo, hi = 0, len(numbers) - 1
    while lo < hi:
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]
        elif s < target:
            lo += 1                 # もっと大きくしたい → 左を右へ
        else:
            hi -= 1                 # もっと小さくしたい → 右を左へ
    return []
```

**計算量**: 時間 O(n) / 空間 O(1)。

**なぜ縮めて良い?**: `s < target` のとき、現在の `hi` と組める左端は `lo` が最善(これ以上左は小さくて届かない)。だから `lo` を捨てても最適解を逃さない —— World 14 の交換論法と同じ論法だ。

---

### 問題 2.2 — 重複なし最長部分文字列 🟡

**問題**: 文字列の中で、文字が重複しない最長の連続部分文字列の**長さ**を返せ。

```
入力: "abcabcbb"  →  出力: 3   ("abc")
入力: "pwwkew"    →  出力: 3   ("wke")
```

**考え方**: **スライディングウィンドウ**。右端を伸ばしながら、重複が出たら左端を縮める。各文字の「最後に見た位置」をハッシュで持つと左端を一気に飛ばせる。

```python
def longest_unique_substring(s):
    last = {}                       # 文字 -> 最後に出た添字
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:
            left = last[c] + 1      # 重複文字の次まで左端を飛ばす
        last[c] = right
        best = max(best, right - left + 1)
    return best
```

**計算量**: 時間 O(n)(右端は各 1 回、左端は単調に進むだけ)/ 空間 O(k)。

**つまずきポイント**: `last[c] >= left` の条件が肝。ウィンドウの**外**にある古い重複は無視しないと、左端が後退してバグる。

**面接での一言**: 「両ポインタが単調に右へ進むので、二重ループに見えて実は O(n) です。」

---

## 第3章: 連結リスト(対応: World 2)

### 問題 3.1 — 連結リストの反転 🟢

**問題**: 単方向連結リストを反転して新しい先頭を返せ。

**考え方**: 3 つのポインタ(`prev`, `cur`, `next`)で、各ノードの矢印を 1 本ずつ逆向きに付け替える。**順序が命** —— 先に次を退避しないと鎖の先を見失う(World 2 の鍛冶屋の教え)。

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next              # ① 次を退避(これを忘れると迷子)
        cur.next = prev             # ② 矢印を逆向きに
        prev = cur                  # ③ prev を前進
        cur = nxt                   # ④ cur を前進
    return prev                     # 新しい先頭は元の末尾
```

**計算量**: 時間 O(n) / 空間 O(1)。

**図で追う**:
```
初期:  None   1 → 2 → 3 → None
       prev  cur
1巡後: None ← 1   2 → 3
            prev  cur
最終:  None ← 1 ← 2 ← 3
                      prev(=新先頭)
```

---

### 問題 3.2 — 循環(サイクル)検出 🟡

**問題**: 連結リストに循環があるかを、**追加メモリ O(1)** で判定せよ。

**考え方**: **フロイドの「うさぎとかめ」**。1 歩ずつ進む `slow` と 2 歩ずつ進む `fast`。循環があれば必ず追いつく(World 2 のボス戦で予告した技)。

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next            # 1 歩
        fast = fast.next.next       # 2 歩
        if slow is fast:            # 追いついた = 循環あり
            return True
    return False                    # fast が末尾に到達 = 循環なし
```

**計算量**: 時間 O(n) / 空間 O(1)。

**なぜ必ず追いつく?**: 循環内では `fast` が `slow` に毎ステップ 1 ずつ近づく(相対速度 1)。距離は有限なので必ず 0 になる。ハッシュで訪問済みを記録する O(n) 空間の別解もあるが、O(1) 空間のこちらが美しい。

---

## 第4章: スタックとキュー(対応: World 2)

### 問題 4.1 — 有効な括弧 🟢

**問題**: `()[]{}` からなる文字列の括弧対応が正しいか判定せよ。

**考え方**: 開き括弧をスタックに積み、閉じ括弧で対応する開きを pop して種類が合うか確認。最後に空ならOK(World 2 のクエスト 5 の完全版)。

```python
def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s:
        if c in pairs.values():     # 開き括弧
            stack.append(c)
        elif c in pairs:            # 閉じ括弧
            if not stack or stack.pop() != pairs[c]:
                return False        # 空 pop か種類不一致
    return not stack                # 余りがなければ正しい
```

**計算量**: 時間 O(n) / 空間 O(n)。

**つまずきポイント**: 途中で「閉じが来たのにスタックが空」も不正(例: `")("`)。最後の `not stack` だけ見ると見逃すので、両方チェックする。

---

### 問題 4.2 — 最小値を O(1) で返すスタック 🟡

**問題**: `push` / `pop` / `top` に加え、**現在の最小値を O(1) で返す** `get_min` を持つスタックを設計せよ。

**考え方**: 「各時点の最小値」を**もう一本のスタック**に並走させる。push 時に「今の最小」を一緒に積めば、pop しても過去の最小が復活する。

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []              # 各時点の最小値を並走

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

**計算量**: 全操作 O(1) / 空間 O(n)。

**面接での一言**: 「最小値の履歴をスタックに持たせることで、pop による最小値の巻き戻しも O(1) になります。」

---

## 第5章: 木(対応: World 3)

### 問題 5.1 — 二分木の最大深さ 🟢

**問題**: 二分木の根から最も深い葉までの深さを返せ。

**考え方**: 木の問題はたいてい**再帰**。「自分の深さ = 1 + 左右の深い方」。基底は空ノード(深さ 0)。World 6 の再帰と World 3 の木の合わせ技。

```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

**計算量**: 時間 O(n)(全ノード訪問)/ 空間 O(h)(再帰スタック、h は木の高さ。最悪 O(n)、平衡なら O(log n))。

---

### 問題 5.2 — BST の検証 🟡

**問題**: 与えられた二分木が正しい BST かを判定せよ。

**考え方**: World 3 で予告した罠 —— 「自分と直接の子だけ」では不十分。**各部分木が取れる値の範囲 (lo, hi)** を上から引き回す。

```python
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root:
        return True
    if not (lo < root.val < hi):    # 範囲外なら違反
        return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))
```

**計算量**: 時間 O(n) / 空間 O(h)。

**つまずきポイント**: 左の子が「親より小さい」だけでなく「祖先が定めた下限より大きい」必要がある。範囲を狭めながら降りるのが核心。別解として「中順走査がソート列になるか」を見る方法もある。

---

### 問題 5.3 — 最近共通祖先 (LCA) 🟡

**問題**: BST 上で 2 ノード `p`, `q` の最近共通祖先を返せ。

**考え方**: BST の大小性を使う。両方が現ノードより小さければ左、大きければ右、**分かれた所が LCA**。

```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root             # 分岐点 = LCA
```

**計算量**: 時間 O(h) / 空間 O(1)。

---

## 第6章: グラフ(対応: World 5)

### 問題 6.1 — 島の数 (Number of Islands) 🟡

**問題**: `'1'`(陸)と `'0'`(水)のグリッドで、上下左右につながった陸の塊(島)の数を数えよ。

**考え方**: グリッドは**暗黙のグラフ**(各マスが頂点、隣接マスが辺)。未訪問の陸を見つけるたびに DFS/BFS で島全体を沈め(訪問済みにし)、その回数を数える。World 5 の連結成分の数え上げそのもの。

```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(r, c):                 # DFS で島を沈める
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'            # 訪問済みにする(再訪防止)
        sink(r+1, c); sink(r-1, c); sink(r, c+1); sink(r, c-1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                sink(r, c)          # この島を丸ごと消す
    return count
```

**計算量**: 時間 O(行 × 列)(各マス 1 回訪問)/ 空間 O(行 × 列)(最悪の再帰深さ)。

**つまずきポイント**: 訪問済みを記録しないと無限ループ。元のグリッドを書き換えたくない場合は別途 `visited` 集合を使う。

---

### 問題 6.2 — コース受講可能判定(閉路検出)🟡

**問題**: `n` 個のコースと前提条件 `[a, b]`(b を取る前に a が必要)が与えられる。全コースを受講できるか(=依存グラフに閉路がないか)判定せよ。

**考え方**: **トポロジカルソートの存在判定**。World 5 の Kahn 法(入次数 0 から消す)で、全ノードを消せれば閉路なし。

```python
from collections import deque

def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:      # b → a の依存
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
    return done == num_courses      # 全部消せた = 閉路なし
```

**計算量**: 時間 O(V + E) / 空間 O(V + E)。

**面接での一言**: 「依存関係は DAG であるべきで、トポロジカルソートできるか=閉路がないかと同値です。入次数 0 から削っていって全部消えれば受講可能です。」

---

## 第7章: 動的計画法(対応: World 6)

### 問題 7.1 — コイン両替(最小枚数)🟡

**問題**: コインの種類 `coins` と金額 `amount` が与えられる。`amount` を作る最小コイン枚数を返せ(作れなければ −1)。

**考え方**: DP の定石。状態「dp[x] = 金額 x を作る最小枚数」、遷移「dp[x] = min(各コイン c について dp[x−c] + 1)」。

```python
def coin_change(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount       # dp[0] = 0(0 円は 0 枚)
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x and dp[x - c] + 1 < dp[x]:
                dp[x] = dp[x - c] + 1
    return dp[amount] if dp[amount] != INF else -1
```

**計算量**: 時間 O(amount × len(coins)) / 空間 O(amount)。

**なぜ貪欲ではダメ?**: 「大きいコインから貪欲に」は coins=[1,3,4], amount=6 で破綻する(貪欲は 4+1+1=3 枚、最適は 3+3=2 枚)。選択の影響が後に波及するので全選択肢を比較する DP が必要 —— World 6 のボス戦の答えそのもの。

---

### 問題 7.2 — 最長増加部分列 (LIS) 🔴

**問題**: 配列の中で、狭義単調増加する部分列(連続でなくてよい)の最大長を返せ。

```
入力: [10, 9, 2, 5, 3, 7, 101, 18]  →  出力: 4   ([2, 3, 7, 18] など)
```

**考え方(O(n²) DP)**: 「dp[i] = i で終わる LIS の長さ」、遷移「自分より前で自分より小さい j について dp[i] = max(dp[j]) + 1」。

```python
def length_of_lis(nums):
    if not nums:
        return 0
    dp = [1] * len(nums)            # 各要素単体で長さ 1
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**計算量**: 時間 O(n²) / 空間 O(n)。

**さらに速く(O(n log n))**: 「長さ k の増加列の末尾の最小値」を配列 `tails` に保ち、各要素を二分探索で置き換える(World 4 の二分探索 + 貪欲)。面接で「もっと速くできる?」と聞かれたらこれを述べられると上級。

```python
import bisect

def length_of_lis_fast(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)         # 新しい最長を伸ばす
        else:
            tails[i] = x            # 末尾を小さく更新(将来の余地を広げる)
    return len(tails)
```

`tails` の長さが答え。`tails` 自体は LIS そのものではない点に注意(長さだけが正しい)。

---

### 問題 7.3 — 編集距離 (Levenshtein) 🔴

**問題**: 文字列 `word1` を `word2` に変える最小操作数を返せ。操作は 1 文字の挿入・削除・置換、各コスト 1。

**考え方**: World 6 のボス戦で定式化した 2 次元 DP。状態「dp[i][j] = word1 の先頭 i 文字を word2 の先頭 j 文字に変える最小コスト」。

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                # word1 を空にするには i 回削除
    for j in range(n + 1):
        dp[0][j] = j                # 空から word2 を作るには j 回挿入
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]         # 一致 → 操作不要
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],     # 削除
                    dp[i][j-1],     # 挿入
                    dp[i-1][j-1],   # 置換
                )
    return dp[m][n]
```

**計算量**: 時間 O(m × n) / 空間 O(m × n)(各行は前行しか使わないので O(n) に落とせる)。

**応用**: スペルチェッカ、DNA 配列比較、diff ツールの基礎。「実用で使われている DP」の代表例として語れる。

---

## 第8章: ヒープと二分探索(対応: World 3・1)

### 問題 8.1 — 配列の k 番目に大きい要素 🟡

**問題**: ソートせずに、配列の k 番目に大きい値を求めよ。

**考え方**: **サイズ k の最小ヒープ**を保つ。k 個を超えたら最小を捨てる。ヒープの根が答え(World 3 のボス戦の応用)。

```python
import heapq

def find_kth_largest(nums, k):
    heap = []                       # サイズ k の最小ヒープ
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)     # 最小を捨てる → 上位 k 個が残る
    return heap[0]                  # 根 = k 番目に大きい値
```

**計算量**: 時間 O(n log k) / 空間 O(k)。

**別解**: クイックセレクト(World 14)なら平均 O(n)。「最速は?」と聞かれたら述べられると良い。

---

### 問題 8.2 — 回転ソート配列の探索 🔴

**問題**: 昇順ソート後にある点で回転された配列(例 `[4,5,6,7,0,1,2]`)から、値 `target` の添字を O(log n) で探せ。

**考え方**: 二分探索の変種。中央を見れば、左半分か右半分の**少なくとも一方は必ずソート済み**。ソート済み側に target があるか範囲判定して探索範囲を半分にする。

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:           # 左半分がソート済み
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                # target は左半分に
            else:
                lo = mid + 1
        else:                               # 右半分がソート済み
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1                # target は右半分に
            else:
                hi = mid - 1
    return -1
```

**計算量**: 時間 O(log n) / 空間 O(1)。

**つまずきポイント**: `<=` か `<` かの境界判定が命。`nums[lo] <= nums[mid]` の等号は要素数が少ないとき(mid==lo)に必要。テストケース `[3,1]` target=1 などで境界を確かめること。

---

## 第9章: ビット演算(対応: World 7)

### 問題 9.1 — 1 つだけ現れる数 (Single Number) 🟢

**問題**: 1 つを除き全要素がちょうど 2 回現れる配列で、1 回だけの数を**空間 O(1)**で見つけよ。

**考え方**: **XOR の魔法**。`a ^ a = 0`、`a ^ 0 = a`。全部 XOR すればペアは消え、孤独な数だけ残る。

```python
def single_number(nums):
    result = 0
    for x in nums:
        result ^= x                 # ペアは打ち消し合う
    return result
```

**計算量**: 時間 O(n) / 空間 O(1)。

**面接での一言**: 「XOR は同じ値を打ち消すので、ハッシュもソートも要らず空間 O(1) で解けます。」

---

## 🏆 修練場クリアの心得

ここまでの問題が**何も見ずに**解けるようになったら、君は技術面接の実戦力を備えた。最後にパターンの地図を渡しておく:

| 問題の匂い | 疑うべき道具 |
|---|---|
| 「重複」「カウント」「相補値を引く」 | ハッシュテーブル(第1・2章) |
| 「ソート済み」「2 数を探す」「ペア」 | 二ポインタ(第2章) |
| 「連続部分文字列/配列で最長/最大」 | スライディングウィンドウ / Kadane(第1・2章) |
| 「最後に入れたものを最初に」「対応」「Undo」 | スタック(第4章) |
| 「木」「階層」「再帰的構造」 | DFS 再帰(第5章) |
| 「最短(重みなし)」「レベルごと」 | BFS(第6章) |
| 「つながり」「島」「連結成分」「依存」 | DFS/BFS/トポロジカルソート(第6章) |
| 「最小/最大の組み合わせ」「方法の数」「最適」 | 動的計画法(第7章) |
| 「上位 k 個」「常に最小/最大」 | ヒープ(第8章) |
| 「ソート済み」「O(log n) で探す」 | 二分探索(第8章) |

➡️ 次は実システムの設計へ: [付録 II: システム設計問題大全](appendix-02-system-design.md)
