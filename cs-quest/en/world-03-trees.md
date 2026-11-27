# 🌲 World 3: The Tree Labyrinth — Trees, Binary Search Trees, and Heaps

> Beyond the town gates lies a strange, upside-down forest.
> **The roots float in the sky, and the leaves grow downward toward the earth.**
> Only two hermits know the way out of this labyrinth ——
> "BST, the Hermit of Search" and "Heap, the Hermit of Priority."

**What you'll learn in this chapter (university equivalent: "Data Structures, Lectures 6–8")**
- Tree terminology and properties
- The four traversals
- Binary search tree (BST) operations and complexity
- How heaps (priority queues) work

---

## 📖 Lecture 1: The Language of the Forest (10 XP)

A **tree** is a connected graph with no cycles, representing hierarchy. CS trees are drawn upside down.

```
            (root)
           /      \
     (internal)  (internal)
       /    \         \
   (leaf)  (leaf)    (leaf)
```

| Term | Meaning |
|---|---|
| Root | The topmost node |
| Parent / child / sibling | Directly connected vertical and horizontal relations |
| Leaf | A node with no children |
| Depth | Number of edges from the root to a node |
| Height | Number of edges from a node to its deepest leaf |
| Binary tree | Each node has at most 2 children |

**A crucial fact**: a binary tree of height h can hold at most 2^(h+1) − 1 nodes.
Conversely, if you pack n nodes in **a balanced way**, the height stays **O(log n)**.
That logarithmic height is the very source of the speed trees grant us.

## 📖 Lecture 2: How to Walk the Labyrinth — The Four Traversals (10 XP)

```
        4
       / \
      2   6
     / \ / \
    1  3 5  7
```

| Traversal | Order | Result on the tree above | Used for |
|---|---|---|---|
| Preorder | self → left → right | 4 2 1 3 6 5 7 | Copying a tree, prefix notation |
| **Inorder** | left → self → right | **1 2 3 4 5 6 7** | **On a BST, values come out sorted!** |
| Postorder | left → right → self | 1 3 2 5 7 6 4 | Deleting a tree, postfix notation |
| Level-order (BFS) | shallow levels first | 4 2 6 1 3 5 7 | Shortest distance, level display |

Pre/in/postorder are implemented with recursion (or a stack); level-order uses a queue.
The stack and queue you trained with in World 2 become weapons here.

## 📖 Lecture 3: The Hermit of Search — Binary Search Trees (10 XP)

**The BST Law (invariant)**: at every node, `all values in the left subtree < my value < all values in the right subtree`

Thanks to this law, searching is just "compare and descend left or right."
**The candidates halve at every step** —— it's binary search in tree form.

| Operation | Well-balanced tree | Worst case (a straight line) |
|---|---|---|
| Search / insert / delete | O(log n) | O(n) |

⚠️ **Insert an already-sorted sequence in order and the tree degenerates into a straight line (effectively a linked list), collapsing to O(n).**
Self-balancing trees (AVL trees, red-black trees — they await in the Hidden Dungeons) prevent this.
In practice it suffices to know: "the standard TreeMap / std::map is a red-black tree with guaranteed O(log n)."

**The three deletion cases** (interview favorite):
1. A leaf → just cut it off
2. One child → lift the child up to take its place
3. Two children → swap with the **minimum of the right subtree** (the inorder successor), then delete that minimum node

