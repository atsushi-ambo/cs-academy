# Module 6 — Evaluation, Observability & Reliability (Weeks 19–21)

> Goal: be the person in the room who can answer "how do we know it works?" — with numbers.
> Evals are the single most-cited differentiator in FDE/Applied-AI interview loops (Anthropic's
> system design round is explicitly eval-focused), and the most common gap in candidates.

The customer conversation that defines this module:
> **Customer:** "We tried it on a few examples and it seems good. Ship it?"
> **You:** "Here's our eval suite, the score, the failure taxonomy, and the regression gate.
> Now we can ship it."

---

## Week 19 — Eval design

- [ ] **From vibes to metrics**: turn a fuzzy goal ("answers should be good") into measurable
      criteria (groundedness, completeness, format compliance, tone, refusal-correctness).
- [ ] **Build a golden dataset** for TicketFlow AI: 100+ labeled examples. Sources: synthetic
      generation (model-assisted, human-verified), edge cases from your Field Notes, adversarial
      cases. Learn why 30 good examples beat 1000 sloppy ones — and why you start collecting
      from day 1 of an engagement.
- [ ] **Grader types** and when each is trustworthy:
      - exact match / regex / schema checks (cheap, brittle, great for extraction & SQL),
      - execution-based (run the generated SQL/code, compare results — strongest when possible),
      - **LLM-as-judge** (rubric design, position bias, self-preference bias; calibrate the
        judge against ~30 human labels before trusting it),
      - human review (the gold standard you're economizing).
- [ ] Implement the eval harness: a `pytest`-style runner that takes (dataset, system version) →
      scorecard. Run it on 3 prompt variants of your RAG pipeline; pick a winner **with data**.
- [ ] **Agent evals** (harder, interview-favorite): evaluate trajectories, not just final
      answers — did it call the right tools, with right args, in a sane order? Tool-call
      accuracy, task completion rate, steps-to-completion, cost-per-task.
- [ ] RAG-specific: retrieval metrics (recall@k, MRR) measured **separately** from generation
      quality, so you know which half is broken.

**Study**
- [ ] Anthropic docs — [empirical evals guide](https://docs.anthropic.com/en/docs/test-and-evaluate).
- [ ] Hamel Husain — ["Your AI Product Needs Evals"](https://hamel.dev/blog/posts/evals/) and the error-analysis follow-ups. Read closely; this is the practitioner canon.
- [ ] Skim an eval framework (promptfoo / Braintrust / LangSmith evals) and decide what your
      hand-rolled harness is missing.

## Week 20 — Error analysis & the improvement loop

- [ ] **Error analysis ritual**: run the suite → read every failure (yes, manually) → tag with a
      failure taxonomy you invent (bad retrieval / bad reasoning / format / refusal / data bug) →
      fix the biggest category → re-run. Do **three full cycles** on TicketFlow AI and chart the
      score. This loop *is* applied AI engineering; interviewers ask you to narrate it.
- [ ] **Regression gates in CI**: evals run on every PR that touches a prompt; a score drop
      blocks merge. Wire it into your GitHub Actions from Module 2.
- [ ] **Drift**: model version upgrades silently change behavior. Pin versions; re-run suite on
      upgrades; keep a model-upgrade changelog like you would a dependency.
- [ ] **Online signals**: thumbs up/down, edit-distance between draft and what the human
      actually sent, escalation rate. Design the feedback capture into the product UI.

## Week 21 — Observability & reliability for LLM systems

- [ ] **Tracing**: every request gets a trace — prompt version, model, tokens, cost, latency,
      tool calls, retrieved chunks. Instrument TicketFlow AI (OpenTelemetry or a platform like
      LangSmith/Langfuse/Braintrust — pick one and go deep).
- [ ] **Dashboards a customer exec can read**: cost/day, p50/p95 latency, success rate,
      escalation rate. Build it.
- [ ] **Reliability patterns**: timeout budgets per step; retries with jitter (idempotency!);
      **fallback chains** (primary model → cheaper model → static response); circuit breakers;
      queue + async for spiky load; graceful degradation when a provider has an outage (they
      do — design for it, and know each provider's status-page history).
- [ ] **Cost control in production**: caching (exact + prompt-cache), model routing
      (cheap model for easy cases, escalate hard ones), context pruning, batch APIs for
      offline work. Exercise: cut TicketFlow AI's cost per ticket by 50% without dropping your
      eval score. Document the levers you pulled — superb interview story.
- [ ] **Incident drill**: simulate "quality regressed in prod but no code changed." Walk the
      diagnosis: model upgraded? corpus changed? traffic mix shifted? prompt-cache poisoned?
      Write the post-mortem in `writeups/`.

---

## Module 6 deliverable

`writeups/ticketflow-eval-report.md` — golden dataset description, harness design, 3-cycle
improvement chart, regression-gate setup, cost-reduction results. This single document,
walked through aloud in 10 minutes, is your strongest interview asset.

## Module 6 exit criteria

- [ ] You can design an eval for any task an interviewer names, in under 3 minutes, covering:
      dataset, graders, metrics, and how it gates deployment.
- [ ] CI blocks a prompt change that tanks quality — demonstrate it with a deliberately bad PR.
- [ ] You can explain LLM-as-judge pitfalls and how you calibrated yours.

*Next → [Module 7: Enterprise Deployment](07-enterprise-deployment.md)*
