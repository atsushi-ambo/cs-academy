# 📗 Appendix II: The Complete System Design Problem Bank — Fully Explained, Down to the Design Decisions

> This is "The Design Workshop of the Sky Castle." Having learned the building blocks in GRAD 1 (Distributed Systems),
> this is where you **design an entire real-world service from scratch**.
> System design interviews have no "single correct answer" — what's being tested is **whether you can articulate the trade-offs**.
> For each problem, we walk through **the entire thought process**: from requirements gathering to estimation, design, and bottleneck mitigation.

## 📖 The "Template" for System Design (the procedure used in every problem)

Following this order works well in real design interviews too. **Don't start by drawing diagrams.**

1. **Clarify the requirements (functional & non-functional)**
   - Functional: what should it be able to do (post, search, …)?
   - Non-functional: what are the demands on scale, latency, availability, and consistency?
2. **Estimate the scale (back-of-the-envelope calculation)**
   - Daily active users, QPS (requests per second), storage, bandwidth
3. **Design the API** (endpoints and arguments)
4. **Design the data model** (tables/schema, and which DB to choose)
5. **Sketch the overall architecture** (client → LB → app → cache → DB)
6. **Eliminate the bottlenecks** (scaling, caching, sharding, replication)
7. **State the trade-offs explicitly** (which side of CAP you chose, and why)

### Memorized numbers for estimation (just learn these)

| Quantity | Rough value |
|---|---|
| Seconds in a day | About 86,400 ≈ 100K |
| Memory reference | About 100 nanoseconds |
| SSD random read | About 100 microseconds |
| Disk seek | About 10 milliseconds |
| Round trip within the same data center | About 0.5 milliseconds |
| Intercontinental round trip | About 100 milliseconds |
| One character (UTF-8 alphanumeric) | 1 byte |

**QPS estimation formula**: `requests per day ÷ 86,400`. Expect peaks to be 2–3× the average.

---

## Problem 1: URL Shortening Service (TinyURL) 🟢

Design a service that "turns a long URL into a short URL, and when accessed, redirects to the original."

### Step 1: Requirements

- **Functional**: ① generate a short URL from a long URL, ② redirect from the short URL to the original URL, ③ (optional) expiration, custom aliases, statistics
- **Non-functional**: reads (redirects) vastly dominate. **Reads >> writes.** Low latency is a must. Short URLs must never collide.

### Step 2: Estimation

- 100 million URLs written/month ≈ 40 URLs/sec; if reads are 100× that, then 4,000 QPS
- 1 record ≈ 500 bytes × 100M × 12 months × 5 years ≈ 3 TB. Easily fits in a DB.
- **Implication**: since it's read-heavy, caching is effective. The core challenge is maintaining uniqueness with a short key.

### Step 3: API

```
POST /shorten        body: { long_url }            -> { short_url }
GET  /{short_code}                                  -> 301 redirect
```

### Step 4: Data Model

```
url_mapping
  short_code  VARCHAR(7)  PRIMARY KEY   -- e.g., "aZ3xK9p"
  long_url    TEXT
  created_at  TIMESTAMP
  expires_at  TIMESTAMP NULL
```

**How to make the short code (the heart of the design)**:
- **Approach A: hash + truncate** — MD5 the long_url and take the leading portion as Base62 (the 62 characters a–z A–Z 0–9) to make 7 characters. Re-generate on collision. Pro: simple. Con: requires collision handling.
- **Approach B: sequential number + Base62 conversion** — encode a global counter (sequential number) in Base62. With `62^7 ≈ 3.5 trillion` combinations, it won't run out. No collisions. Con: sequential numbers are predictable (for security, randomize them or distribute ranges via a distributed ID generator).
- **Chosen**: Approach B (no collision handling needed, and reliable). Issuing the sequential numbers is delegated to a numbering service (the ID generation discussed later).

### Step 5: Overall Architecture

```
client → load balancer → app server → cache (Redis) → DB
                                           ↘ on miss, query the DB and load it into the cache
```

A redirect works as: "look up the cache by short_code → if present, return immediately → if absent, hit the DB → load it into the cache." Over 90% of reads complete from the cache.

### Step 6: Bottlenecks and Mitigations

- **Read concentration**: Redis cache + CDN. Popular URLs have a high cache hit rate (the locality of World 7).
- **Scaling the DB**: shard by short_code (by range or hash). At 3 TB, a single instance is fine for now.
- **Single point of failure in numbering**: make the ID generator redundant (the Snowflake approach discussed later).

### Step 7: Trade-offs

- If the redirect is **301 (permanent)**, browsers cache it and you can't collect statistics. If you want statistics, use **302 (temporary)**. Leaning toward availability means an **AP-leaning** design (short URLs being slightly stale isn't fatal).

