# Module 8 — Customer Skills: Discovery, Scoping & Executive Communication (Weeks 24–25)

> Goal: build the half of the FDE job that engineers systematically underestimate. Anthropic's
> loop has a customer-conversation simulation that reportedly filters out ~60% of candidates
> *who already passed the coding rounds*. You cannot cram this the week before; you can train it
> in two focused weeks and keep practicing.

Everything here is practiced **out loud and in writing** — reading about communication trains
nothing.

---

## Week 24 — Discovery and scoping

### Lesson 8.0 — Business fundamentals: how enterprises buy, and what "value" means

You can't scope what you can't price. Before the conversation skills, internalize the business
machinery your work lives inside:

- [ ] **How enterprise software gets bought**: champion → economic buyer → security review →
      procurement → legal. Know who an FDE serves at each stage and why deals die at each
      stage (no quantified value, failed security review, no internal owner after you leave).
- [ ] **The ROI equation you'll reuse forever**:
      `value = (hours saved × loaded hourly cost) + revenue lift + risk reduction − (build cost
      + run cost + maintenance)`. Practice it on TicketFlow AI: tickets/day × minutes saved ×
      agent cost vs your Module 6 cost-per-ticket number. Put the result in the exec one-pager
      (Lesson 8.3) — a deployment that "saves $310k/yr and costs $18k/yr to run" is how FDEs
      talk.
- [ ] **Pilot → production economics**: why pilots are scoped to one team with a hard metric;
      what "land and expand" means; why an unmeasured successful pilot is a failed pilot.
- [ ] **Build vs buy vs wait**: be able to argue all three honestly for a given use case —
      including "wait two model generations," which is sometimes the right call and always a
      credibility builder.
- [ ] **Read the customer's business in 2 hours**: for one public company in an industry you
      like, skim the latest annual report / earnings call summary and answer: how do they make
      money, what's their biggest cost center, where would AI plausibly move a number they
      report? Write 10 lines. Do this twice. (FDEs do exactly this before a first meeting.)

### Lesson 8.1 — Discovery: finding the real problem

Customers describe solutions ("we want a chatbot"), not problems ("our agents spend 40% of
their time searching old tickets"). Discovery is the structured conversation that gets from the
first to the second.

- [ ] Learn the question ladder, and write your own version of it:
      - *Workflow*: "Walk me through the last time this happened, step by step."
      - *Pain quantification*: "How often? How long does it take? Who does it? What does an
        error cost?"
      - *Current workarounds*: "What have you tried? Why didn't it stick?"
      - *Success definition*: "If this works perfectly, what number changes on whose dashboard?"
      - *Constraints*: data access, security, systems involved, who must approve.
- [ ] Anti-patterns to drill out of yourself: pitching before understanding; accepting the
      stated solution; talking to only one stakeholder; technical jargon during discovery;
      hearing "AI should do X end-to-end" and not probing for the 20% slice that delivers 80%.
- [ ] **Practice (required, with a human)**: recruit a friend/colleague and give them a
      one-paragraph persona ("you run claims processing at an insurer; you're skeptical;
      you have a vendor horror story"). Run a 30-minute discovery call. Record it. Listen to it
      — count how often you interrupted, pitched early, or asked leading questions. Run it
      again with a second persona. (If truly no human is available, run it against an LLM
      role-playing the customer — worse than a human, far better than nothing.)

**Study**: *The Mom Test* (Rob Fitzpatrick) — short, the single best book on asking customers
questions; written for founders, maps 1:1 to FDE discovery.

### Lesson 8.2 — Scoping: from problem to steel thread

- [ ] **Steel thread**: the thinnest end-to-end slice proving the core value (one ticket
      category fully automated, not all categories half-automated). Practice: for 5 problem
      statements (invent them from industries you know), write a steel-thread scope in 5
      sentences each.
- [ ] **Feasibility triage** — the FDE judgment call. For any proposed AI use case, assess:
      Is the data accessible and good enough? Is the task verifiable (can you build an eval)?
      What's the cost of a wrong answer, and is there a human checkpoint? Does model capability
      today actually cover it? Practice on 10 use cases; sort into *build now / pilot
      carefully / decline*. Being able to say "decline, because…" is senior-signal.
- [ ] **Write a Statement of Work-lite** for TicketFlow AI as if a customer engagement:
      problem, scope (in AND out — the "out" list is where projects die), milestones with demo
      dates, success metrics, risks with mitigations, what you need from the customer (data
      access, a domain expert 2h/week, a security review slot). Template it; reuse forever.

## Week 25 — Communication artifacts and executive presence

### Lesson 8.3 — Writing (FDEs write constantly)

Produce all four artifacts for TicketFlow AI, for real, in `writeups/`:

- [ ] **Design memo** (1–2 pages): context → options considered → recommendation → trade-offs →
      decision needed. Top-down structure: the busy reader gets everything from the first
      five lines.
- [ ] **Weekly status update** (10 lines max): shipped / metric movement / blocked on /
      next week / risks. Write the imaginary week-3 update where something slipped — practice
      reporting bad news early and plainly.
- [ ] **Executive one-pager**: what we built, the number it moved, what it costs to run,
      what's next. Zero jargon. Test: a non-technical friend reads it in 3 minutes and can
      repeat the point back.
- [ ] **Handoff/runbook doc**: how to operate, monitor, and extend the system after you leave.
      (FDEs leave. The doc is the deliverable that makes expansion possible.)

### Lesson 8.4 — Demos and the executive conversation

- [ ] **Demo craft**: narrate problem → live product → the number → next step. Never demo
      from a feature list; demo from the user's day. Always have a recorded backup. Show one
      handled failure on purpose. Re-record your Module 5 demo applying all of this; compare.
- [ ] **Translation drill**: explain each of these to a smart non-engineer, out loud, ≤60
      seconds each, recorded — context windows; why the model "lies" (hallucination); why we
      need an eval suite before shipping; why this costs $0.04/ticket; what prompt injection is.
      Listen back. Kill the jargon. Repeat until clean.
- [ ] **Pushback simulation** (the interview round, rehearsed): have a friend or an LLM play —
      an exec demanding an impossible deadline; a CISO with Module 7's objections; an engineer
      on the customer side who feels threatened and is quietly blocking you. Goal in each:
      hold the technical boundary *and* keep the relationship. The move is always: acknowledge →
      reframe to the shared goal → offer the viable alternative with reasons → agree on a test.
- [ ] **Stakeholder mapping**: for your simulated engagement, chart sponsor / users / blockers /
      security / IT; what each cares about; what each needs from you weekly.

---

## Module 8 exit criteria

- [ ] Two recorded discovery calls done and self-reviewed.
- [ ] ROI math done on your own project, and two 10-line business teardowns written.
- [ ] SOW-lite, design memo, status update, exec one-pager, runbook — all in `writeups/`.
- [ ] Translation drill recordings pass the no-jargon test.
- [ ] One pushback simulation recorded where you held the line without losing the room.

*Next → [Module 9: Capstone Projects](09-capstone-projects.md)*
