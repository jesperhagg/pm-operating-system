# CLAUDE.md

## Purpose

This repo is a **product workspace that also hosts the pm-os framework**. It holds, in one place:

- **PM operating system** — skills, agents, and reference docs under `.claude/` that run PM
  workflows (strategy, discovery, GTM, cadence) against product context in `context/` + `tasks/`.
- **Product codebase** — the product's own code, with its coding/architecture guidelines in `docs/`.
  (No product code exists yet; the coding-side docs are scaffolded and ready.)

Two modes of work: **PM workflows** (invoke a skill — see `.claude/skills/README.md`) and
**product development** (follow `docs/engineering.md`). When scope is unclear, read `REPO-MAP.md` first.

## How I work

- Be direct. No preamble, no filler. Default to the next concrete step, not a menu.
- **Think before coding** — state assumptions; surface interpretations and tradeoffs; ask when unclear.
- **Simplicity first** — minimum code that solves it; nothing speculative.
- **Surgical changes** — touch only what the request needs; match existing style; clean up only your own mess.
- **Goal-driven** — turn tasks into verifiable goals; state a brief plan with verify steps, then execute.
- Skills own methodology — when a skill exists, invoke it; don't improvise.
- Delegate to the cheapest capable model (Haiku/Sonnet/Opus). Full rules: `docs/engineering.md`.

**Don't:** write files, create PRs, or take irreversible actions without asking · hardcode product
names/personas/features into skills or agents · recommend capabilities I already have (`REPO-MAP.md`) ·
ask questions inferrable from context.

## Where to look

| Need | Go to |
|---|---|
| Coding principles + subagent delegation | `docs/engineering.md` |
| Product architecture & data flows | `docs/architecture.md` |
| House style / conventions (enforced by `/dev-review-diff`) | `docs/conventions.md` |
| Repo run commands, quirks, hard rules | `docs/agent-playbook.md` |
| How to work with / when to invoke agents | `AGENTS.md` |
| Skill catalog, packages, when-to-run, local testing | `.claude/skills/README.md` |
| Framework (skill/agent) authoring standards + pre-commit checklist | `.claude/context/dev-standards.md` |
| Where product context/data lives + file shapes | `.claude/context/context-schemas.md` (live example: `example/context/`) |
| Observability — automatic skill/agent activity log (audit trail) | `.claude/context/dev-standards.md` (§ Observability Layer); hook: `.claude/hooks/activity-log.sh` |
| Generated routing map of the repo | `REPO-MAP.md` |

## MCP usage

| Server | Used by | If unavailable |
|---|---|---|
| Tavily | `/ops-pm-digest`, `/gtm-market-scan` | Graceful — skip web sections, note limitation |
| Notion | `/ctx-context-sync`, `/ctx-context-init` | Graceful — skip Notion source, note limitation |
| Gmail | `/ctx-context-sync` | Graceful — skip Gmail source, note limitation |

## Constraint Layer

This repo runs on a **constraint layer**: tests, lints, docs, and a review agent that encode "what good looks like" and mechanically reject anything below the bar. The coding agent reads three docs before writing code, in this order:

1. `docs/agent-playbook.md` — how to run, where things live, credentials, quirks, hard rules.
2. `docs/conventions.md` — house style. The review agent uses this as its rubric.
3. `docs/architecture.md` — system shape and hot paths.

> **This repo is dual-purpose.** `/dev-scaffold-constraint-layer` intentionally halts here (it scaffolds *other* product repos), so the Gate was installed by hand: `.github/workflows/ci.yml` (stack-detecting), `.github/workflows/review-agent.yml`, `.github/pull_request_template.md`, and this section. When app code lands, fill the placeholders in `docs/conventions.md` and `docs/architecture.md` so the rubric has teeth.

### The Loop — When the Agent Makes a Mistake

Do not patch the code directly. The fix is two steps, in order:

1. **Encode the constraint first.** Run `/dev-encode-constraint` describing the mistake. The skill outputs the right artifact (regression test, lint rule, conventions paragraph, playbook note, or review-agent prompt) and the exact location.
2. **Apply it, then re-run the original task.** The next attempt is blocked by the constraint, not by a human.

If the mistake was a missing piece of context (where a credential lives, why a script must run twice), use `/dev-agent-playbook-update` so the next session inherits the knowledge.

If you can't write a constraint that catches the class of mistake, write a paragraph in `docs/conventions.md` or `docs/agent-playbook.md`. The repo teaches the agent — the agent doesn't memorize the repo.

### The Gate

- Tests + lints run in CI on every PR. Red CI = blocked merge.
- Every PR must answer: **"What test or constraint prevents this regression?"** If the answer is "none," the work isn't done.
- The review-agent workflow runs `/dev-review-diff` against `docs/conventions.md` and comments findings.

### Identifying a Constraint-Layer Gap

A **gap** is a class of mistake the layer should have caught but didn't — the rubric never encoded the rule. Signals that you've hit one:

- `/dev-review-diff` returns clean but something is still wrong on read.
- The same class of mistake recurs across diffs.
- A bug reaches `main` with green CI.
- A reviewer (human or agent) flags something no test, lint, or convention names.

When you spot one, the gap is in the layer, not the diff: run `/dev-encode-constraint` to add the missing test/lint/convention, then re-run `/dev-review-diff` — the next diff of that class is caught mechanically.
