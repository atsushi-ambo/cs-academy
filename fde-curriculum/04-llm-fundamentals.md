# Module 4 — LLM Fundamentals & Prompt Engineering (Weeks 11–13)

> Goal: understand how LLMs behave well enough to predict failures before they happen, and steer
> models reliably with prompts. FDEs don't train models — but they must out-understand the
> customer's engineers about *model behavior*.

---

## Week 11 — How LLMs actually work (the FDE-relevant 20%)

You need a working mental model, not research depth.

- [ ] **Tokens**: what they are, why "how many r's in strawberry" fails, why token counts drive
      cost and latency. Play with a tokenizer visualizer until it's intuitive.
- [ ] **Next-token prediction & sampling**: temperature, top-p; why outputs vary; when to set
      temperature 0 (and why that still isn't fully deterministic).
- [ ] **Context windows**: what fits, what it costs, "lost in the middle" degradation, why
      "just stuff everything in context" eventually fails — and when it's actually fine.
- [ ] **Training pipeline at a glance**: pretraining → instruction tuning → RLHF/RLAIF. Enough
      to explain why models are sycophantic, why they hallucinate, and what a system prompt is.
- [ ] **Model landscape**: current Claude / GPT / Gemini families and open-weights (Llama,
      Mistral, Qwen). For each: context length, cost per Mtok, latency class, modality. Build a
      comparison sheet and **refresh it monthly** — stale model knowledge reads terribly in
      interviews.
- [ ] **Multimodality**: image/PDF/audio inputs; when vision solves a problem OCR can't.

**Study**
- [ ] Karpathy — [Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) (1h, the single best foundation).
- [ ] Karpathy — [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) (optional but excellent).
- [ ] [3Blue1Brown — Transformers, visually](https://www.youtube.com/watch?v=wjZofJX0v4M) (intuition only; skip the math guilt-free).

## Week 12 — Prompt engineering, seriously

Prompting is the FDE's primary tuning knob: it ships instantly, costs nothing, and solves the
majority of "the model is wrong" complaints.

- [ ] Read the prompt engineering guides from **both** [Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
      and [OpenAI](https://platform.openai.com/docs/guides/prompt-engineering); note where they
      disagree.
- [ ] Master, with hands-on exercises for each: role/system prompts; structured output (JSON
      mode / tool-schema-enforced output); few-shot examples (and when they backfire); chain of
      thought and "think step by step" vs reasoning models that do it natively; XML/markdown
      sectioning for long contexts; putting instructions *after* long documents; prompt
      injection awareness (deep dive in Module 7).
- [ ] **Reasoning models** (o-series, Claude extended thinking, Gemini thinking): what they're
      for, what they cost in latency/$, when a customer problem justifies them.
- [ ] Caching: prompt/context caching on Anthropic & OpenAI — restructure a prompt so the
      static 90% is cached; measure the cost difference.

**Exercise — the prompt gym.** Pick 5 tasks (extract fields from messy invoices; classify
support tickets into a taxonomy; rewrite legal text at 8th-grade level; generate SQL from a
question + schema; grade an essay against a rubric). For each: write a prompt, create 20 test
inputs, get accuracy ≥ 90% by iterating on the prompt **only**. Log every iteration — the
discipline of "change one thing, measure" is Module 6 in embryo.

## Week 13 — Working with model APIs like a professional

- [ ] Build a thin **provider-agnostic client** (or learn one: LiteLLM / Vercel AI SDK) over
      Anthropic + OpenAI + Gemini: streaming, retries with backoff, timeout budgets, token
      counting, cost logging per request.
- [ ] **Streaming UX**: stream tokens to your TicketFlow frontend (SSE). Measure and internalize
      time-to-first-token vs total latency — customers feel TTFT.
- [ ] **Structured outputs in anger**: schema-validated extraction with retry-on-invalid;
      know failure modes (truncation mid-JSON, schema drift).
- [ ] **Cost & latency engineering**: estimate cost for "50k support tickets/day, 2k tokens in,
      300 out" across 3 models. Build a tiny spreadsheet model. FDE interviews love napkin math.
- [ ] **Rate limits & quotas**: design a worker that respects RPM/TPM limits with a queue.
- [ ] **Fine-tuning vs prompting vs RAG**: when each wins. Default answer: prompting + RAG;
      fine-tuning for style/format at scale or latency-critical classification. Be able to
      defend this hierarchy — it's a standard interview probe.

**Deliverable — "Model Behavior Field Notes."** A public repo/page where you document 10
surprising model behaviors you found yourself (with reproducible prompts): a hallucination
pattern, a formatting quirk, a cross-model disagreement, a context-position effect… This is an
unusually strong portfolio piece because it demonstrates the core FDE skill: *empirical curiosity
about model behavior*.

---

## Module 4 exit criteria

- [ ] Explain tokens → cost → latency → context limits in one breath, to a non-engineer.
- [ ] Prompt gym: 5/5 tasks at ≥90% on your own test sets.
- [ ] Streaming, schema-validated, cost-logged API client working in TicketFlow.
- [ ] Field Notes published with 10 entries.

*Next → [Module 5: Building LLM Applications](05-building-llm-applications.md)*
