# 🌊 World 5: The Graph Ocean — Graph Theory and Search

> With the volcano behind you, a vast ocean dotted with countless islands spreads before you.
> Islands are linked by sea routes — some one-way, some with steep fares due to storms.
> Whoever masters this ocean masters the world itself.
> Because — **social networks, map apps, compilers, the internet: they are all graphs.**

**What you'll learn in this chapter (the university equivalent of "Algorithms, Lectures 6–9")**
- Graph terminology and the two ways to represent a graph
- BFS (breadth-first search) and DFS (depth-first search)
- Topological sort
- Dijkstra's algorithm (single-source shortest paths)

> As the original says: "**Graphs can represent many problems in CS, making them a hugely important field. They show up often, too.**"
> This world is worth your time.

---

## 📖 Lecture 1: How to Read a Sea Chart (10 XP)

A **graph G = (V, E)** is a pair of a set of vertices V and a set of edges E.

| Term | Meaning | Example |
|---|---|---|
| Undirected graph | Edges have no direction | Friendships |
| Directed graph | Edges have direction | Twitter follows, task dependencies |
| Weighted graph | Edges have a cost | Road distance, fare |
| Degree | Number of edges incident to a vertex | Number of friends |
| Path / cycle | A route along vertices / a route back to the start | |
| Connected component | A cluster of mutually reachable vertices | |
| DAG | A directed graph with no cycles | Build dependencies, course prerequisites |

### The Two Representations

```
Graph:   A — B
         |   |
         C — D
```

**Adjacency list** (almost always this one in practice):
```
A: [B, C]
B: [A, D]
C: [A, D]
D: [B, C]
```

**Adjacency matrix**:
```
    A B C D
A [ 0 1 1 0 ]
B [ 1 0 0 1 ]
C [ 1 0 0 1 ]
D [ 0 1 1 0 ]
```

| | Adjacency list | Adjacency matrix |
|---|---|---|
| Memory | O(V + E) | O(V²) |
| "Is there an edge u→v?" | O(degree) | O(1) |
| Enumerate neighbors | O(degree) | O(V) |
| When to use | Sparse graphs (most of reality) | Dense graphs, or when you frequently query edge existence |

## 📖 Lecture 2: Two Navigators — BFS and DFS (10 XP)

### ⚓ BFS (breadth-first search) — "Visit the Nearest Islands First"

Use a **queue** to spread out from the start like ripples on water.

```
BFS(G, s):
    queue = [s], visited = {s}
    while queue is not empty:
        v = dequeue()
        for u in G.neighbors(v):
            if u not in visited:
                visited.add(u); enqueue(u)
```

- Complexity **O(V + E)**
- Finds the **shortest path in an unweighted graph** (fewest edges) — BFS's greatest weapon
- Record the "parent" at visit time and you can reconstruct the path too

### 🤿 DFS (depth-first search) — "Dive as Deep as You Can"

Use a **stack** (or recursion) to push down a single path and back up at dead ends.

```
DFS(G, v):
    visited.add(v)
    for u in G.neighbors(v):
        if u not in visited:
            DFS(G, u)
```

- Complexity **O(V + E)**
- Specialties: **cycle detection**, **counting connected components**, **topological sort**, exhaustive maze search

**Rule of thumb for choosing**: hear "shortest" → BFS. "Examine everything / inspect the structure" → DFS.

## 📖 Lecture 3: A Sea Chart of Dependencies — Topological Sort (10 XP)

Line up the vertices of a **DAG** so that "every edge points front → back."
This is the mathematical essence of course ordering (Calculus I → Calculus II), build order, and task scheduling.

**DFS method**: record the order in which each vertex's DFS **finishes** (post-order), then reverse it at the end. O(V + E).
**Kahn's method**: put vertices with in-degree 0 into a queue, then repeatedly pop one and delete its edges. If there's a cycle, you get stuck partway (= it also detects cycles).

## 📖 Lecture 4: The Shortest Route Through a Stormy Sea — Dijkstra's Algorithm (10 XP)

When edges have **non-negative weights**, find the shortest distance from a start vertex to all vertices.

**Intuition**: among the routes extending from "settled ports," **greedily settle the port you can reach most cheaply.**
To quickly extract the minimum among the unsettled, use a **min-heap (the hermit from World 3!)**.

```
dijkstra(G, s):
    dist[v] = ∞ (all vertices), dist[s] = 0
    heap = [(0, s)]
    while heap is not empty:
        (d, v) = extract_min()
        if d > dist[v]: continue      # skip stale info
        for (u, w) in G.neighbors(v):
            if dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
                heap.insert((dist[u], u))
```

