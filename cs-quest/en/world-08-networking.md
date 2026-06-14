# 📡 World 8: The Sky City of Communication — Networking

> When you ride the underground city's elevator all the way up, a city floats above the clouds.
> Countless carrier pigeons (packets) crisscross the sky, carrying letters to cities around the world.
> The pigeons get lost, the letters get soaked and torn, and they even arrive out of order.
> So why does the world's communication hold together at all? —— that magic goes by the name of **protocol**.

**What you'll learn in this chapter (a university course would call it "Intro to Computer Networks")**
- Protocols and layered models
- The division of labor among IP, TCP, and UDP
- DNS, HTTP/HTTPS
- The full story of "from typing a URL to the page appearing"

---

## 📖 Lecture 1: The Sky City's Postal System — The Layered Model (10 XP)

A network is built from stacked **layers**. Each layer does only its own job and
doesn't need to know the details of the layer below —— the very same idea as "abstraction" in software design.

| Layer (TCP/IP model) | Job | Representative protocols | Analogy |
|---|---|---|---|
| Application layer | the format of the letter's contents | HTTP, DNS, SMTP | the wording and language of the letter |
| Transport layer | reliably deliver to the destination **app** | TCP, UDP | registered or ordinary mail |
| Internet layer | choose a route from city to city | IP | the post office's routing network |
| Link layer | carry to the next relay point over | Ethernet, Wi-Fi | the trucks and delivery workers |

When sending, each layer from top to bottom wraps the data with a header (encapsulation); the receiving side peels them off from bottom to top.

## 📖 Lecture 2: The Carrier Pigeons' Code — IP, UDP, and TCP (10 XP)

### IP — "No guarantee it arrives. But I'll do my best."

It assigns each machine an **IP address** and forwards packets to their destination on a **best-effort** basis.
If they vanish along the way, arrive out of order, or get duplicated — IP plays dumb. That's the IP way.

### UDP — "Just throw it, fast."

