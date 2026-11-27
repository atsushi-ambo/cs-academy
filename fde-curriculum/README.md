# FDE Academy — Become a Forward Deployed Engineer

**🌐 言語 / Language: English (this page) ・ [日本語](ja/README.md)**

> A complete, self-paced curriculum for landing a **Forward Deployed Engineer (FDE)** role at
> frontier AI labs (OpenAI, Anthropic, Google), Palantir, and the growing ecosystem of
> AI-deployment companies — built from real job postings and interview loops.

---

## What is a Forward Deployed Engineer?

A Forward Deployed Engineer is a software engineer who **embeds directly inside a customer's
environment** — on-site, in their cloud/VPC, inside their workflows — and ships production
software that solves that customer's specific problem with their company's platform or models.

The role was pioneered at **Palantir** (where FDEs are called "Deltas") and has exploded across
the AI industry: OpenAI, Anthropic, Google, Cohere, Scale AI, Databricks, and many startups now
hire FDEs to turn frontier models into deployed, value-generating systems. Job postings for FDEs
grew **over 800%** between January and September 2025, and in 2026 OpenAI formalized the model at
scale with "The Deployment Company," a deployment-focused joint venture.

**The one-line difference from adjacent roles:**

| Role | Optimizes for |
|---|---|
| Software Engineer | One capability, used by **many** customers |
| Forward Deployed Engineer | Many capabilities, for **one** customer — shipped to *their* production |
| Solutions Architect | Advice, reference architectures, demos (usually doesn't own production code) |
| Consultant | Reports and recommendations (someone else builds it) |
| ML Engineer | Models and training pipelines (usually not customer-facing) |

An FDE **owns implementation**. You write real code that runs in the client's production systems,
and you stay until it works.

### What FDEs actually do (from 2025–2026 job postings)

- Embed with strategic customers to design, build, and deploy **full-stack LLM applications**,
  custom data pipelines, agents, MCP servers, and evaluation harnesses — in production.
- Act as the **primary technical owner** for high-stakes deployments; be the last line of defense
  when production breaks.
- Run **discovery**: map a messy business problem to a buildable, valuable technical solution.
- Communicate with everyone from staff engineers to CISOs to C-suite executives, and hold
  technical boundaries gracefully under pressure.
- Identify **repeatable deployment patterns** and feed them back to product and engineering.
- Operate **autonomously under ambiguity** — often as the only engineer from your company on-site.

### What companies require (composite of OpenAI / Anthropic / Palantir postings)

- Strong programming skills — **Python** plus ideally **TypeScript/JavaScript** or Java — with a
  track record of shipping production applications.
- **Production experience with LLMs**: prompt engineering, agents, RAG, evaluation frameworks,
  deployment at scale.
- Full-stack and data fundamentals: APIs, relational databases (Postgres/MySQL), cloud
  infrastructure, containers.
- Enterprise context: security, privacy, compliance, working inside customer VPCs.
- Exceptional communication: translate complex technical concepts for non-technical audiences,
  brief executives, negotiate scope.
- Bias for action; comfort with travel and with being embedded in someone else's organization.

### Compensation (US, 2025–2026 public ranges)

FDE roles at frontier labs are typically compensated like senior product engineers:
roughly **$200k–$420k+ total compensation** at OpenAI/Anthropic depending on level and location,
with Palantir FDSE ranges somewhat lower at entry level. Treat these as snapshots — always check
current postings.

---

## How this curriculum works

This is a **~29-week program** (10–15 hrs/week part-time; halve it if full-time). It assumes you
can already program in at least one language. Each module has lessons, exercises, deliverables,
and a checklist — like [Coding Interview University](https://github.com/jwasham/coding-interview-university), check items off as you go.

**The golden rule: every module produces an artifact.** FDE hiring is portfolio-heavy. By the end
you will have a public GitHub portfolio of deployed LLM systems, plus the customer-facing skills
the interviews actually test.

### Curriculum map

| Phase | Module | Weeks | Theme |
|---|---|---|---|
| 0 | [Prerequisites & Setup](00-prerequisites.md) | 1–2 | Can you build and ship *anything*? |
| 1 | [The FDE Role & Mindset](01-fde-role-and-mindset.md) | 3 | Understand the job you're training for |
| 2 | [Production Engineering Foundations](02-production-engineering.md) | 4–7 | Full-stack, databases, cloud, Docker, CI/CD |
| 3 | [CS Foundations & System Design](03-cs-and-system-design.md) | 8–10 | DSA, OS/networking/concurrency, architecture & design method |
| 4 | [LLM Fundamentals & Prompt Engineering](04-llm-fundamentals.md) | 11–13 | How models work, how to steer them |
| 5 | [Building LLM Applications: RAG, Tools, Agents, MCP](05-building-llm-applications.md) | 14–18 | The core technical craft of the modern FDE |
| 6 | [Evaluation, Observability & Reliability](06-evals-and-reliability.md) | 19–21 | The #1 differentiator in FDE interviews |
| 7 | [Enterprise Deployment: Security, Privacy, Compliance](07-enterprise-deployment.md) | 22–23 | VPCs, SSO, data governance, the CISO conversation |
| 8 | [Customer Skills: Business, Discovery, Scoping & Executive Communication](08-customer-skills.md) | 24–25 | The rounds that filter out 60% of candidates |
| 9 | [Capstone: Simulated Customer Engagements](09-capstone-projects.md) | 26–28 | Three end-to-end "deployments" for your portfolio |
| 10 | [Interview Preparation & Job Search](10-interview-prep.md) | 29+ | Loop-by-loop prep for OpenAI, Anthropic, Palantir |

### Weekly rhythm

- **~60% building** — the projects are the curriculum; readings support them.
- **~25% study** — papers, docs, courses linked in each module.
- **~15% communication practice** — writing memos, recording demos, explaining decisions out
  loud. This feels optional. It is not. It is the part of the loop most engineers fail.

---

## Who is hiring FDEs (2026)

- **OpenAI** — Forward Deployed Engineer / Forward Deployed Software Engineer (SF, NYC, DC, Tokyo,
  London…), plus "The Deployment Company."
- **Anthropic** — Forward Deployed Engineer (Applied AI), Applied AI Engineer.
- **Google / Google Cloud** — FDE and Applied AI engineering roles around Gemini deployments.
- **Palantir** — Forward Deployed Software Engineer ("Delta") and Forward Deployed AI Engineer.
- **Others** — Cohere, Scale AI, Databricks, Snowflake, Mistral, Glean, Sierra, Decagon, Distyl,
  major consultancies (Deloitte, Accenture) building FDE practices, and most well-funded AI
  application startups.

---

## FAQ

**Do I need a CS degree?** No. You need to demonstrably ship. The portfolio from this curriculum
plus solid CS fundamentals (see [Coding Interview University](https://github.com/jwasham/coding-interview-university) for the deep version)
is the realistic path.

**Do I need ML/research background?** No. FDEs consume models; they don't train them. You need to
deeply understand model *behavior*, context windows, tool use, and evals — not backpropagation.
Module 4 covers exactly the right depth.

**I'm a working SWE — can I skip ahead?** Yes. Take the Phase 0 self-assessment, skim Modules 1–2,
and spend your time on Modules 5–10. The LLM application craft and the customer skills are what you
likely lack.

**How is this different from "AI Engineer" curricula?** Roughly: AI Engineer ⊂ FDE. The FDE role
adds enterprise deployment, customer embedding, discovery/scoping, and executive communication on
top of LLM application engineering. Modules 7–9 are the difference.

---

*Start here → [Module 0: Prerequisites & Setup](00-prerequisites.md)*
