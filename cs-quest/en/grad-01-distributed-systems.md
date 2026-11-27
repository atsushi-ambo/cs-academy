# ☁️ GRAD 1: The Sky Parliament of Distribution — Distributed Systems

> Beyond the clouds, at the gateway to the Heavens, stood a colossal round table.
> Sages scattered across a thousand islands deliberated together using nothing but carrier pigeons (delayed, lost),
> and yet they kept **a single ledger** in agreement.
> The chairperson asks: "Pigeons go astray, sages fall asleep, islands sink.
> **Even so, can you keep every sage's ledger consistent?** This is the Heavens' first trial."

**Corresponding graduate course**: MIT **6.824 / 6.5840 Distributed Systems** (public lectures, with Labs)
**Prerequisites**: World 8 (Networking), World 10 (Logs and concurrency), World 11 (Transactions)

**What you'll learn in this chapter**
- Why we distribute, and what breaks
- MapReduce and large-scale data processing
- Replication and consistency (linearizability)
- The consensus protocol Raft
- Distributed transactions (2PC)

---

## 📖 Lecture 1: The Premise of the Heavens — Failure Is the Norm, Not the Exception (20 XP)

There are three reasons to distribute: **performance** (exceed the limits of a single machine), **fault tolerance** (keep going when one machine dies), and **geography** (place data near users).
And the moment you distribute, new enemies appear:

- Machines **fail at any time** (with thousands of them, one dies every day)
- The network **delays, drops, duplicates, and reorders** (review from World 8)
- The worst enemy: **network partition** — whether "the other side died" or "the path was merely cut" is **fundamentally impossible to distinguish**

**The CAP theorem**: When a partition (P) occurs, consistency (C: everyone sees the same latest value) and
availability (A: always respond) **cannot both be guaranteed**. Which one to give up is the designer's choice
(a bank balance leans toward C, the like count on social media leans toward A — the classic examples).

## 📖 Lecture 2: The Assembly Line of a Thousand Islands — MapReduce (20 XP)

Google's framework for "**doing a giant's work with a crowd of ordinary folk**." The programmer writes just two pure functions:

```
map(document) → [(word, 1), (word, 1), ...]     # in parallel on each island
   ↓ shuffle (gather the same key onto the same island)
reduce(word, [1,1,1,...]) → (word, total)       # in parallel per key
```

- Fault handling is the framework's job: a dead worker's task is simply **re-run on another island**
- Re-running is safe because map/reduce are **deterministic and side-effect-free** — functional thinking becomes fault tolerance
- Successors (Spark, etc.) share the same core: "split the data across islands, send the computation to the islands"

## 📖 Lecture 3: Transcribing the Ledger — Replication and Consistency (20 XP)

Replicate the data across 3 islands and you're safe even if one island sinks — but a new problem is born: **the copies drift apart**.

A **consistency model** = "what behavior the replica group promises, as seen by the client":

| Model | Promise | Cost |
|---|---|---|
| **Linearizability** | Every operation appears to happen at "a single instant," visible in real-time order (= effectively looks like a single machine) | High (requires consensus) |
| Sequential consistency | Everyone sees the **same order** (not necessarily real time) | Medium |
| Eventual consistency | Once updates stop, replicas **eventually** agree | Low (fast, available) |

"I read a stale value," "I can't see my own write" — under weak models, these happen routinely.
Choosing the model by working backward from **how much anomaly the application can tolerate** is the graduate-level way to design.

## 📖 Lecture 4: How the Sky Parliament Votes — Raft (20 XP)

The heart of keeping replicas consistent is **consensus**: even with failures, all islands agree on the **same operation log**.

**Raft** is a consensus protocol designed with "understandability" as a goal. Three pillars:

1. **Leader election**: One leader per era (term). When the leader's heartbeat stops,
   each island, after a random timeout, runs for office and wins with a **majority** of votes
2. **Log replication**: All writes go through the leader. The leader appends to its log, distributes to followers, and
   **commits once a majority has written it** (the final evolution of "log first," continued from World 10)
3. **Safety**: The mathematics of majority rule — any two majorities must overlap (pigeonhole! World 9), so
   anyone unaware of a committed entry cannot become leader (the election restriction)

**Why a majority**: even if 2 of 5 islands sink, deliberation continues. During a partition, **only the larger side** can make progress, so
the ledger never splits into two (no split-brain).

**FLP impossibility** (the shadow of theory): in a fully asynchronous setting, consensus cannot be guaranteed. Raft pragmatically sidesteps this with timeouts (partial synchrony) — a concrete example of "designing to coexist with impossibility," which you learned in World 13.

## 📖 Lecture 5: A Deal Across Islands — Distributed Transactions (20 XP)

"Debit the account on island A, credit the account on island B" — World 11's ACID, across islands.

**Two-phase commit (2PC)**:
1. **Voting phase**: the coordinator asks all participating islands "can you commit?" → each island prepares and answers Yes/No
2. **Decision phase**: if all said Yes, send commit to every island; if even one said No, send abort

⚠️ Weakness: if the coordinator sinks right before the decision, the participating islands are **left waiting while holding locks** (blocking).
The modern remedy is to "replicate the coordinator itself with Raft" (e.g., Spanner).
— This is how the Heavens are built: by **stacking components**: log → consensus → replication → transactions.

