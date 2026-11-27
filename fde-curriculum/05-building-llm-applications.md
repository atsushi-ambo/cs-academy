# Module 5 — Building LLM Applications: RAG, Tools, Agents, MCP (Weeks 14–18)

> Goal: master the four load-bearing patterns of applied AI. Anthropic's FDE posting literally
> names the deliverables: *"MCP servers, sub-agents, and agent skills used in production
> workflows."* This module is the technical heart of the curriculum.

A strong default: **use the provider SDKs directly** and understand every moving part. Learn
frameworks (LangChain/LlamaIndex et al.) afterwards, as accelerators — FDE interviews punish
candidates who can only operate a framework.

---

## Week 14 — Retrieval-Augmented Generation (RAG), built from parts

Rebuild Module 0's "Ask My Docs" properly. Corpus: ~200 real documents (e.g., a product's docs
dump, or Wikipedia subset).

- [ ] **Ingestion**: parsing (PDF/HTML/Markdown), cleaning, chunking. Try 3 chunking strategies
      (fixed, semantic/heading-based, with overlap); you'll measure which wins properly in Module 6.
- [ ] **Embeddings & vector search**: embed with a hosted model; store in **pgvector** (you
      already run Postgres — FDE bonus: one less system to sell to the customer's security team).
- [ ] **Hybrid retrieval**: BM25/full-text + vector + **reranking** (hosted reranker). Hybrid
      beats pure-vector embarrassingly often; know why (exact identifiers, jargon, codes).
- [ ] **Generation**: grounded answers with **citations** back to chunks; refusal when the
      corpus doesn't contain the answer (this matters more to enterprises than fluency).
- [ ] **The failure tour**: deliberately produce — a confidently wrong answer from a bad chunk;
      a "lost in the middle" miss; a stale-index miss after a doc updates. Write each up in
      Field Notes.
- [ ] Know the scaling story: when pgvector runs out, what's next (dedicated vector DBs,
      managed search); metadata filtering; multi-tenancy isolation.

**Study**: Anthropic & OpenAI RAG/retrieval cookbooks; [pgvector docs](https://github.com/pgvector/pgvector).

## Week 15 — Tool use / function calling (the gateway to agents)

- [ ] Give a model tools against **TicketFlow's real API**: `search_tickets`, `get_ticket`,
      `update_status`, `post_comment`. Natural language in → correct API calls out.
- [ ] Tool design craft: descriptions are prompts; few, well-named tools beat many; return
      errors as structured content the model can react to; pagination/truncation of tool results.
- [ ] Parallel tool calls; multi-step chains (model calls tool → reads result → calls next).
- [ ] **Text-to-SQL** done responsibly: schema in context, read-only connection, allowlist,
      result-size limits. Build it against TicketFlow's DB. (Every enterprise asks for this.)
- [ ] Handle the ugly parts: model calls a tool that doesn't exist; arguments fail validation;
      tool times out. Your harness must survive all three.

## Week 16 — Agents

An agent = model + tools + loop + stop conditions. The engineering is in the loop, not the magic.

- [ ] Build a **support-triage agent** for TicketFlow from raw SDK calls: it reads new tickets,
      searches docs (Week 14 RAG as a tool), drafts replies, escalates what it can't handle.
      Max-iteration guard, token/cost budget, full trace logging of every step.
- [ ] **Human-in-the-loop**: the agent *proposes*, a human approves destructive actions. Build
      the approval queue UI. Enterprises will not deploy without this; FDEs who design for it
      win deals.
- [ ] **Sub-agents / orchestration**: a planner that delegates to specialized workers (triage →
      {billing-agent, tech-agent}). When this helps (context isolation, parallelism) vs when
      it's complexity cosplay.
- [ ] **Memory & state**: conversation persistence, summarization-compaction when context
      fills, resumability after a crash (persist the agent's state machine, not just chat).
- [ ] Read: [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
      (workflows vs agents; start simple). This essay's vocabulary is interview lingua franca.
- [ ] Study one production harness deeply (e.g., Claude Code or an open agent repo): how it does
      planning, tool permissioning, context compaction.

## Week 17 — MCP (Model Context Protocol) & the integration layer

MCP is the standard plumbing for "model ↔ enterprise systems" — and a named FDE deliverable.

- [ ] Understand the protocol: servers, clients, **tools / resources / prompts**, transports
      (stdio, streamable HTTP). Read the [MCP docs](https://modelcontextprotocol.io/).
- [ ] **Build an MCP server for TicketFlow** (Python or TS SDK): expose its API as MCP tools;
      connect it to Claude Desktop/Code and drive your app from chat.
- [ ] Build a second MCP server wrapping something messier — a legacy SOAP/XML API or a
      directory of CSVs. The skill being trained: *wrapping ugly enterprise systems in a clean
      model-facing interface*. That sentence is half the FDE job.
- [ ] Auth for MCP in enterprises: OAuth flows, scoped tokens, audit logging of tool calls.
- [ ] **Agent skills**: package a repeatable procedure (e.g., "weekly ticket-trends report")
      as a reusable skill/prompt+scripts bundle.

## Week 18 — Putting it together + frameworks survey

- [ ] **Ship "TicketFlow AI"**: RAG-grounded answers + triage agent + approval queue + MCP
      server, deployed, demoable in 5 minutes. This is a flagship portfolio piece.
- [ ] Record a **5-minute demo video**: the problem, the live product, one failure case and how
      the system contains it. (Showing a failure on purpose is a senior move; do it.)
- [ ] Frameworks fly-by (1 day each, build a toy, form an opinion): LangGraph; LlamaIndex;
      Vercel AI SDK; one eval/observability platform's SDK. Write a paragraph each: what it
      buys, what it hides, when you'd recommend it to a customer.
- [ ] Multi-provider reality: port one component from Claude to GPT and Gemini. Note every
      behavioral difference in Field Notes — FDEs at labs compete against the others' models
      and must speak fluently about all of them.

---

## Module 5 exit criteria

- [ ] TicketFlow AI deployed; demo video recorded and linked in portfolio.
- [ ] You can whiteboard the agent loop — including failure handling and stop conditions —
      from memory.
- [ ] Your MCP servers work from a real client (Claude Desktop/Code).
- [ ] You can argue RAG vs fine-tuning vs long-context for a given scenario, with costs.

*Next → [Module 6: Evaluation, Observability & Reliability](06-evals-and-reliability.md)*