📺 [MIT 6.006 - Binary Search Trees (video)](https://www.youtube.com/watch?v=76dhtgZt38A)

## 📖 Lecture 4: The Hermit of Priority — Heaps (10 XP)

**The Max-Heap Law**: parent ≥ child (that's all — left/right order doesn't matter)

It's a **complete binary tree** (every level full except possibly the last, filled left-to-right), so it **fits in an array**:

```
Index:  0  1  2  3  4  5
Array: [9, 7, 8, 3, 5, 6]
Children of i = 2i+1, 2i+2 / parent of i = (i−1)//2
```

| Operation | Complexity | How |
|---|---|---|
| Peek at the max | O(1) | Just look at the root |
| Insert | O(log n) | Place at the end and **sift up** while bigger than the parent |
| Extract max | O(log n) | Swap root with the last element, remove it, **sift down** the root |
| Build a heap from an array (heapify) | **O(n)** | Sift down from the last parent backwards (NOT n log n — beware!) |

A heap is the very implementation of a **priority queue** — the right answer whenever you "always want the max (or min) next."
It is the heart of Dijkstra's algorithm (World 5) and heapsort (World 4).

📺 [Heap lecture (video)](https://www.youtube.com/watch?v=B7hVxCmfPtM)

---

## ⚔️ Quests

### Quest 1: Reading the Labyrinth Map (20 XP)

Insert these values into an empty BST in this order: `50, 30, 70, 20, 40, 60, 80`

1. Draw the resulting tree
2. What does the inorder traversal output?
3. What does the tree look like after deleting 40?
4. Then after deleting 50 (the root, with two children)?

<details>
<summary>📜 Answers</summary>

1. A perfect tree: 50 at the root, 30/70 as children, 20/40/60/80 as grandchildren
2. 20 30 40 50 60 70 80 (sorted order!)
3. 40 is a leaf, so it simply disappears
4. The right subtree's minimum, **60**, is lifted to the root, and the original 60 (a leaf) is deleted
</details>

### Quest 2: 💻 Implementation Quest "Apprentice to the BST Hermit" (50 XP)

Implement a BST: `insert`, `get_node_count`, `print_values (inorder)`, `delete_tree`,
`is_in_tree`, `get_height`, `get_min`, `get_max`, `is_binary_search_tree` (validation), `delete_value`,
`get_successor` (the next value in inorder).

⚠️ The trap in `is_binary_search_tree`: comparing "myself and my direct children" is not enough.
**Pass down the (min, max) range for the entire subtree as arguments.**

### Quest 3: 💻 Implementation Quest "Apprentice to the Heap Hermit" (50 XP)

Implement an array-based max-heap: `insert`, `sift_up`, `get_max`, `extract_max`,
`sift_down`, `remove(i)`, `heapify`, `heap_sort`.

### Quest 4: The Gatekeeper's Riddles (20 XP)

1. What is the height of a complete binary tree with n nodes?
2. BST or heap — which is better at "enumerating the k smallest values in order," and why?
3. What is the intuitive reason heapify only costs O(n)?

<details>
<summary>📜 Answers</summary>

1. ⌊log₂ n⌋ = O(log n)
2. **BST** — an inorder walk visits values in sorted order. A heap only knows its root, and siblings have no order between them.
3. Sift-down cost is proportional to height, but **most nodes live near the bottom of the tree where the height is small**.
   There are about n/2^(h+1) nodes at height h, and Σ h·n/2^(h+1) converges to O(n).
</details>

---

## 👹 Boss Battle: The Labyrinth's Master, "The Twin-Phase Treant" (100 XP)

Close your notes and fight. Win with 70% or more.

1. State the BST invariant precisely (careful — it's not just about direct children).
2. What condition must hold for BST operations to be O(log n), and give an input that breaks it.
3. Describe how to perform an inorder traversal **without recursion**, using a stack.
4. State, step by step, how to extract the maximum from a max-heap.
5. "I want to keep the top k items from a stream at all times." Which data structure, used how? Complexity?
6. Given a binary tree, what data structure and procedure implement level-order traversal?

<details>
<summary>📜 Answers</summary>

1. For any node v: every element of v's left subtree < v's value < every element of v's right subtree.
2. The tree height must stay O(log n) (balance). Inserting an already-sorted sequence produces a straight line and degrades to O(n).
3. Descend left from the current node, pushing onto the stack; at a dead end, pop and output, then move to the right child. Stop when the stack is empty and there is no current node.
4. Take the root (the max) → move the last element to the root → shrink the heap by 1 → sift the root down to its proper place.
5. **A min-heap of size k**. If a new element is larger than the heap's minimum, replace the minimum and sift down. O(log k) per element, O(n log k) overall.
6. **A queue**. Enqueue the root → dequeue a node, output it, enqueue its children → repeat until empty.
</details>

---

🏆 **Victory Reward**: Badge "🌳 Sage of the Forest" + 100 XP

➡️ On to the next world: [World 4: The Sorting Volcano](world-04-sorting.md)
