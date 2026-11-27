# Module 2 — Production Engineering Foundations (Weeks 4–7)

> Goal: be able to design, build, deploy, and debug a full-stack application with a real
> database, in a container, on a cloud — alone. This is the floor for every FDE posting.

FDE coding interviews are **practical**, not LeetCode-heavy: build a working thing, integrate an
API, debug a broken service, design a data pipeline. This module is structured as one continuous
project with weekly layers.

**The running project: "TicketFlow"** — a small internal-tools app (support-ticket tracker) that
you will later (Module 5) retrofit with AI. Internal tools are the bread and butter of real FDE
work.

---

## Week 4 — Backend & API design

- [ ] Build a REST API with **FastAPI** (Python) — tickets CRUD, users, comments.
- [ ] Proper structure: routers, services, models; Pydantic validation on every boundary.
- [ ] Auth: session or JWT login. Understand *why* JWTs are stateless and what that costs.
- [ ] Pagination, filtering, error envelope, request logging middleware.
- [ ] Write `pytest` integration tests against a test database.

**Study**
- [ ] [FastAPI docs](https://fastapi.tiangolo.com/) — read "Tutorial – User Guide" fully.
- [ ] REST design: read [Zalando's API guidelines](https://opensource.zalando.com/restful-api-guidelines/) (skim, keep as reference).
- [ ] HTTP deeply: idempotency, caching headers, content negotiation, streaming responses
      (you'll stream tokens constantly in Modules 5+).

## Week 5 — Databases (Postgres is named in OpenAI's posting; take the hint)

- [ ] Model TicketFlow in **Postgres**: schema design, foreign keys, indexes, constraints.
- [ ] Hand-write the 10 most useful queries (joins, aggregates, window function for "tickets
      per agent per week"). No ORM for this exercise; then add SQLAlchemy and compare.
- [ ] Use `EXPLAIN ANALYZE` on a slow query; add an index; measure the difference.
- [ ] Migrations with Alembic. Practice a zero-downtime column rename (expand → migrate →
      contract).
- [ ] Know when you'd reach for: Redis (cache/queues), SQLite (embedded/edge), a document DB,
      a vector DB (preview of Module 5), a data warehouse (BigQuery/Snowflake — enterprises
      live in these).

**Study**
- [ ] [Use The Index, Luke](https://use-the-index-luke.com/) — chapters 1–3.
- [ ] Transactions & isolation levels — read the Postgres docs chapter; be able to explain a
      lost update and how `SELECT ... FOR UPDATE` prevents it.

## Week 6 — Frontend, integration glue & data pipelines

FDEs ship demos and internal UIs constantly; "good enough, fast" is the bar.

- [ ] Build the TicketFlow UI in **React + TypeScript** (Vite): list, detail, create, comment.
- [ ] Streaming-friendly data fetching (you'll reuse this for token streaming): `fetch` +
      `ReadableStream` or SSE.
- [ ] Learn one component kit (shadcn/ui or MUI) — speed matters more than originality.

**Integration glue — the secret half of FDE work.** Enterprise problems are mostly "system A
must talk to system B."
- [ ] Write a pipeline that ingests a messy CSV export (invent one: 50k rows, broken encodings,
      duplicate keys, inconsistent dates) into Postgres: validate → normalize → upsert →
      report rejects. Make it idempotent and re-runnable.
- [ ] Consume a webhook (e.g., GitHub webhook → ticket auto-created) and call a third-party
      API with retries + exponential backoff + timeout budget.

## Week 7 — Containers, cloud, CI/CD, observability

- [ ] Dockerize backend + frontend; `docker compose up` runs the whole stack with Postgres.
- [ ] Deploy to your cloud account: one managed path (Cloud Run / App Runner / Azure Container
      Apps) **and** understand the VPC story (Module 7 deepens this): what's a subnet, security
      group, private vs public endpoint.
- [ ] GitHub Actions: lint + tests on PR, build + deploy on merge to main.
- [ ] Observability floor: structured JSON logs, a `/healthz` endpoint, error tracking (Sentry
      free tier), and one dashboard (request rate, p95 latency, error rate).
- [ ] Practice debugging under pressure: have a friend (or yourself via a script) break the
      deployed app three ways — bad env var, exhausted DB connections, a dependency outage —
      and fix each from logs alone. Time yourself. This simulates the FDE on-call reality.

**Study**
- [ ] [The Twelve-Factor App](https://12factor.net/) — all of it; it's short.
- [ ] Designing Data-Intensive Applications (Kleppmann), ch. 1–3 — read; ch. 5, 7 — skim.
      The vocabulary (replication, partitioning, transactions) comes up in FDE system design.

---

## Module 2 deliverable

**TicketFlow shipped**: public URL, README with architecture diagram (use Mermaid), CI badge,
and a `writeups/ticketflow-design.md` covering: schema decisions, one performance fix with
numbers, one thing you'd do differently. Link from portfolio.

## Module 2 exit criteria (mock-interview yourself, out loud)

- [ ] "Walk me through what happens when a user submits a ticket" — from browser to disk and back.
- [ ] "Your app is suddenly slow. Go." — articulate a real debugging tree.
- [ ] "Why Postgres and not MongoDB here?" — argue it with trade-offs, not tribalism.

*Next → [Module 3: CS Foundations & System Design](03-cs-and-system-design.md)*