A thin protocol that merely adds a port number (which app it's for) to IP.
No guarantees, no connection, blazing fast. For uses like **games, calls, video streaming, and DNS** where "a little loss is fine, but latency is the enemy."

### TCP — "All of it, in order, for certain."

The greatest magic of this world: **building reliability** on top of unreliable IP.

- Establish a connection with a **3-way handshake**: `SYN →` `← SYN+ACK` `ACK →` (both sides sync their numbers)
- Reorder using **sequence numbers**, and **retransmit** if no **ACK (acknowledgment)** comes back
- **Flow control**: adjust how much is sent to match the receiver's processing capacity
- **Congestion control**: sense network congestion and slow the sending pace (don't pour cars onto a jammed highway)

| | TCP | UDP |
|---|---|---|
| Delivery & order guarantee | ✓ | ✗ |
| Connection setup | required (handshake) | not needed |
| Speed / overhead | heavier | light |
| Uses | Web, email, file transfer | games, calls, DNS |

## 📖 Lecture 3: The Magic of Names — DNS (10 XP)

Humans remember `example.com`, while machines communicate by IP address. **DNS** is the distributed database that looks up that mapping.

```
browser → OS cache → resolver (ISP, etc.)
            ↓ if not found, walk the hierarchy
       root server → .com server → example.com's authoritative server → the IP address!
```

- A tree-structured **distributed** system (no single place knows the whole world)
- Each level has a **cache** (with a TTL), so most queries are answered instantly partway along
- Here's a real-world example of World 3's tree structures and World 7's caching at work

## 📖 Lecture 4: The Format of Letters — HTTP and HTTPS (10 XP)

**HTTP** is the format of the Web's letters. A simple round trip of request and response.

```
GET /index.html HTTP/1.1          HTTP/1.1 200 OK
Host: example.com         →      Content-Type: text/html
                          ←
                                  <html>...
```

- **Methods**: GET (retrieve), POST (send), PUT (update), DELETE (delete)
- **Status codes**: 200 (success), 301 (moved), 404 (not found), 500 (internal server error)
- HTTP is **stateless** (each letter is independent). State is held in cookies or tokens.

**HTTPS** = HTTP + **TLS**. It encrypts the communication and confirms whether the other party is genuine via a **certificate**.
Keys are exchanged using public-key cryptography, and from then on the conversation uses fast symmetric-key cryptography (the cryptographic details are in the hidden dungeons).

📺 Recommended: the original [Networking section](https://github.com/jwasham/coding-interview-university#networking) — the Computerphile / Khan Academy video collections

---

## ⚔️ Quests

### Quest 1: Choosing Your Pigeon (20 XP)

Which should you use, TCP or UDP, and why?

1. Syncing position data in an online competitive game (sent 60 times per second)
2. A bank's money-transfer API
3. A live video stream
4. A file download

<details>
<summary>📜 Answer</summary>

1. **UDP** — there's no point retransmitting stale position data. Latency is the top priority.
2. **TCP** — not a single byte may be lost.
3. **UDP** (family) — low latency matters more than a momentary dropout (in practice this uses QUIC, RTP, etc.).
4. **TCP** — completeness is essential.
</details>

### Quest 2: 🔬 Observation Quest "See the Pigeons with Your Own Eyes" (30 XP)

Get hands-on and observe (in a macOS / Linux terminal):

1. Watch the DNS answer and TTL with `dig example.com` (or `nslookup`)
2. With `curl -v https://example.com`, read the HTTP request/response headers and the TLS handshake log
3. With `traceroute example.com`, take in the journey of routers a packet passes through

In each output, point to and confirm one concept that appeared in the lectures (TTL, status code, route).

### Quest 3: The Classic Catechism "What Happens After You Type a URL?" (30 XP)

Explain what happens from typing `https://example.com` and pressing Enter until the page is displayed,
**in order, touching as many layers as you can** (this is an extremely common real interview question).

<details>
<summary>📜 The skeleton of a model answer</summary>

1. The browser parses the URL (scheme https, host example.com, port 443).
2. **DNS resolution**: check the cache → resolver → root / .com / authoritative server, in that order, to get the IP.
3. **TCP connection**: the 3-way handshake (SYN / SYN+ACK / ACK).
4. **TLS handshake**: establish an encrypted path via certificate verification and key exchange.
5. **Send the HTTP request**: `GET / HTTP/1.1` (from here, IP routes each packet and TCP guarantees order and retransmission).
6. The server returns an **HTTP response** (200 OK + HTML).
7. The browser parses the HTML, fetching the referenced CSS/JS/images in parallel while it renders.
</details>

---

## 👹 Boss Battle: The Sky City's Gatekeeper, "Protocol Gryphon" (100 XP)

Close your notes and face it. Score 70% or more to win.

1. Explain the benefit of designing a network with a layered model, in the language of software design.
2. State the three packets of TCP's 3-way handshake and the role of each.
3. List 3 mechanisms by which TCP makes the unreliable communication of plain IP reliable.
4. What are the 2 design reasons DNS queries can be handled quickly across the whole world?
5. What does it mean for HTTP to be stateless? How is login state achieved?
6. Name 2 things HTTPS protects and 1 thing it does not.

<details>
<summary>📜 Answers</summary>

1. An abstraction where each layer is connected only through interfaces (separation of concerns). You can swap a lower layer's implementation (Wi-Fi or wired) without changing the upper layers.
2. SYN (connection request + your own initial sequence number), SYN+ACK (acceptance + acknowledging the peer's number + your own number), ACK (acknowledgment). Once both sides' numbers are synced, the connection is established.
3. Restoring order via sequence numbers, retransmission via ACKs and timeouts, and corruption detection via checksums (+ flow control and congestion control).
4. A hierarchical distributed structure (load doesn't concentrate at the root) and the TTL-based caches at each level.
5. Each request is independent, and the server doesn't remember the previous request. Cookies (a session ID) or tokens are placed on the request to pseudo-maintain state.
6. Protects: the confidentiality of the communication's contents (encryption), the authenticity of the other party (certificate) and tamper detection. Doesn't protect: e.g., the domain name you're accessing, the volume of traffic, and the timing can be observed (or the case where the server itself is malicious).
</details>

---

🏆 **Victory Reward**: badge "📨 Traveler of Packets" + 100 XP

➡️ At last, the final battle: [FINAL: The Demon Lord's Castle](final-boss.md)
