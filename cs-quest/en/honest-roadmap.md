# 🧭 The Honest Roadmap — How Far This Course Really Takes You

> Adventurer, as your elder, let me speak honestly.
> The game cheers you on with "Clear it all and become a Grand Sage!" That's stagecraft for morale.
> But if you truly want to grow strong, you must look squarely at **what this course gives you and what it does not.**
> Only those who can doubt the map can go beyond it.

## 🎯 The Conclusion First

**Once you've cleared all of CS Quest, here's where you'll be:**
- ✅ The skills to pass major companies' technical interviews (coding + system design)
- ✅ A grasp of **the map and the core** of the main subjects in a university CS department
- ✅ The vantage point to imagine "what lies beneath" even when you meet a new technology
- ✅ The foundation to read through papers, textbooks, and official documentation on your own

**What CS Quest alone still doesn't give you:**
- ⚠️ The experience of **research, paper writing, and peer review** needed for a graduate degree (this fundamentally can't be filled by self-study materials)
- ⚠️ The experience of a **large-scale implementation project** (the muscle to design and maintain tens of thousands of lines of code)
- ⚠️ The **mathematical depth** of some subjects (linear algebra, probability and statistics, analysis at the level of specialized texts)
- ⚠️ The **sheer volume of hands-on work** (you only gain it by actually doing all of this course's "implementation quests")

In other words, CS Quest is **"an excellent map + lecture notes + a problem set"** — it is **not "the experience of having walked the road itself."**
Merely gazing at a map doesn't mean you've traveled. **Only when you write every implementation quest in code and solve every problem in the set does knowledge become power.**

## 📊 Mapping to a University Curriculum (How Much Is Covered)

| Area | CS Quest's Coverage | What to Supplement |
|---|---|---|
| Data structures & algorithms | 🟢 90% — plenty for interview level | Build up repetition with competitive programming |
| Computer systems & OS | 🟢 80% — the core is covered | Actually write a small OS/shell (the xv6 labs of MIT 6.S081) |
| Databases | 🟡 70% | Write a lot of real SQL; implement transactions |
| Networking | 🟡 70% | Packet capture, socket programming |
| Compilers | 🟡 65% | Go beyond a calculator language and build one typed language |
| Theory of computation | 🟢 80% — concepts are comprehensive | Write proofs by hand from Sipser's textbook |
| Distributed systems | 🟡 60% | Implement the Raft labs of MIT 6.824 in Go (essential-tier) |
| Machine learning | 🟡 55% | Solidify the math (linear algebra, probability) separately; practice on Kaggle |
| Architecture & parallelism | 🟡 65% | Profile on real hardware; implement CUDA/parallel code |
| **Mathematical foundations** | 🟠 40% | **This is the biggest weakness** (see below) |

## 🔢 The Biggest Weakness: Mathematical Foundations

Honestly, CS Quest follows a "grasp the core with minimal math" approach, so **training in math itself is thin.**
If you're seriously aiming for the graduate level, solidifying the following in parallel will deepen your understanding of the course by a notch:

1. **Linear algebra** — the language of machine learning, graphics, and data processing. Matrices, eigenvalues, singular value decomposition
   - Recommended: [3Blue1Brown "Essence of Linear Algebra"](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) (intuition) + Strang's lectures (MIT 18.06)
2. **Probability & statistics** — the foundation of ML, randomized algorithms, and performance analysis
   - Using the probability chapter of World 9 as a springboard, move on to probability distributions, estimation, and hypothesis testing
3. **Calculus** — the math of gradient descent (GRAD 3)
4. **Discrete math** — already covered in World 9 (this is where CS Quest is strong)

> 💡 For those afraid of math: don't tackle the specialized texts head-on. First feel "what is this math good for" in each world of CS Quest, then come back — that gives you the motivation to keep going. Doing it in the reverse order makes it easy to give up.

## 🛠️ Practical Challenges to Build "the Experience of Walking the Road"

To turn the map into a journey, there's no choice but to get your hands moving. In priority order:

### Level 1: Do all of the course's implementation quests (essential)
Take the 💻 implementation quests scattered throughout the README and **actually write them in code and run them.** This alone makes a difference — many people drop out here.
- Dynamic arrays, linked lists, hash tables, BSTs, heaps, the various sorts, BFS/DFS, the various DP problems
- Repeat the coding problems in Appendix I until you can solve them **with nothing in front of you**

### Level 2: Tackle each field's "famous labs" (strongly recommended)
The hands-on assignments published by the world's top universities:
- **OS**: the xv6 labs of [MIT 6.S081](https://pdos.csail.mit.edu/6.S081/) (modify a small UNIX)
- **Distributed**: the MapReduce + Raft labs of [MIT 6.824](https://pdos.csail.mit.edu/6.824/) (Go)
- **Compilers**: [Crafting Interpreters](https://craftinginterpreters.com/) (free; a classic where you build your own language)
- **CS fundamentals overall**: [CS50](https://cs50.harvard.edu/) (Harvard's intro course, well-supported)
- **ML**: [fast.ai](https://www.fast.ai/) or Andrew Ng's Coursera + Kaggle

### Level 3: Build your own project (where it becomes real strength)
Complete one **reasonably sized** thing that combines several fields you've learned.
- Example: your own key-value store (storage + WAL + networking + concurrency)
- Example: a mini search engine (crawl + index + ranking)
- Example: a chat app (WebSocket + DB + auth), actually deployed
The experience of completing and debugging it is what helps most, in interviews and on the job alike.

### Level 4: Read and write papers (the entrance to research)
From the original [Papers section](https://github.com/jwasham/coding-interview-university#papers), read the classics (MapReduce, Raft, Dynamo, Transformer, etc.).
Once you can read them, try writing up your own experiments. This is the world of graduate school.

## 🗓️ A Realistic Time Estimate

| Goal | Rough time required (at 2–3 hours a day) |
|---|---|
| Clear the First Continent (interview-ready level) | 3–6 months |
| Clear the Second Continent (cover the main undergraduate subjects) | +6–12 months |
| Clear the Heavens (the entrance to graduate school) | +6–12 months |
| Real skill including the labs and projects | 2–4 years overall |

This is the **same order of magnitude** as a 4-year undergraduate degree + a 2-year master's. Of course — you're handling the same volume of knowledge.
There are no shortcuts, but because you **have the order and the map**, the wandering of self-study is greatly reduced. That is the value of this course.

## 🌅 The Elder's Final Advice

> "Your wish — 'I want to be able to understand it from this course alone' — is the right one.
> That's why I prepared not just the problems but **complete solutions and explanations** in the appendices (Appendices I, II, III).
> Grasp the concepts in the lectures, get your hands moving with the problem sets, and make them flesh and blood with the implementation quests — with these three in place,
> as teaching material it carries you to the very limit of how far self-study can go.
>
> But the final step, 'the experience of having walked the road,' is the one thing I cannot give you. It comes only from you writing code,
> suffering through bugs, and giving a small fist-pump the moment it works — only from accumulating that.
>
> I've handed you the map. I've given you the problem set and the solutions too. Now, set out on your journey.
> The one who becomes a Grand Sage is not the one who has finished reading. **It is the one who has finished doing.**"

➡️ [Back to CS Quest Home](README.md) ・ [Complete Coding Problems](appendix-01-coding-problems.md) ・ [Complete System Design Problems](appendix-02-system-design.md) ・ [Complete Architecture Problems](appendix-03-architecture-problems.md)