- Complexity **O((V + E) log V)** (with a binary heap)
- ⚠️ **Breaks if there are negative weights** (in that case use the Bellman–Ford algorithm — see the Hidden Dungeons)
- The prototype of route-finding in map apps (the real thing is sped up with A* and the like — also in the Hidden Dungeons)

📺 Recommended video: the MIT 6.006 lecture series in the original [Graphs section](https://github.com/jwasham/coding-interview-university#graphs)
(BFS / DFS / topological sort / Dijkstra)

---

## ⚔️ Quests

### Quest 1: Choosing a Sea Chart (20 XP)

Model each problem as a graph (what are the vertices, what are the edges, is it directed, what is the weight, what algorithm do you use).

1. You want to find everyone within 2 hops, "friends of friends."
2. You want to decide the build order of source code (A imports B, etc.).
3. You want the shortest travel time from station to station.
4. You want to decide whether a maze has an exit.

<details>
<summary>📜 Answer</summary>

1. Vertices = people, edges = friendships (undirected, unweighted). **BFS** to depth 2.
2. Vertices = files, edges = dependencies (directed). **Topological sort**. A cycle means a circular import.
3. Vertices = stations, edges = lines (weight = travel time, non-negative). **Dijkstra's algorithm**.
4. Vertices = cells, edges = adjacent cells. **DFS or BFS works** (if you only need reachability).
</details>

### Quest 2: 💻 Implementation Quest "The Navigator's License" (50 XP × 2)

Implement a graph with an adjacency list and write the following:

1. **BFS** (returns the visit order + reconstructs the shortest path between two vertices via `shortest_path(s, t)`)
2. **DFS** (both a recursive version and a stack version + `count_components()` that counts connected components)

Build 2–3 test graphs yourself and check that they match the predictions you drew on paper.

### Quest 3: 💻 Implementation Quest "Crossing the Sea of Dependencies" (50 XP)

Implement topological sort of a directed graph (DFS method or Kahn's method).
If there is a cycle, report it.

### Quest 4: The Harbor Catechism (20 XP)

1. In 1–2 sentences, why does BFS correctly find unweighted shortest paths?
2. How do you detect a cycle in a **directed** graph with DFS? (manage visit state with 3 colors)
3. Why does Dijkstra's algorithm break with negative edges?

<details>
<summary>📜 Answer</summary>

1. BFS discovers vertices in order of distance 0, 1, 2, …, so the distance at first arrival is the shortest.
2. Manage state as white (unvisited), gray (visiting = on the recursion stack), black (finished). **Finding an edge to a gray vertex (a back edge) means a cycle.**
3. Dijkstra is a greedy method that assumes "a distance once settled never shrinks again." With negative edges, a shorter path can appear after settling, so that assumption collapses.
</details>

---

## 👹 Boss Battle: The Lord of the Deep "The Kraken" (100 XP)

Close your notes and face it. Win with 70% or more.

1. Compare adjacency lists and adjacency matrices on memory and operation cost, and state when each fits.
2. Write the pseudocode for BFS and DFS (make the difference in data structures clear).
3. Given V islands and E sea routes, how do you decide in O(V + E) whether you can visit all islands (whether it's connected)?
4. What is the necessary and sufficient condition for a topological sort to exist?
5. Why can each step of Dijkstra "greedily settle the minimum unsettled vertex"? (explain using non-negative weights)
6. How do you do bipartite checking (whether vertices can be 2-colored) with BFS?

<details>
<summary>📜 Solution</summary>

1. List: O(V+E), fast neighbor enumeration, suits sparse graphs. Matrix: O(V²), O(1) edge-existence check, suits dense graphs.
2. BFS uses a queue, DFS a stack (or recursion). The skeletons are as in Lecture 2.
3. Run BFS/DFS from any vertex and check whether the number visited equals V.
4. The graph must be a **DAG (directed acyclic graph)**.
5. For a shorter path to the minimum unsettled vertex v to appear later, it would have to pass through an unsettled vertex, but the distance to that vertex is already at least v's, and adding non-negative edges can't make it shrink.
6. Color a vertex the opposite color of its parent at visit time in BFS. If you find an edge joining two same-colored vertices, it's not bipartite.
</details>

---

🏆 **Victory Reward**: the badge "🧭 Navigator of the Deep" + 100 XP

➡️ On to the next world: [World 6: The Recursion Desert & DP Ruins](world-06-recursion-dp.md)
