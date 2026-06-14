# 🌑 EXTRA: The Hidden Dungeons — Advanced Topics

> Dungeons that aren't on any map, open only to those who have defeated the Demon Lord.
> Clearing them isn't required. But the treasure you find here is
> **the knowledge that working engineers truly use in the field.**
> Each dungeon cleared grants **150 XP** + the badge "🌑 One Who Peers into the Abyss."

Each dungeon is structured as "Entrance (the motivation) → Trial (what you learn) → Treasure (the resources)."
Every resource links to the relevant section of the original [Coding Interview University](https://github.com/jwasham/coding-interview-university).

---

## 🏯 Dungeon 1: The Tower of Balanced Trees

**Entrance**: As you learned in World 3, a plain BST degrades to O(n) on sorted input.
The dwellers of this tower **rotate the tree on every insertion to fiercely defend a height of O(log n)**.

**Trial**:
- **AVL trees** — the strict school that keeps the left/right height difference within 1. Understand the 4 patterns of rotation.
- **Red-black trees** — the pragmatic school that paints nodes with colors and keeps balance more loosely. This is the true identity behind many languages' TreeMap / std::map.
- **B-trees / B+ trees** — giants that pack many keys into a single node. The heart of **database indexes and file systems**. Since disks read "in block units," World 7's discussion of locality applies directly here.

**Treasure**: the video collection in the original [Balanced search trees](https://github.com/jwasham/coding-interview-university#balanced-search-trees) section

## 🗝️ Dungeon 2: The Cathedral of Cryptography

**Entrance**: In World 8 you learned that HTTPS "exchanges keys with public-key crypto, then talks with a symmetric key." In the cathedral, you peer inside that magic circle.

**Trial**:
- **Symmetric-key cryptography (AES)** — encrypt and decrypt with the same key. Fast, but the problem of "how to hand over the key" remains.
- **Public-key cryptography (RSA, etc.)** — encrypt with a public key, decrypt with a private key. Solves the key-distribution problem.
- **Hash functions (SHA-2, etc.)** — one-way fingerprints. For tamper detection and password storage (+ salt).
- Become able to explain why passwords are "hashed and stored" rather than "encrypted and stored."

**Treasure**: the original [Cryptography](https://github.com/jwasham/coding-interview-university#cryptography) section (Khan Academy and others)

## 🧭 Dungeon 3: The Observatory of A*

**Entrance**: Dijkstra's algorithm spreads its search in all directions. But a map app knows "the destination is that way."

**Trial**:
- **Heuristic function h(v)** — an optimistic estimate of the distance to the goal (e.g., straight-line distance)
- A* searches from the vertex with the smallest "cost so far g + estimate h"
- When h **never overestimates (is admissible)** the real cost, A* guarantees an optimal solution
- Standard equipment for NPC pathfinding in games, car navigation, and puzzle solvers (the 15-puzzle)

**Treasure**: the original [A*](https://github.com/jwasham/coding-interview-university#a) section

## 🎲 Dungeon 4: The Gambling Hall of Probability

**Entrance**: "Wager just a little accuracy, and you gain orders of magnitude in memory and speed" — a building where that kind of bet pays off.

**Trial**:
- **Bloom filter** — answers "definitely not present" or "maybe present" using just a few bits per element. False positives happen, but never false negatives. Shines in a web crawler's "already visited" check, avoiding unnecessary DB reads, and more.
- **HyperLogLog** — the magic that estimates the unique count of billions of elements in about 1.5 KB
- **Skip list** — a probabilistic sorted list that builds its levels by coin flips. Achieves the same O(log n) as a balanced tree, without rotations (the true identity behind Redis's Sorted Set)

**Treasure**: the original [Bloom Filter](https://github.com/jwasham/coding-interview-university#bloom-filter) / [HyperLogLog](https://github.com/jwasham/coding-interview-university#hyperloglog) / [Skip lists](https://github.com/jwasham/coding-interview-university#skip-lists)

## 🤝 Dungeon 5: The Round Table of the Union

**Entrance**: On the round table sits a device that keeps answering, at blazing speed, "do these two islands belong to the same country?"

**Trial**:
- **Union-Find (disjoint-set data structure)** — `find(x)` (returns the representative of the group it belongs to) and `union(x, y)` (merge groups)
- With the two optimizations of **path compression** and **union by rank**, it reaches nearly O(1) (the inverse Ackermann function)
- Shines in network connectivity checks, Kruskal's algorithm (minimum spanning tree), and image region segmentation

**Treasure**: the original [Disjoint Sets & Union Find](https://github.com/jwasham/coding-interview-university#disjoint-sets--union-find)

## 📜 Dungeon 6: The Library of Strings

**Entrance**: Librarians searching for a passage in a vast collection can't get the job done with the naive brute force of O(nm).

**Trial**:
- **Trie** — a tree with characters as edges. The standard for prefix search and autocomplete.
- **KMP algorithm** — preprocesses the pattern's own structure (the failure function) and searches in O(n + m)
- **Rabin-Karp algorithm** — compares substrings quickly with a rolling hash. Also used for plagiarism detection.

**Treasure**: the original [String searching & manipulations](https://github.com/jwasham/coding-interview-university#string-searching--manipulations) / [Tries](https://github.com/jwasham/coding-interview-university#tries)

## 🏗️ Dungeon 7: The Sky Castle of Large-Scale Design (raid for the experienced)

**Entrance**: "Design a Twitter that won't fall over even with 100 million users."
A large-scale raid you can't take on alone. The custom is to build up real work experience before attempting it (even the original treats this as an interview topic for those with 4+ years of experience).

**Trial**:
- The vocabulary of scalability: vertical/horizontal scaling, load balancers, replication, sharding, the CAP theorem, caching (World 7's knowledge grown to city scale)
- The design-interview pattern of "clarify requirements → rough estimation (back-of-the-envelope math) → API design → data model → crush the bottlenecks"

**Treasure**: the original [System Design, Scalability, Data Handling](https://github.com/jwasham/coding-interview-university#system-design-scalability-data-handling) —
in particular, [The System Design Primer](https://github.com/donnemartin/system-design-primer) is the complete walkthrough for the sky castle

---

## Deeper into the Abyss

If you still want to dive further, head to the following sections of the original. They're all treasures of the "you'll meet them someday" kind:

- [Information theory](https://github.com/jwasham/coding-interview-university#information-theory-videos) / [entropy](https://github.com/jwasham/coding-interview-university#entropy) / [compression](https://github.com/jwasham/coding-interview-university#compression)
- [Parallel programming](https://github.com/jwasham/coding-interview-university#parallel-programming)
- [Compilers](https://github.com/jwasham/coding-interview-university#compilers)
- [k-D trees](https://github.com/jwasham/coding-interview-university#k-d-trees) / [linear programming](https://github.com/jwasham/coding-interview-university#linear-programming-videos) / [geometry & convex hull](https://github.com/jwasham/coding-interview-university#geometry-convex-hull-videos)
- [Discrete math](https://github.com/jwasham/coding-interview-university#discrete-math)
- [List of computer science open courses](https://github.com/jwasham/coding-interview-university#computer-science-courses)

> An adventure never ends. But you can now **open any door on your own.** That is the true reward for clearing this game.
