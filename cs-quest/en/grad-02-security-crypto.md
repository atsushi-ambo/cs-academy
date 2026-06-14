# 🛡️ GRAD 2: The Sky Fortress of Security — Security and Cryptographic Theory

> An impregnable fortress floating in the Heavens.
> The castle lord says: "What you learn here is not attack itself.
> It is **to think with an attacker's mind and wield the defender's mathematics**.
> A system built by one who doesn't know how to lock a door is more perilous than a safe with no door at all."
>
> ⚠️ The knowledge of this fortress exists **to defend, and for authorized testing**.
> The techniques you learn may be used only on your own castle, or on a castle for which you have permission. That is the knight's code.

**Corresponding graduate course**: MIT **6.858 Computer Systems Security** / Stanford **CS255 Cryptography** / upstream [Cryptography](https://github.com/jwasham/coding-interview-university#cryptography) [Computer Security](https://github.com/jwasham/coding-interview-university#computer-security)
**Prerequisites**: World 9 (Number theory), World 8 (Networking), World 10/11 (Systems and transactions)

**What you'll learn in this chapter**
- Threat models and security principles
- Symmetric-key and public-key cryptography (building RSA from number theory)
- Hashing, signatures, and authentication
- Key exchange and protocols (the inside of TLS)
- System attacks and defenses (injection, memory corruption, the Web)

---

## 📖 Lecture 1: The Design Philosophy of the Fortress — Threat Models and Principles (20 XP)

Security is not the craft of building "absolute safety." It is the engineering of defining **"from whom, what, and to what extent you protect" (the threat model)**
and making attacks not worth the cost.

The iron rules of the fortress:
- **Defense in depth**: never rely on a single wall
- **Least privilege**: grant each component only the minimum authority it needs
- **Fail secure**: when something breaks, it should fail toward "closed"
- **Kerckhoffs's principle**: **the algorithm may be public; keep only the key secret** (security by obscurity is fragile)
- "Don't roll your own crypto": use battle-tested standard libraries. Homemade ciphers are always broken

The three pillars security protects — **CIA**: Confidentiality, Integrity, Availability.

## 📖 Lecture 2: Guarding with the Same Key — Symmetric-Key Cryptography (20 XP)

Sender and receiver encrypt and decrypt with **the same secret key** (the world of World 9's modular arithmetic).

- **AES**: the modern standard block cipher. It scrambles a 128-bit block with the key in many rounds
- **The mode of operation is vitally important**: **don't use ECB** (identical plaintext blocks become identical ciphertext, the famous failure where the picture shows through).
  Use CBC, CTR, or authenticated **GCM**
- Fast. But the fundamental problem remains: **"how do you deliver the key to the other party?"** → on to Lecture 3

## 📖 Lecture 3: The Magic of Two Keys — Public-Key Cryptography and RSA (20 XP)

**Lock with the public key, unlock with the private key.** The public key may be distributed to the world. This solves the key distribution problem.

### Building RSA from number theory (you can build it with World 9's tools alone!)

1. Choose large primes p, q; set n = pq, φ(n) = (p−1)(q−1)
2. Choose e (public), and compute d ≡ e⁻¹ (mod φ(n)) with the **extended Euclidean algorithm** (secret)
3. Encrypt c = mᵉ mod n; decrypt m = cᵈ mod n (fast via **repeated squaring**)

**Basis of security**: it is **hard to factor** n into p, q (no efficient classical algorithm has been found).
In World 13's terms, "factoring is not known to be in P."
⚠️ But **a quantum computer's Shor's algorithm factors in polynomial time** → a migration to post-quantum cryptography (lattice-based) is underway.

In practice RSA is slow, so the standard is the hybrid "use the public key to **exchange a shared key**, then encrypt the body with AES" (the true identity of World 8's HTTPS).

## 📖 Lecture 4: Fingerprints and Wax Seals — Hashing, Signatures, and Authentication (20 XP)

- **Cryptographic hashes (SHA-256, etc.)**: one-way (preimage resistance), collision resistance.
  ⚠️ By World 9's birthday attack, a collision can be found at 2^(n/2) → which is why the output needs to be 256 bits
- **Password storage**: not encryption but a **salted hash** (a deliberately **slow** function like bcrypt/argon2).
  The salt invalidates rainbow tables, and the slowness makes brute force expensive
- **MAC / HMAC**: with a shared key, guarantees "this hasn't been tampered with" (integrity + authentication)
- **Digital signatures**: sign with the private key, verify with the public key. Makes "the person really wrote it, and it wasn't tampered with" publicly verifiable.
  But "is that public key really theirs?" → **certificates (CA) and the chain of trust** (World 8's HTTPS certificates)

## 📖 Lecture 5: The Rite of Exchanging Keys, and the Cracks in Systems (20 XP)

### Diffie–Hellman key exchange
The magic of creating a shared secret right in front of an eavesdropper. It rests on the hardness of the discrete logarithm.
**Forward secrecy**: if you create a throwaway key for each session, then even if the long-term key leaks later, past communications stay protected.

### Representative system attacks (known in order to defend)

| Attack | Mechanism | Defense |
|---|---|---|
| **SQL injection** | Concatenating input into a SQL statement and hijacking the syntax | **Prepared statements** (separate data from code) |
| **XSS** | Running a malicious script in someone else's browser | Output escaping, CSP |
| **Buffer overflow** | Writing past array bounds and hijacking the return address (the stack frame of World 7/12) | Bounds checking, ASLR, stack canaries, memory-safe languages (Rust) |
| **CSRF** | A forged request exploiting the victim's logged-in state | Tokens, SameSite cookies |

**The common lesson**: most attacks are born where "**the boundary between data and code is blurry**."
Don't trust input (as World 13 shows, a "perfect input validator" cannot be built, so separate them structurally).

---

## ⚔️ Quests

### Quest 1: A Knight's Creed (40 XP)

1. What is dangerous about the sales pitch "our cipher is proprietary, so it's unbreakable" (Kerckhoffs)?
2. Why are passwords stored "hashed" rather than "encrypted"? What is the role of the salt?
3. Explain why encrypting an image in ECB mode lets the original picture show through.

<details>
<summary>📜 Answers</summary>

1. It makes security depend on keeping the algorithm secret. Algorithms always leak (decompilation, departing employees, analysis), and the moment it leaks, everything collapses. Security should depend on the key alone, and the algorithm should be one that has survived public scrutiny.
2. Encryption can be reversed with the decryption key, so if the key leaks, every password is exposed. A hash is one-way; not even the server needs to know the original password. A salt adds a different value per user so that even identical passwords produce different hashes, invalidating precomputation (rainbow tables) and bulk attacks.
3. ECB always maps an identical plaintext block to an identical ciphertext block, so regions of uniform color in the image remain as patterns in the ciphertext.
</details>

### Quest 2: 💻 Implementation Quest — "Build Textbook RSA" (80 XP)

Using World 9's extended Euclidean algorithm and repeated squaring, implement RSA from scratch with **small primes**
(key generation → encryption → decryption → confirm it round-trips back).
When done, **be sure to write in a comment**: "This is for learning. In production, textbook RSA is not secure
(padding OAEP, randomness, and side-channel defenses are required). In production, use a standard library."

### Quest 3: 💻 Attack-and-Defense Quest — "Plug the Injection" (60 XP)

Prepare vulnerable code that builds SQL via string concatenation (`"SELECT * FROM users WHERE name='" + input + "'"`),
and reproduce, on **your own local DB (World 11's SQLite)**, how `' OR '1'='1` leaks every row.
Then fix it to use a prepared statement and confirm the same input is neutralized.
(⚠️ Your own environment only. Attempting it on others' systems is forbidden.)

### Quest 4: The Eye for Protocols (40 XP)

1. In Diffie–Hellman, why can't an eavesdropper who sees all the communication compute the shared key (name the hardness)?
2. With forward secrecy, why are past communications protected even if the server's long-term private key leaks in the future?
3. State one difference between a digital signature and a MAC (who can verify it).

<details>
<summary>📜 Answers</summary>

1. To derive the shared key g^(ab) from the exchanged g, gᵃ, gᵇ, you would need to solve the discrete logarithm, for which no efficient classical algorithm is known (the hardness of the discrete logarithm problem).
2. Because a throwaway ephemeral key per session is used to create the actual encryption key, and it is discarded after the session. The long-term key is used only to authenticate the ephemeral keys and provides no material to recover past session keys.
3. A MAC can be verified only by someone holding the shared key, and the verifier can also forge it (sender and receiver are symmetric). A signature can be created only by the signer holding the private key, and **anyone** holding the public key can verify it (providing non-repudiation).
</details>

---

## 👹 Boss Battle: The Castle Lord "Cipher Guardian" (200 XP)

Close your notes and face it. Win with 70% or more.

1. State Kerckhoffs's principle, and the problem with "security by obscurity," which violates it.
2. Explain how public-key cryptography solves the key distribution problem of symmetric-key cryptography.
3. Name the mathematical hardness RSA's security depends on, and the future technology that threatens it.
4. State the three properties required of a cryptographic hash, and explain the requirement the birthday attack places on output length.
5. Explain the correct way to store passwords using the three words "hash, salt, slow function."
6. State in one sentence the root cause common to SQL injection and buffer overflow, and give the defense for each.
7. Explain how "encryption, authentication, key exchange, and integrity" combine when establishing an HTTPS connection, integrating it with your World 8 knowledge.

<details>
<summary>📜 Outline of answers</summary>

1. The principle that security should depend on the key alone. Relying on keeping the algorithm secret leads to total collapse upon the leak that always comes, and forfeits the chance to find weaknesses through public scrutiny.
2. Either encrypt a shared key (session key) with the public key and send it, or share a key via DH — thereby establishing a symmetric key securely without pre-sharing a secret.
3. The hardness of factoring large composite numbers. Because a quantum computer's Shor's algorithm solves it in polynomial time, a migration to post-quantum (lattice-based) cryptography is required.
4. Preimage resistance, second-preimage resistance, and collision resistance. Because a birthday attack finds a collision at about 2^(n/2), 128-bit security requires a 256-bit output.
5. Concatenate a user-specific salt to the password and apply a deliberately slow hash function such as bcrypt/argon2 many times before storing. The salt prevents bulk and precomputation attacks, and the slowness raises the cost of brute force.
6. Common cause: the boundary between data and code (instructions) is blurry, so input gets interpreted as control flow or syntax. Defenses: for SQL, prepared statements (separating data/code); for memory corruption, bounds checking, ASLR, canaries, and memory-safe languages.
7. Resolve the IP via DNS → establish a TCP connection → in the TLS handshake, **authenticate the server** via the certificate, perform **key exchange** with (EC)DHE (forward secrecy), and use the established shared key to **encrypt and ensure integrity** of the body with AES-GCM. Subsequent HTTP flows over this encrypted channel.
</details>

---

🏆 **Victory reward**: Badge "🛡️ Guardian Knight of the Fortress" + 200 XP

➡️ Next: [GRAD 3: The Observatory of Intelligence (Machine Learning)](grad-03-machine-learning.md)
