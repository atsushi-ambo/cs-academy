# Module 9 — Capstone: Simulated Customer Engagements (Weeks 26–28)

> Goal: run the **entire FDE loop** — discovery → scope → build → evaluate → harden → handoff —
> three times, end to end, under time pressure. These are the projects you'll demo in
> interviews and the stories you'll tell in behavioral rounds. Treat each as a real engagement
> with a real (simulated) customer.

**Rules of engagement**
1. Each capstone gets a **hard one-week time-box**. Shipping a smaller scope on time beats
   shipping a bigger scope late — that *is* the lesson.
2. Each needs a "customer": a friend playing a persona, or an LLM with a detailed persona
   prompt who you must interview for requirements and demo to weekly. Do not skip this; the
   artifacts from these conversations are half the portfolio value.
3. Every capstone produces the full artifact set: SOW-lite → working deployed system → eval
   report with numbers → security note → exec one-pager → runbook → 5-min demo video.
4. Use a different model provider as the primary for each capstone (Claude / GPT / Gemini),
   with at least one going through a cloud-mediated route (Bedrock/Vertex/Azure).

---

## Capstone A (Week 26) — Document intelligence for a regulated industry

**Persona**: Operations lead at a mid-size insurance company. 30k claims/year arrive as PDFs
(scans, photos, forms). Adjusters re-type data and miss policy exclusions. Skeptical of AI
after a failed chatbot pilot; security team is strict.

**Likely shape** (let discovery decide, but expect): multimodal extraction from messy PDFs →
schema-validated fields with confidence scores → policy-exclusion flagging via RAG over policy
docs → human review queue where low-confidence items route to people → metrics dashboard
(straight-through rate, minutes saved). Eval suite with a labeled set of ≥50 documents you
assemble (public insurance forms, synthetic claims).

**What it proves**: multimodal handling, extraction evals, human-in-the-loop design,
regulated-industry security posture (your Module 7 briefing, adapted).

## Capstone B (Week 27) — Agent automation inside business systems

**Persona**: Head of customer success at a B2B SaaS startup. Support runs on email + a shared
inbox + a wiki + Stripe. Wants "AI to handle support" (you must scope this down); fears wrong
refunds and hallucinated promises.

**Likely shape**: triage-and-draft agent — classifies incoming requests, pulls account context
via tools (mock or sandbox Stripe + a wiki you create), drafts responses with citations,
auto-resolves only the provably safe category, routes everything else to humans with a
pre-filled summary. MCP server exposing the business systems; approval queue; trajectory evals
(tool-call accuracy, escalation correctness); spend/latency budget per ticket.

**What it proves**: agents + MCP + tool permissioning + the judgment to scope *down* an
overbroad ask — narrate that scoping decision in the demo video, it's the most senior moment
in your portfolio.

## Capstone C (Week 28) — Analytics copilot over enterprise data

**Persona**: CFO of a retail chain. Analysts spend days each month answering "why did margin
drop in region X?" Data lives in a warehouse (simulate with Postgres/DuckDB + a public retail
dataset). Wrong numbers are worse than no numbers.

**Likely shape**: text-to-SQL with schema grounding and a read-only, allowlisted connection →
result verification (row counts, sanity checks, "show me the SQL" transparency) → chart/summary
generation → execution-based eval suite (50 question/SQL/answer triples — graded by running
the query, not by judging text) → "I don't know / ambiguous question" refusal behavior, tested.

**What it proves**: data engineering + text-to-SQL done responsibly + execution-based evals +
communicating uncertainty to executives who will quote your numbers in a board meeting.

---

## The portfolio assembly (rolling, finish end of Week 28)

- [ ] Portfolio README rewritten as a professional index: one paragraph + metrics + demo link
      per project. Lead with TicketFlow AI and the three capstones.
- [ ] **Write one public blog post** about the most interesting technical problem you hit
      (e.g., "What broke when I put an agent in front of refunds"). Recruiters and hiring
      managers at the labs genuinely read these; one good post outperforms ten repos.
- [ ] Cross-link everything: each repo README → writeups → demo videos → blog post.
- [ ] The honest-failures page: one section listing what *didn't* work across the program and
      what you changed. Counterintuitively, this is the page interviewers remember.

## Module 9 exit criteria

- [ ] Three capstones live, each with the complete artifact set.
- [ ] All three demo videos under 5 minutes, each showing one handled failure.
- [ ] A stranger (not your "customer") can follow each runbook and operate the system.
- [ ] Blog post published.

*Next → [Module 10: Interview Preparation & Job Search](10-interview-prep.md)*