**One line for the interview**: "Since it's read-heavy, caching is the main player. For unique keys, Base62 conversion of sequential numbers structurally eliminates collisions."

---

## Problem 2: Rate Limiter (API Throughput Limiting) 🟡

Design a mechanism that enforces "up to 100 requests per minute per user."

### Requirements and Estimation

- For a given identifier (user ID / IP / API key), limit the number of times per unit of time
- Must be **extremely fast** (it sits in front of every API, so latency is critical) and must work **consistently in a distributed environment**

### Algorithm Options (this is the heart of the design)

| Approach | How it works | Characteristics |
|---|---|---|
| Fixed window counter | Increment a counter "per minute" | Simple, but the boundary problem lets 2× through at window edges |
| Sliding log | Record each request's timestamp and count how many fall within the window | Accurate, but memory-hungry |
| **Sliding window counter** | Weighted average of the current and previous window counts | Good balance of accuracy and cost |
| **Token bucket** | Refill tokens at a fixed rate; 1 request = consume 1 token | Tolerates bursts (momentary concentration). The most popular in practice |

**Chosen: token bucket.** "Bucket capacity = allowed burst" and "refill rate = the normal limit" can be configured separately, matching real-world needs.

```python
# Conceptual implementation (in practice, done atomically on Redis)
import time

class TokenBucket:
    def __init__(self, capacity, refill_per_sec):
        self.capacity = capacity            # maximum number of tokens in the bucket
        self.refill = refill_per_sec        # number refilled per second
        self.tokens = capacity
        self.last = time.time()

    def allow(self):
        now = time.time()
        # refill tokens for the elapsed time (up to the cap)
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.refill)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True                     # allow
        return False                        # limit (return 429)
```

### Implementation in a Distributed Environment

- The state (remaining tokens) is kept in **Redis** and shared across all app servers
- To prevent races, execute "read → compute → write" atomically with a **Lua script** (the concurrency control of World 11, the critical-section practice of World 10)
- When the limit is exceeded, return **HTTP 429 Too Many Requests**

### Trade-offs

- The latency of a Redis round trip vs. local approximation on each server (local is faster but less precise). For strictness, use centralized management; for speed, use local + periodic synchronization.

---

## Problem 3: News Feed (Twitter/Instagram style) 🔴

Design a "feed where posts from the people you follow are arranged chronologically." The classic hardest problem.

### Requirements and Estimation

- **Functional**: post, follow, view your own feed
- **Scale**: 200M DAU, average 200 follows per person, reads:writes = 100:1, **read-heavy**
- **The core difficulty**: feed generation means "merge the posts of **everyone** you follow and sort chronologically." Doing this every single time is expensive.

### The Two Major Schools of Design (this is where it's won or lost)

**① Pull model (generate at read time / fan-out on read)**
- Every time the feed is viewed, fetch and merge the latest posts of everyone followed
- Pro: writes are light, storage is saved. Con: **reads are heavy** (slow when following many people)

**② Push model (distribute at write time / fan-out on write)**
- When someone posts, immediately **write it into all of their followers' feeds (caches)**
- Pro: reads are blazing fast (you just read your own feed). Con: **writes are heavy**, the celebrity problem

**③ Hybrid (the solution used by actual Twitter etc.)**
- Regular users: push model (few followers, so distribution is light)
- **Celebrities (millions of followers): pull model** (distributing to everyone would explode the writes, so merge at read time)
- When displaying the feed, merge "what was delivered via push" + "the latest from celebrities you follow"

**This is the standard solution to the "celebrity problem."** A textbook example of selectively applying trade-offs.

### Data Model and Architecture

```
posts(post_id, user_id, content, created_at)
follows(follower_id, followee_id)
feed_cache: a per-user list in Redis (holds post IDs in chronological order)
```

```
post → app → ① save to posts
              ② fan-out service pushes to followers' feed_cache (regular users)
read → app → read feed_cache + pull the latest from celebrities you follow → merge → fetch the post bodies
```

### Bottlenecks and Mitigations

- **Fan-out load**: distribute in the background via an asynchronous queue (the messaging of World 8). Return the post's response immediately.
- **Storage**: feed_cache holds only post IDs (bodies are fetched later from posts). Old posts are deleted on expiration.
- **Hot posts**: multi-layered CDN and caching

### Trade-offs

- For consistency, **eventual consistency is sufficient** (no one is harmed if a post shows up in the feed a few seconds late — the consistency-model choice of GRAD 1). An **AP design** that prioritizes availability and throughput.

