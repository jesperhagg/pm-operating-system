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
