# Module 1 — The FDE Role & Mindset (Week 3)

> Goal: understand precisely what the job is, how it differs across companies, and start
> practicing the operating mindset — because the interviews test the mindset, not just the code.

---

## Lesson 1.1 — History: from Palantir "Deltas" to frontier labs

Palantir invented the modern FDE model in the 2010s: instead of selling software and hoping
customers figure it out, send engineers **into** the customer to configure and extend the
platform until it solves the actual problem. Internally split into:

- **Echo (Deployment Strategist)** — owns the problem definition and the customer relationship.
- **Delta (Forward Deployed Software Engineer)** — owns the technical solution.

The model worked so well that Palantir alumni (mostly FDE-adjacent) founded 100+ companies. When
LLMs arrived, the same gap reappeared at massive scale: frontier models are general-purpose, and
enterprises can't bridge "GPT/Claude/Gemini exists" → "our claims processing is automated" alone.
OpenAI, Anthropic, and Google all built FDE teams to close that gap; OpenAI went furthest in 2026
by spinning up an entire deployment-focused company.

- [ ] Read: [A Day in the Life of a Palantir Forward Deployed Software Engineer](https://blog.palantir.com/a-day-in-the-life-of-a-palantir-forward-deployed-software-engineer-45ef2de257b1)
- [ ] Read: [Why OpenAI and Anthropic are hiring forward deployed engineer teams (The New Stack)](https://thenewstack.io/forward-deployed-engineers-ai/)
- [ ] Read: [The Definitive Guide to Forward Deployed Engineering (Vinoo Ganesh)](https://vinoo.io/writing/2026-02-05-forward-deployed-engineering/)

## Lesson 1.2 — The role, company by company

Read 3–5 **live job postings** and build your own comparison table. Postings rotate; search each
careers site for "forward deployed" and "applied AI."

- [ ] OpenAI careers — FDE postings (note: full-stack emphasis, Postgres explicitly named,
      "last line of defense" production ownership, high-stakes deployments).
- [ ] Anthropic careers — FDE (Applied AI) postings (note: MCP servers, sub-agents, agent skills
      as named deliverables; evaluation frameworks; "operate autonomously, thrive under
      ambiguity"; safety culture).
- [ ] Google Cloud / DeepMind — applied AI & FDE-style postings around Gemini.
- [ ] Palantir — FDSE and Forward Deployed AI Engineer postings.

**Deliverable**: a one-page table in your portfolio `writeups/role-research.md`:
rows = companies; columns = *what they build, required skills, seniority bar, interview loop
(from Glassdoor/Blind/guides), what's unique*. You will reuse this in Module 10 verbatim.

## Lesson 1.3 — The FDE operating loop

Every engagement follows roughly the same loop. Memorize it; Modules 8–9 drill it.

1. **Discover** — interview stakeholders, watch the real workflow, find where value leaks.
2. **Scope** — pick the thinnest slice that proves value ("steel thread"); write it down; get
   explicit agreement on what success looks like (metrics!).
3. **Build** — ship the slice fast, in their environment, with their constraints.
4. **Evaluate** — measure against the agreed metric; demo honestly, failures included.
5. **Harden** — security, reliability, monitoring, handoff docs.
6. **Expand or exit** — codify the repeatable pattern, feed it back to product, move on.

The non-obvious part: steps 1, 2, and 4 are where FDEs earn their pay. Building is assumed.

## Lesson 1.4 — The mindset (what interviewers probe for)

- **Ownership without authority.** You're a guest in someone else's org with no formal power.
  You ship anyway.
- **Ambiguity tolerance.** "Make AI work for our claims team" is a complete spec at some
  customers. You turn it into one.
- **Ruthless pragmatism.** A cron job that works beats an elegant system that ships next
  quarter. But you must know *which* corners are safe to cut (Modules 6–7 teach the unsafe ones).
- **Honest signal.** When the model isn't good enough for the use case, you say so early —
  credibility is the asset. Anthropic's loop explicitly screens for this; OpenAI's behavioral
  round simulates holding a technical boundary against a pushy executive.
- **Pattern extraction.** The best FDEs leave behind reusable assets, not just one-off hacks.

**Exercise** — pick a company you've worked at (or your school/club). Write half a page: if an
FDE from an AI lab embedded with that org for 8 weeks, (a) what workflow should they attack
first, (b) what would the steel thread be, (c) what metric would prove value? Put it in
`writeups/`. This exact question shape appears in FDE interviews.

## Lesson 1.5 — Is this role for you?

Honest negatives, from people in the seat: significant travel and customer-site time; context
switching across customers; you sometimes build with the customer's legacy stack, not the fun
one; pressure is real ("the demo is Tuesday"); some weeks are more meetings + Slack diplomacy
than code. The upside: maximum learning rate in tech right now, direct view of what AI is
actually worth, and the strongest known pipeline to founding companies.

- [ ] Write 5 sentences in your portfolio README: why you want this specific role (not "AI is
      cool"). Interviewers ask. A rehearsed-but-true answer is a free pass on a hard question.

---

## Module 1 exit criteria

- [ ] Role-comparison table committed to `writeups/role-research.md`.
- [ ] FDE-loop exercise written.
- [ ] You can explain to a friend, in 2 minutes, the difference between an FDE, a solutions
      architect, and a consultant — out loud. Actually do this.

*Next → [Module 2: Production Engineering Foundations](02-production-engineering.md)*