**One line for the interview**: "The standard approach is a hybrid: push for regular users to keep reads fast, and pull for celebrities to avoid a write explosion. For consistency, we settle for eventual consistency."

---

## Problem 4: Chat System (LINE/Slack style) 🔴

Design "real-time chat for both 1-on-1 and groups."

### Requirements and Core

- **Functional**: sending/receiving messages, online status, read receipts, history
- **Core**: the server needs to **push to clients in real time** (HTTP is inherently client-initiated)

### Options for Real-Time Delivery

| Approach | How it works | Assessment |
|---|---|---|
| Polling | Periodically ask "anything new?" | Simple but wasteful, with high latency |
| Long polling | The server holds the response until something new appears | An improved version |
| **WebSocket** | Establish a persistent bidirectional connection | The standard for chat. Low latency |

**Chosen: WebSocket.** The client maintains a persistent connection to a connection server.

### Architecture

```
client ⇄ WebSocket ⇄ connection server (tracks which user is on which server)
                          ↓ message queue
                      message storage (DB) + forward to the recipient's connection server
```

- **Connection management**: share the "user ID → connected server" mapping in something like Redis. No matter which server the recipient is on, you can deliver to them.
- **Message storage**: writes are frequent and reads are chronological → **NoSQL (e.g., Cassandra, strong at write scaling)** is a good fit. Order by `(chat_id, timestamp)`.
- **Offline**: if the recipient is not connected, queue the message and deliver on reconnect. Also use push notifications in tandem.

### Data Model

```
messages(chat_id, message_id, sender_id, content, created_at)  -- partition by chat_id
chat_members(chat_id, user_id)
```

### Trade-offs

- For message ordering, **per-chat ordering guarantees** are required (you don't need global real-time ordering — GRAD 1). Assign sequence numbers per `chat_id`.
- Read-receipt and delivery status can be eventually consistent.

---

## Problem 5: Distributed Unique ID Generator (Snowflake) 🟡

Design a mechanism that generates "collision-free, roughly chronologically ordered 64-bit IDs in a distributed environment." This is the foundation needed as a building block in all of Problems 1–4.

### Why is it hard?

- A single DB's sequential numbering is a **single point of failure** and a bottleneck
- UUIDs (random) don't collide, but they're **large at 128 bits and not chronologically ordered** (poor DB index locality — World 11)

### Solution: The Twitter Snowflake Approach

Divide 64 bits into meaningful sections:

```
| 1 bit unused | 41 bit timestamp (milliseconds) | 10 bit machine ID | 12 bit sequence |
```

- The **timestamp** is in the high bits → IDs are **roughly chronologically ordered** (kind to DB indexes)
- The **machine ID** lets each server issue independently → no central coordination, no collisions
- The **sequence** handles multiple issuances within the same millisecond (up to 4096 per millisecond)

```python
class Snowflake:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.seq = 0
        self.last_ts = -1

    def next_id(self, now_ms):
        if now_ms == self.last_ts:
            self.seq = (self.seq + 1) & 0xFFF   # wrap at 12 bits
            if self.seq == 0:
                now_ms = self._wait_next_ms(now_ms)  # if exhausted, wait for the next millisecond
        else:
            self.seq = 0
        self.last_ts = now_ms
        return (now_ms << 22) | (self.machine_id << 12) | self.seq
```

### Trade-offs

- Beware of clock rollback (NTP sync moving the server time backward). If a rollback is detected, you need countermeasures such as temporarily pausing issuance — **in distributed systems, you can't even fully trust "time"** (the lesson of GRAD 1).

---

## 🏆 Tips for Clearing the Design Workshop

There's no silver bullet in system design. But the **order of thinking** and the **standard trade-offs** are fixed:

| Situation | Standard decision |
|---|---|
| Reads vastly dominate | Make cache (Redis) + CDN the main players |
| Writes are heavy / scale is required | NoSQL, sharding, asynchronous queues |
| Real-time push is required | WebSocket |
| Feed/distribution with celebrities | Push/pull hybrid |
| A unique key is required | Base62 of sequential numbers / Snowflake |
| Strict consistency is required (money) | Strong consistency, distributed transactions (CP) |
| Slightly stale is OK (likes, feeds) | Eventual consistency (AP) |
| Want to enforce throughput across all APIs | Token bucket + Redis |

**The most important mindset**: the interviewer isn't asking for "the correct answer." They're watching **whether you can explain "why you made that choice, and what you sacrificed."** Always say your reasoning out loud: "Since this is read-heavy…", "Here I chose availability over consistency…".

➡️ Next, down to the lowest layer of the machine: [Appendix III: The Complete Computer Architecture Problem Bank](appendix-03-architecture-problems.md)
