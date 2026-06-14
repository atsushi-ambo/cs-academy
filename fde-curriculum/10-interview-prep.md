# Module 10 — Interview Preparation & Job Search (Weeks 29+)

> Goal: convert the portfolio into offers. FDE loops are multi-modal — practical coding,
> system design, customer simulation, behavioral — and each company weights them differently.
> You've built every skill they test; this module is about packaging and reps.

---

## Lesson 10.1 — Know the loops (refresh your Module 1 research — postings and loops drift)

**OpenAI (FDE/FDSE)** — high-velocity loop, often ~7 touches in 3–4 weeks: recruiter call →
technical screen → coding rounds (practical: build/integrate/debug, not algorithm trivia) →
a substantial **take-home (~5 hours, build something real with their API)** → system design →
behavioral centered on **customer empathy under pressure** (the "explain this to a skeptical
CISO" simulation — hold the technical boundary without losing the room) → leadership chat.

**Anthropic (FDE / Applied AI)** — recruiter screen → technical screen → coding (practical;
often with AI-tools-allowed policies — ask, and be excellent either way) → **customer
conversation simulation** (the famous filter; your Module 8 discovery reps are the prep) →
system design that leans **eval design** ("how would you know it works?") → values/safety
conversation (read their published views on safety; have a genuine opinion, not a recited one).

**Palantir (FDSE)** — decomposition-heavy coding screens → "Palantir-style" system design
(messy real-world constraints, data integration) → strong emphasis on drive/ownership stories.

**Google (Gemini-adjacent applied AI / FDE-style roles)** — closer to classic Google loops
(DSA still matters more here — your Module 3 work carries this) plus applied-AI rounds and
"Googleyness" behavioral.

- [ ] For each target company: re-read 3 current postings, search recent interview reports
      (Glassdoor/Blind/Reddit), and write a one-page brief: rounds, weights, your gap, your plan.

## Lesson 10.2 — The four round types, and your drills

### A. Practical coding
- [ ] Re-run Module 3's six practical drills cold, timed, narrating aloud.
- [ ] New drills: consume an unfamiliar REST API from docs in 45 min; debug a planted bug in
      a small FastAPI repo (have a friend or an LLM plant 3 bugs); stream-process a file too
      big for memory.
- [ ] If AI tools are allowed in the round: practice *with* them — interviewers grade how you
      direct, verify, and correct AI output. If not allowed: practice without. Know both modes.

### B. System design (incl. eval-centric)
- [ ] Redo Module 3's five designs from scratch — they should be 2× faster and crisper now.
- [ ] Eval-design drill (Anthropic-style): for 5 prompts like "customer wants to auto-answer
      RFPs," produce in 10 minutes: success metric, golden-set plan, grader design, deployment
      gate, online signal. You wrote the playbook in Module 6; compress it to reflex.
- [ ] One full mock with a human (tryexponent, interviewing.io, or a senior friend). Minimum
      two total mocks before the first real loop.

### C. Customer simulation
- [ ] Re-run Module 8's pushback simulations with fresh personas: the impossible-SLA exec;
      the CISO; the "just fine-tune it on everything" enthusiast; the silent stakeholder you
      must draw out. Record, review, repeat.
- [ ] Drill the universal move until it's muscle memory: **acknowledge → clarify the real
      need → reframe to the shared goal → offer the viable path with reasons → agree on a
      next step with a metric.**
- [ ] Prepare your "honest no" examples: times you told a customer/stakeholder something they
      didn't want to hear, kindly, with an alternative. Every lab probes for this.

### D. Behavioral
- [ ] Write 8–10 stories in STAR-with-numbers form, indexed by signal: ambiguity, ownership
      without authority, shipped under pressure, scoped down an overbroad ask, technical
      disagreement resolved, failure + what changed. Your capstones ARE these stories — that
      was the point of doing them as engagements, not projects.
- [ ] "Why this company / why FDE" — your Module 1 paragraph, now upgraded with everything
      you've built. For Anthropic specifically: engage genuinely with safety; for OpenAI:
      shipping velocity and customer obsession; for Palantir: ownership and impact.

## Lesson 10.3 — The take-home playbook

Take-homes are won on **product judgment per hour**, not features:
- [ ] Spend the first 30 minutes on scope: write a mini-SOW in the README *before coding*
      ("In scope / out of scope / why"). Reviewers at these companies notice this instantly.
- [ ] Include: a tiny eval (even 10 cases — most candidates have zero), error handling on the
      API path, cost/latency notes, and a "what I'd do with another week" section.
- [ ] Make it run in one command. A reviewer who can't run it scores it accordingly.
- [ ] Practice once: pick a real past take-home prompt (the guides in Resources have
      examples), do it in a hard 5-hour box, then review it like a hostile senior engineer.

## Lesson 10.4 — Pipeline mechanics

- [ ] **Resume**: one page, shipped-things-with-numbers, top third = your strongest capstone
      metrics. "Built and deployed agent system that auto-resolved 38% of support tickets at
      $0.04/ticket (eval suite: 150 cases, 94% precision)" — that sentence does more than any
      skills list.
- [ ] **Where to apply**: the four labs + Module 1's broader list. FDE-adjacent titles to
      search: *Forward Deployed Engineer, Applied AI Engineer, Solutions Engineer (AI),
      Deployment Engineer, Member of Technical Staff – Applied*. Apply broadly across the
      tier-2 list — interview practice compounds, and offers create leverage.
- [ ] **Referrals beat portals**: your blog post + a short genuine note to FDEs at target
      companies ("I built X, wrote up the failure modes here, would love 15 minutes") has a
      real hit rate. Do 10 of these.
- [ ] **Sequencing**: schedule practice-tier loops 2–3 weeks before target-tier loops.
- [ ] Track everything in a sheet: company, stage, date, learnings per round. After every
      interview, write down the questions while fresh and patch the gap within 48 hours.

## Lesson 10.5 — Keep current (the role moves fast)

Until you're hired (and after): weekly — release notes from all three labs; monthly — refresh
your Module 4 model comparison sheet and re-test one capstone against new models. An FDE
candidate who fluently discusses *this month's* model capabilities is rare and memorable.

---

## Final checklist — "am I ready to apply?"

- [ ] Portfolio: TicketFlow AI + 3 capstones, all live, all with eval numbers and demo videos.
- [ ] You can do a practical coding drill, narrated, under time, without panic.
- [ ] You can design an eval-gated LLM system on a whiteboard in 35 minutes.
- [ ] You've survived 3+ recorded customer simulations and can watch them without wincing.
- [ ] 8–10 behavioral stories written; "why FDE" answer is true and rehearsed.
- [ ] One blog post live; 10 outreach notes sent; tracking sheet exists.

When most of these are checked: apply. You will never feel 100% ready — FDEs ship at 80%
confidence and iterate, and so should you. 頑張って — go get it.

---

## Appendix — Curated resources

**Role & interviews**
- [Exponent — FDE Interview: The Definitive Guide](https://www.tryexponent.com/blog/forward-deployed-engineer-interview-the-definitive-2026-guide-fde)
- [Sundeep Teki — FDE Interview Guide](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) and [Forward Deployed AI Engineer career guide](https://www.sundeepteki.org/advice/forward-deployed-ai-engineer)
- [The New Stack — Why OpenAI and Anthropic are hiring FDE teams](https://thenewstack.io/forward-deployed-engineers-ai/)
- [Vinoo Ganesh — The Definitive Guide to Forward Deployed Engineering](https://vinoo.io/writing/2026-02-05-forward-deployed-engineering/)
- [Palantir — A Day in the Life of an FDSE](https://blog.palantir.com/a-day-in-the-life-of-a-palantir-forward-deployed-software-engineer-45ef2de257b1)
- [OpenAI interview guide (official)](https://openai.com/interview-guide/)

**Technical canon (one link per module, the single best thing)**
- M2: [The Twelve-Factor App](https://12factor.net/) · M3: [System Design Primer](https://github.com/donnemartin/system-design-primer)
- M4: [Karpathy — Intro to LLMs](https://www.youtube.com/watch?v=zjkBMFhNj_g) · M5: [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) + [MCP docs](https://modelcontextprotocol.io/)
- M6: [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) · M7: [OWASP Top 10 for LLM Apps](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- M8: *The Mom Test* (Fitzpatrick)

**Keep current**: Anthropic/OpenAI/Google AI release notes & cookbooks; Latent Space podcast;
Simon Willison's blog (the best running commentary on LLM capabilities and prompt injection).
