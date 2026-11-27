# Module 0 — Prerequisites & Setup (Weeks 1–2)

> Goal: confirm you can build and ship working software, set up your tooling, and create the
> portfolio scaffolding the rest of the program fills in.

This curriculum does **not** teach programming from zero. If you can't pass the self-assessment
below, spend 2–3 months on fundamentals first (e.g., [Coding Interview University](https://github.com/jwasham/coding-interview-university),
CS50, or *Python Crash Course*), then come back.

---

## Self-assessment — you should be able to do all of these today

- [ ] Write a ~200-line Python program (CLI tool, scraper, small API client) without a tutorial.
- [ ] Explain what an HTTP request is: methods, headers, status codes, JSON bodies.
- [ ] Write a SQL query with a `JOIN`, a `GROUP BY`, and a `WHERE` clause.
- [ ] Use git: branch, commit, push, open a pull request, resolve a simple merge conflict.
- [ ] Read a stack trace and debug your own code with print statements or a debugger.
- [ ] Explain Big-O of a nested loop and of a hash-map lookup.

If you checked 5–6: proceed. 3–4: proceed, but budget extra time in Module 2. 0–2: build
fundamentals first.

---

## Lesson 0.1 — Your two languages

FDE postings overwhelmingly ask for **Python** (the language of LLM tooling and data work) and
strongly prefer a second language, usually **TypeScript** (the language of web frontends, demos,
and much of the MCP ecosystem). You will use both throughout this curriculum.

- [ ] Python: comfortable with virtualenvs (`uv` or `venv`), `pip`, type hints, `dataclasses`,
      `async`/`await` basics, and writing tests with `pytest`.
- [ ] TypeScript: comfortable with `npm`/`pnpm`, basic types/interfaces, `async`/`await`,
      and building a trivial Node script and a trivial React page.

**Resources**
- *Python*: [official tutorial](https://docs.python.org/3/tutorial/), [uv docs](https://docs.astral.sh/uv/)
- *TypeScript*: [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- If new to one of them: 1 week max. You learn languages by building the modules, not upfront.

## Lesson 0.2 — Tooling setup

- [ ] Editor with an AI assistant (VS Code / Cursor / Zed). FDEs are expected to be fast; using
      AI coding tools well is now table stakes — and at the labs, it's part of the job.
- [ ] A terminal you're fluent in: shell basics, `curl`, `jq`, SSH.
- [ ] Docker Desktop (or equivalent) installed and working.
- [ ] Accounts + API keys: **Anthropic API**, **OpenAI API**, **Google AI Studio (Gemini)**.
      Budget $20–50 for the whole program; most modules cost cents.
- [ ] A cloud account with a free tier (AWS, GCP, or Azure — pick one, you'll deploy there in
      Module 2). Also grab a free [Fly.io](https://fly.io)/[Railway](https://railway.app)/[Render](https://render.com)
      account for quick deploys.
- [ ] GitHub profile cleaned up: real name or consistent handle, photo, bio, pinned repos area
      ready. Your GitHub **is** your resume for this role.

## Lesson 0.3 — Portfolio scaffolding

Create a public GitHub repo `fde-portfolio` (or a personal site) with this structure; every
module deliverable gets linked from it:

```
fde-portfolio/
  README.md          <- index of projects, one paragraph + demo link each
  writeups/          <- design memos and decision docs (Module 8 teaches the format)
  demos/             <- links to recorded demos (Loom/YouTube unlisted)
```

- [ ] Repo created with a README skeleton.
- [ ] Write a 5-line "who I am and what I'm building toward" intro. You'll rewrite it in
      Module 10 — that's the point. Keep the first draft.

## Lesson 0.4 — Baseline project (the "hello world" of this program)

Build and deploy a tiny end-to-end app in a weekend. It proves your toolchain works and gives
you a baseline to measure your growth against.

**Build: "Ask My Docs" v0**
- A web page with a text box. User types a question.
- Backend (FastAPI or Express) calls one LLM API with the question plus the contents of 2–3
  Markdown files you wrote, stuffed into the prompt.
- Returns the answer. No RAG, no vector DB, no streaming. Deliberately naive — Module 5 will make
  you rebuild this properly, and the diff is your learning.

**Deliverable checklist**
- [ ] Deployed to a public URL (Fly.io/Railway/Render).
- [ ] Code on GitHub with a README: what it does, how to run it, a screenshot.
- [ ] One paragraph in the README: "What's wrong with this design?" List every weakness you can
      see (cost, latency, context limits, no evals, no auth…). Save it. Compare in Module 6.

---

## Module 0 exit criteria

- [ ] Self-assessment passed.
- [ ] Both API-key providers tested with a `curl` request from your terminal.
- [ ] Baseline project deployed and linked in `fde-portfolio`.

*Next → [Module 1: The FDE Role & Mindset](01-fde-role-and-mindset.md)*
