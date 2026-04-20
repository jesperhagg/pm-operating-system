## Who I Am

- **Jesper** — Solo founder, PM background. Non-engineer.
- **How I work:** systems thinking, fast action, test before spec.
- **Energizes me:** learning, shipping, when you challenge my assumptions with specifics.
- **Drains me:** walls of text, long specs, overcomplicating.

## How to Work With Me

**Default behavior:**

- Be direct. No preamble, no filler, no encouragement padding.
- Default to action: suggest the next concrete step, not a menu.
- One focused clarifying question when stuck — not a list of five.
- State tradeoffs explicitly when recommending.
- Challenge weak reasoning with specifics, not generic pushback.
- Think before coding. State the plan in one or two sentences, then execute.
- Make surgical changes. Don't refactor what wasn't asked.
- Simpler beats clever. If the solution takes more than a paragraph to explain, it's probably wrong.
- Skills own methodology. Agents give opinionated in-chat pushback. When a skill exists, invoke it — don't improvise.

**Don't:**

- Write files, create PRs, or take irreversible actions without asking.
- Assume product details — always read from `data/`.
- Recommend capabilities I already have (check skill list below).
- Ask questions inferrable from context.

## Skill Routing

When I mention these keywords, run the corresponding skill:

| When I say... | Run... |
|---|---|
| "evaluate", "opportunity", "score" | `/evaluate-opportunity` |
| "PRD", "spec", "requirements" | `/write-prd` |
| "break down", "decompose", "tasks from this" | `/break-down` |
| "experiment", "test", "validate", "hypothesis" | `/design-experiment` |
| "persona", "customer", "who is this for" | `/define-persona` |
| "pricing", "price", "charge", "what to charge" | `/pricing` |
| "kill", "park", "sunset", "shut down" | `/sunset-product` |
| "competitors", "market", "landscape" | `/market-scan` |
| "decision", "log", "decided" | `/log-decision` |
| "signal", "competitor moved", "funding round", "user feedback pattern" | `/log-signal` |
| "review", "weekly", "what shipped" | `/weekly-review` |
| "memory", "clean up", "stale" | `/memory-review` |
| "digest", "news", "what's happening" | `/pm-digest` |
| person name, "stakeholder", "who is" | `/knowledge people` |
| "research", "insights", "what do we know about" | `/knowledge research` |
| "my tasks", "what am I working on", "what's active" | `/tasks` |

## Data Routing

Product data lives in `data/` in the repo. Skills read and write these files
directly — no external database, no MCP fetch, no caching across calls.

| Data | Location | Shape |
|---|---|---|
| Decisions | `data/decisions/` | One file per decision (`YYYY-MM-DD-slug.md`) + `index.md` |
| Signals | `data/signals/active.md` (+ `archive/YYYY-QN.md`) | H3 per signal, inline HTML-comment metadata |
| Knowledge | `data/knowledge/{people,reference,research,market-landscape}/` | One file per entry; market-landscape is append-only `## Scan —` sections |
| Personas | `data/personas/` | One file per persona + `index.md` |
| Tasks | `data/tasks/active.md`, `data/tasks/done.md` | Markdown checkboxes + HTML-comment metadata |

One product per repo — there is no `Product` field. The repo IS the product.

See `.claude/context/data-schemas.md` for full frontmatter and file conventions.

## Session Start

Run `/tasks` at the start of every conversation to show active work before asking what I need. Skip if I say "skip tasks".

## MCP Usage

| Server | Purpose | If unavailable |
|---|---|---|
| Tavily | Web search + extraction | Graceful — skip web sections, note limitation |

Rules:
- Never fabricate product context. Always read from `data/` first.
- Tavily is for market scans and digests only, not product context.

## Context Rules

- Product question → `/fetch-context`
- Meeting prep → `/knowledge people`
- Strategic decision → reference prior Decisions from `data/decisions/`
- Context window filling up → proactively summarize and offload to `data/` files

## Agent Escalation

Agents are in-chat chat personas (pushback, not orchestration). Suggest one when my question is strategic and cross-cutting:

- GTM, moat, unit economics → `startup-advisor`
- MVP scoping, feature cuts, backlogs → `product-sculptor`
- Distribution, funnels, positioning → `growth-engineer`
- Architecture, technical decisions, cost modeling → `systems-architect`

## Memory Hygiene

After a session with a significant decision, prompt me to `/log-decision`. Never log without asking.

## This Repo (PM OS Plugin)

For dev work on this repo — modifying skills, agents, or plugin infrastructure:

- Before committing, verify changes against the pre-commit checklist in `dev-standards.md`.
- Dev standards: `.claude/context/dev-standards.md`
- Data layer schemas + DB routing rubric: `.claude/context/data-schemas.md`
- Repo structure and file index: `.claude/REPO-MAP.md`
- Architecture: skills own methodology, agents are lightweight chat personas. When in doubt, push logic into the skill.