---

## ⚔️ Quests

### Quest 1: The Parliament's Catechism (40 XP)

1. Why is the inference "it timed out, therefore the other side is dead" dangerous? Give one accident that occurs if it wasn't actually dead.
2. How many simultaneous failures can a 5-node Raft cluster tolerate while continuing to accept writes? What about 7 nodes? Why does going even (6 nodes) not increase fault tolerance?
3. Explain why eventual consistency is acceptable for a "like count" but dangerous for "inventory count."

<details>
<summary>📜 Answers</summary>

1. The other side may be alive and merely slow. Example: the old leader is still alive when a new leader rises, and the client writes to both (split-brain). Raft prevents this by rejecting the old leader's writes based on the term number.
2. 5 nodes → up to 2 (a majority of 3 remains). 7 nodes → up to 3. With 6 nodes the majority is 4, so the tolerable failures stay at 2 — no different from 5 (which is why clusters use odd numbers).
3. A slightly stale like count bothers no one and only needs to converge. For inventory, two people seeing a stale value at once leads to double-selling (oversell), a real harm — so strong consistency or dedicated inventory arbitration is required.
</details>

### Quest 2: 💻 Implementation Quest — "Mini MapReduce" (80 XP)

Simulate MapReduce on a single machine using **4 processes (or threads)**:
implement a word count over multiple text files via the flow map worker → intermediate files (partitioned by key) → reduce worker.
To finish, randomly "kill" one map worker and confirm that **re-running produces the correct result**.

> 🎓 For those who'll take on the real thing: MIT 6.824's [Lab 1 (MapReduce)](https://pdos.csail.mit.edu/6.824/) builds the same thing in Go,
> in a distributed version — one of the finest exercises in the world. Lab 2 has you implement Raft itself. That's where the Heavens' official exam is held.

### Quest 3: Raft Tabletop Simulation (40 XP)

Suppose 5 nodes (S1–S5), with S1 as leader (term 3), and the log committed through index 10.

1. S1 accepted index 11 and managed to replicate it to S2 and S3, then sank. Is index 11 committed?
2. In the subsequent election, S4 (log through index 10) and S2 (log through index 11) both ran. Which can win, and why, by the election-restriction rule?

<details>
<summary>📜 Answers</summary>

1. Since it was replicated to a majority (3/5: S1, S2, S3), the commit condition is met, but if the leader died before announcing the commit, the client cannot know "whether it was finalized as committed." What Raft's safety guarantees is that "only someone holding index 11 can become the next leader."
2. S2. Voters reject any "candidate whose log is older than their own." S4's log (through 10) is older than S2 and S3's logs (through 11), so it cannot win S2's and S3's votes and falls short of a majority. After winning, S2 can re-commit index 11.
</details>

---

## 👹 Boss Battle: Chairperson "Consensus Albion" (200 XP)

Close your notes and face it. Win with 70% or more.

1. State the CAP theorem precisely (where is the popular "pick 2 of 3" phrasing sloppy?).
2. What is the precondition under which MapReduce achieves fault tolerance through "re-running workers" alone?
3. Explain the difference between linearizability and eventual consistency, using examples of phenomena a client can observe.
4. How does Raft's leader election resolve vote splitting from simultaneous candidacies?
5. Explain how "overlapping majorities" underpins Raft's safety (the immortality of committed log entries).
6. What is the blocking problem of 2PC? How do modern systems mitigate it?
7. If you were to design a "global-scale chat service," which consistency model would you choose for message ordering, read status, and billing, respectively? State your reasons.

<details>
<summary>📜 Outline of answers</summary>

1. The precise claim is: **while** a partition (P) is occurring, C and A cannot both be satisfied. P is not an option but a reality (the network can always partition), so it really comes down to "which way to lean — C or A — during a partition." In normal times, both can be provided.
2. That map/reduce are deterministic and side-effect-free (idempotent), and that making output visible is atomic (e.g., rename only after completion).
3. Linearizable: immediately after I write, anyone who reads sees the new value. Eventual: even the writer reading right after may get a stale value (read-your-writes is broken), but once updates stop, everyone eventually agrees.
4. Randomize election timeouts to lower the probability of simultaneous candidacy. If votes split, advance the term and hold another election.
5. Commit = held by a majority. The next leader also needs a majority of votes. Any two majorities must overlap in at least one node, so by the rule that "voters only vote for a candidate with an at-least-as-new log," a candidate lacking a committed entry cannot win.
6. If the coordinator fails before the decision phase, participants cannot decide commit/abort on their own and wait while holding locks. Mitigations: replicate the coordinator with Raft/Paxos to remove the single point of failure, use timeout + arbitration protocols, and reduce reliance on 2PC by design (e.g., Sagas).
7. Example: message ordering = sequential consistency per conversation (everyone sees the same order; real-time ordering is unnecessary), read status = eventual (drift causes little harm), billing = linearizability + distributed transactions (money requires strong consistency). You pass if you can explain choosing models by cost and real-world harm.
</details>

---

🏆 **Victory reward**: Badge "☁️ Member of the Sky Parliament" + 200 XP

➡️ Next: [GRAD 2: The Sky Fortress of Security (Security and Cryptography)](grad-02-security-crypto.md)
