# Module 3 — CS Foundations & System Design (Weeks 8–10)

> Goal: the computer-science depth and architecture judgment that separates "can build a demo"
> from "can be trusted alone inside a Fortune 500." FDE loops at OpenAI include coding rounds
> and a system design round; Palantir's FDSE loop leans hard on decomposition and design.
> This module makes you dangerous in both — and gives every later module its vocabulary.

This is the *FDE-calibrated* dose: deep enough to pass lab interviews and reason about
production systems, without the 9-month grind of a research-track prep. If you want the full
deep-dive on any topic, the parent repo — [Coding Interview University](https://github.com/jwasham/coding-interview-university) — is the
canonical map; treat it as this module's optional expansion pack.

---

## Week 8 — Data structures & algorithms (the working set)

FDE coding rounds are *practical-leaning* but still assume fluency: you'll be asked to build
something real (a rate limiter, a log parser, a mini key-value store) and your data-structure
choices are the evaluation. LeetCode-hard dynamic programming is rare; clean, fast, correct
implementation under time pressure is universal.

### Core fluency (be able to implement and choose between, from memory)

- [ ] **Arrays, strings, hash maps/sets** — 80% of practical rounds live here. Know collision
      behavior, O(1) amortized caveats, and dictionary ordering guarantees in Python/JS.
- [ ] **Stacks, queues, deques** — parsing, undo, BFS frontiers, sliding windows.
- [ ] **Heaps / priority queues** — top-K, scheduling, merge-K-streams (you will literally use
      this for merging paginated API results).
- [ ] **Trees** — traversal (BFS/DFS, recursive & iterative), BSTs conceptually; tries for
      prefix problems.
- [ ] **Graphs** — adjacency list, BFS/DFS, topological sort (dependency resolution — appears
      constantly in data-pipeline work), shortest path (BFS/Dijkstra at a working level).
- [ ] **Sorting & searching** — built-in sort + custom keys; binary search and its
      off-by-one traps; when O(n log n) vs O(n) matters at real data sizes.
- [ ] **Complexity** — Big-O fluency for time *and* space, plus the practical sense layer:
      "n = 50k rows → anything O(n²) is dead; n = 200 → who cares."

### Practice protocol (3–4 problems/day, ~25 total this week, then maintenance)

- [ ] Curated list: [NeetCode 150](https://neetcode.io/) — do the Arrays/Hashing, Two Pointers,
      Stack, Binary Search, Trees, Graphs, Heap sections. Skip the exotic DP for now.
- [ ] **Practical drills** (closer to the real FDE round — do all of these, timed at 45 min):
      - Implement an in-memory key-value store with TTL expiry; then add transactions.
      - Implement a sliding-window rate limiter; then make it per-API-key.
      - Parse a 1GB log file (generate one) and compute p95 latency per endpoint —
        without loading it all into memory.
      - Implement an LRU cache (classic, and you'll genuinely deploy one someday).
      - Flatten a deeply nested JSON config into dotted keys, and unflatten it back.
      - Diff two CSV exports of the "same" table and emit inserts/updates/deletes (this is
        an actual recurring FDE task disguised as an interview problem).
- [ ] Practice **out loud**: narrate trade-offs as you code. FDE interviewers grade
      communication-while-coding heavily — it predicts customer-site behavior.

## Week 9 — How the machine actually works (OS, networking, concurrency)

You debug production systems in *other people's* environments. This layer is what makes you
fast when nothing works and no one knows why.

### Operating systems & Linux (the FDE survival kit)

- [ ] Processes vs threads; memory layout (stack/heap), virtual memory, what an OOM kill is
      and how to spot one (`dmesg`, exit code 137 — you will meet this in a customer's k8s pod).
- [ ] File descriptors, pipes, signals, exit codes; why "too many open files" happens.
- [ ] Linux fluency drill — on a cloud VM, without a GUI: find the process eating CPU
      (`top`/`htop`), inspect its open connections (`ss`/`lsof`), tail and filter its logs,
      check disk (`df`/`du`), inspect a container from the host (`docker exec/stats/logs`),
      read a systemd unit. Time-boxed scenario: a service is down — diagnose using only SSH.
- [ ] Read: [The Linux Command Line](https://linuxcommand.org/tlcl.php) (skim parts 1–3 as
      reference) or work through [OverTheWire Bandit](https://overthewire.org/wargames/bandit/)
      levels 1–20 (more fun, same skills).

### Networking (every enterprise problem is secretly a networking problem)

- [ ] The path of a request, cold: DNS → TCP handshake → TLS → HTTP. Be able to narrate it
      and debug each hop (`dig`, `curl -v`, `openssl s_client`).
- [ ] HTTP/1.1 vs HTTP/2; keep-alive; what a load balancer does (L4 vs L7); reverse proxies.
- [ ] Long-lived connections: WebSockets vs SSE vs polling — and why token streaming
      (Module 4+) almost always rides SSE.
- [ ] Enterprise network reality: proxies, egress firewalls, private DNS, VPNs, mTLS. Why
      "works on my laptop, 403 in the customer's VPC" happens — list five plausible causes.

### Concurrency (where LLM apps actually bottleneck)

- [ ] Threads vs processes vs async — and Python's GIL: what each is for. Rule of thumb you
      can defend: async for I/O-bound fan-out (API calls!), processes for CPU-bound, threads
      for blocking-I/O libraries.
- [ ] Build it: fetch 1,000 URLs (or make 1,000 mock LLM calls) sequentially, with a thread
      pool, and with `asyncio` + semaphore-bounded concurrency. Measure all three. Add retry +
      timeout + rate-limit handling to the async version — this exact harness reappears in
      Module 6's reliability work.
- [ ] Race conditions and locks at a working level; idempotency as the distributed-systems
      escape hatch (you met it in Module 2's pipelines; now name it).

## Week 10 — System design & architecture

The FDE system design round differs from the standard SWE one: less "design Twitter for 500M
users," more "design a real system for *this customer*, under *their* constraints, and defend
the trade-offs to a mixed technical/non-technical audience."

### The building blocks (know what each is for, its failure modes, one real product name)

- [ ] Load balancers; horizontal vs vertical scaling; stateless services (12-factor pays off).
- [ ] Caching layers (client, CDN, Redis, DB) — and invalidation strategies, honestly.
- [ ] **Queues & async workers** (SQS/RabbitMQ/Celery): the single most-used pattern in LLM
      systems — decouple "user clicked" from "model finished 40 seconds later."
- [ ] Database scaling: read replicas, connection pooling, sharding (and why you delay it);
      when to add a search index (Elasticsearch) or a warehouse (BigQuery/Snowflake).
- [ ] Replication & consistency: leader/follower, eventual consistency, CAP at a
      conversational level; exactly-once vs at-least-once delivery (and why "at-least-once +
      idempotent consumer" is the real-world answer).
- [ ] Batch vs streaming data processing; ETL/ELT; what Spark/Kafka are for (Palantir-flavored
      FDE loops expect this vocabulary).
- [ ] Architecture patterns & when each is right: modular monolith (default!), microservices,
      event-driven, serverless. Be ready to argue *against* microservices for a 5-person team.

### The method (drill until automatic)

1. Requirements — functional + scale + constraints (*ask before designing; FDE bonus: ask
   about the customer's existing stack and security posture*).
2. Napkin math — QPS, storage, bandwidth, cost. Practice: tokens/day → $/month is the
   FDE-specific twist; you did the spreadsheet in Module 4 — now do it on a whiteboard.
3. API & data model sketch.
4. High-level boxes-and-arrows; pick the boring technology by default.
5. Deep-dive where the interviewer steers; name failure modes *before* being asked.
6. Trade-offs stated explicitly; evolve the design when requirements change mid-interview
   (they will — it's a test of how you handle the customer changing scope).

### Practice designs (do ≥4 on a real whiteboard/paper, talking aloud; 35 min each)

- [ ] A document-Q&A system for 10M documents with per-user permissions (preview of
      Modules 5/7 — design it naively now, redesign it after Module 7 and diff yourself).
- [ ] An LLM-powered email-triage system for a bank: 1M emails/day, audit requirements,
      4-second p95. Where do queues go? Where do humans go?
- [ ] A nightly pipeline syncing a customer's Salesforce + Postgres + S3 CSVs into one
      warehouse with data-quality checks.
- [ ] A chat application backend with streaming, conversation history, and 50k concurrent
      users (yes, this is "design ChatGPT-lite" — labs ask their own products).
- [ ] Webhook ingestion at 10k events/sec with bursty traffic and a flaky downstream.

**Study**
- [ ] [System Design Primer](https://github.com/donnemartin/system-design-primer) — work
      through it; it's the standard reference.
- [ ] *Designing Data-Intensive Applications* — finish ch. 5–9 started in Module 2 (skim is
      fine; you want the vocabulary and failure modes, not exam recall).
- [ ] Watch 3–4 mock system-design interviews (Exponent / Hello Interview on YouTube) and
      score the candidates with the method above before reading the comments.

---

## Module 3 deliverable

`writeups/design-dossier.md` — your four practice designs, each: one diagram (Mermaid or a
photo of the whiteboard), the napkin math, three trade-offs you made and what you gave up.
Plus a `practical-drills/` repo with the six timed implementation drills, tests included.

## Module 3 exit criteria

- [ ] NeetCode core sections done; the six practical drills pass their tests within time-box.
- [ ] You can diagnose a dead service over SSH in under 15 minutes (have a friend break one).
- [ ] You can do the email-triage design cold, out loud, in 35 minutes — record it and
      check: did you ask requirements first, do napkin math, and name failure modes unprompted?

*Next → [Module 4: LLM Fundamentals & Prompt Engineering](04-llm-fundamentals.md)*
