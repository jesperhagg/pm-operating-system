---
description: Initialize the context/ and tasks/ directory tree in a consumer repo with all subfolders, scaffold files, and Notion routing config. Idempotent — skips files that already exist. Replaces /pm-init.
---

# Context Init

Scaffolds the `context/` and `tasks/` layers so the rest of PM OS
(`/log-decision`, `/log-signal`, `/log-lead`, `/tasks`, `/pipeline`,
`/knowledge`, `/context-sync`, etc.) has a place to read and write.
Creates directories + empty seed files + Notion routing config.
**Never** overwrites existing content.

**When to run:**
- Fresh consumer repo that doesn't yet have `context/`.
- Partial tree (some folders exist, some missing) — fills gaps only.
- Before the first run of `/context-sync` — routing config is required.

**When NOT to run:**
- Already have `context/` with content — `/context-sync` keeps it fresh.

## Step 1 — Preconditions

1. Confirm cwd is the consumer repo root (contains `CLAUDE.md`). If not,
   halt: *"Run `/context-init` from the repo root."*
2. Read CLAUDE.md for product name (Repo Identity section). If missing,
   ask the user: *"What product does this repo represent?"*
3. If `context/` already exists with any `.md` files beyond the seeds
   this skill writes, confirm before proceeding:
   *"`context/` already has content. I'll only fill missing seeds — nothing
   existing will be touched. Proceed? (y/n)"*

## Step 2 — Create Directories

Create the full tree (ok if they exist):

```
context/
├── product/
├── market/
│   └── archive/
├── users/
├── ops/
│   └── leads-detail/
├── learnings/
└── audit/
tasks/
```

## Step 3 — Seed Files

For each file: if it exists, **skip** and log it to the summary. Else
write the template below verbatim.

### `context/README.md`

```markdown
# Context

Product context for this repo. One product per repo — the repo IS the
product. PM OS skills read and write these files directly; no external
database.

`INDEX.md` is the machine-facing router (refreshed by `/context-sync`).
Skills consult it first to scope which files to open.

## Layout

- `product/decisions.md` — commitments made (H2 per decision, newest first).
- `product/strategy.md` — positioning, bets, north-star.
- `product/roadmap.md` — committed / next / later.
- `product/experiments.md` — active hypotheses + outcome log.
- `market/landscape.md` — living competitive doc (append-only scans).
- `market/signals.md` — market and competitive observations.
- `users/personas.md` — customer personas (H2 per persona).
- `users/feedback.md` — user-feedback signal stream.
- `users/research.md` — domain research and literature.
- `ops/people.md` — stakeholder profiles.
- `ops/leads.md` — pipeline board.
- `ops/leads-detail/` — one file per lead (append-only interaction log).
- `learnings/<skill>.md` — per-skill accumulated lessons (created on first
  capture by a looped skill).
- `audit/activity-YYYY-MM.jsonl` — automatic activity log (which skill/agent ran,
  what files it touched, when). Machine-written by the `PostToolUse` hook;
  append-only. See `audit/README.md`.

See the plugin's `.claude/context/context-schemas.md` for frontmatter and
file conventions.
```

### `context/INDEX.md`

```markdown
# Context Index

_Machine-facing router. Read this first; open only the file(s) you need.
Anchor lists are refreshed by `/context-sync` — do not hand-edit._

## product/
- `decisions.md` — H2 per decision, newest first. Recent: _(refreshed by `/context-sync`)_
- `strategy.md` — positioning, bets, north-star (living doc).
- `roadmap.md` — Committed / Next / Later.
- `experiments.md` — H2 per experiment.

## market/
- `landscape.md` — competitive snapshot (append-only via `/market-scan`).
- `signals.md` — H3 dated observations. Recent: _(refreshed by `/context-sync`)_
- `archive/` — quarterly rollover from `signals.md`.

## users/
- `personas.md` — H2 per persona.
- `feedback.md` — H3 dated user feedback. Recent: _(refreshed by `/context-sync`)_
- `research.md` — H2 per finding.
- `icp.md` — H2 per ICP (created on first `/ideal-customer-profile` run).

## ops/
- `people.md` — stakeholder profiles.
- `leads.md` — pipeline board.
- `leads-detail/{slug}.md` — per-lead append-only logs.

## learnings/
- `<skill>.md` — per-skill accumulated lessons (created on first capture).
```

### `context/.sync-state.json`

```json
{
  "last_sync": null,
  "sources": {}
}
```

### `context/product/decisions.md`

```markdown
# Decisions

_H2 per decision, newest first. Written by /log-decision._
```

### `context/product/strategy.md`

```markdown
# Strategy

_Positioning, bets, north-star. Updated by /context-sync and in sessions._
```

### `context/product/roadmap.md`

```markdown
# Roadmap

## Committed

## Next

## Later
```

### `context/product/experiments.md`

```markdown
# Experiments

_H2 per experiment, newest first. Written by /log-signal (Internal Learning type)._
```

### `context/market/landscape.md`

```markdown
# Market Landscape

_Living document. New scans append ## Scan — YYYY-MM-DD sections below. Written by /market-scan._
```

### `context/market/signals.md`

```markdown
# Market Signals

_Newest first. One H3 per signal. Market / competitive observations._
```

### `context/users/personas.md`

```markdown
# Personas

_H2 per persona. Written by /define-persona._
```

### `context/users/feedback.md`

```markdown
# User Feedback

_Newest first. One H3 per signal. User feedback and customer observations._
```

### `context/users/research.md`

```markdown
# Research

_H2 per research area. Updated by /knowledge and /context-sync._
```

### `context/ops/people.md`

```markdown
# People

_H2 per stakeholder. Updated by /knowledge and /context-sync._
```

### `context/ops/leads.md`

```markdown
# Leads

| Status | Company | Contact | Fit | Last Contact | Next Action | File |
|---|---|---|---|---|---|---|
```

### `tasks/active.md`

```markdown
# Active Tasks

## Now

## Next

## Later
```

### `tasks/done.md`

```markdown
# Done

_Completed tasks, chronological. Written by /tasks when items are checked off._
```

### `context/audit/README.md`

````markdown
# Activity Audit Trail

Automatic, append-only log of what skills and agents did in this repo. Written by
the `PostToolUse` hook `.claude/hooks/activity-log.sh` — never by hand, never by a
skill. One JSON object per line, in monthly files `activity-YYYY-MM.jsonl`.

## Event shape

```json
{"ts":"2026-05-29T14:03:22Z","session":"<id>","actor":"skill:log-decision",
 "action":"invoke","targets":["context/product/decisions.md"],"tool":"Edit","status":"ok"}
```

- `actor` — `skill:<name>`, `agent:<subagent_type>`, or `tool:<Write|Edit|NotebookEdit>`.
- `action` — `invoke` | `write` | `edit`.
- `targets` — file path(s) touched, when present.
- `session` + `ts` + `targets` correlate a file change back to the skill that made it.

This records *that an action happened*. The *why* lives in content metadata
(`date:`, `source:`, `agent:[]`, `linked_signals:`) inside the files themselves.

## Reading it

```sh
# Everything a given skill did
jq -c 'select(.actor=="skill:log-decision")' audit/activity-*.jsonl
# Everything that touched a file
jq -c 'select(.targets[]? == "context/product/decisions.md")' audit/activity-*.jsonl
# Run volume by actor
jq -r '.actor' audit/activity-*.jsonl | sort | uniq -c | sort -rn
```
````

## Step 4 — Notion Routing Config

Ask: *"Do you have a Notion workspace with existing product data to sync?
(y/n)"*

- **No:** Write `context/.notion-routing.md` with a commented-out template
  and note: *"Edit `.notion-routing.md` before running `/context-sync`."*
  Skip to Step 5.

- **Yes:** Ask the user to provide:
  1. Any relevant Notion database/page names or IDs they want synced.
  2. For each: which `context/` file it should map to.

  If they have DB IDs ready, use them directly. If not, call
  `mcp__notion__search` to locate databases by name and show results for
  the user to confirm.

  Write `context/.notion-routing.md`:

```markdown
# Notion Routing

Maps Notion databases and pages to context/ files.
Consumed by /context-sync during incremental sync.

## Database Mappings

| Notion DB / Page type | Context file | Notion DB ID |
|---|---|---|
| Decisions | context/product/decisions.md | {db-id} |
| Signals | context/market/signals.md | {db-id} |
| User Feedback | context/users/feedback.md | {db-id} |
| Knowledge Base (reference/strategy) | context/product/strategy.md | {db-id} |
| Knowledge Base (research) | context/users/research.md | {db-id} |
| Personas | context/users/personas.md | {db-id} |
| Tasks | tasks/active.md | {db-id} |
| People / Stakeholders | context/ops/people.md | {db-id} |

## Gmail Query Mappings

| Query | Context file |
|---|---|
| `subject:(competitor OR market OR launch)` | context/market/signals.md |
| `subject:(user OR customer OR feedback OR interview)` | context/users/feedback.md |

## Notes

- Add or remove rows as your Notion setup requires.
- DB IDs are 32-character hexadecimal strings from Notion page URLs.
- Gmail queries support standard Gmail search operators.
```

## Step 5 — Summary

```
## context-init — Summary

Directories ensured: {N}
Files created: {M}
Files skipped (already existed): {K}

| File | Result |
|---|---|
| context/README.md | {created|skipped} |
| context/INDEX.md | {created|skipped} |
| context/.sync-state.json | {created|skipped} |
| context/.notion-routing.md | {created|skipped} |
| context/product/decisions.md | {created|skipped} |
| context/product/strategy.md | {created|skipped} |
| context/product/roadmap.md | {created|skipped} |
| context/product/experiments.md | {created|skipped} |
| context/market/landscape.md | {created|skipped} |
| context/market/signals.md | {created|skipped} |
| context/users/personas.md | {created|skipped} |
| context/users/feedback.md | {created|skipped} |
| context/users/research.md | {created|skipped} |
| context/ops/people.md | {created|skipped} |
| context/ops/leads.md | {created|skipped} |
| context/audit/README.md | {created|skipped} |
| tasks/active.md | {created|skipped} |
| tasks/done.md | {created|skipped} |
```

## Follow-ups

- Migrating existing Notion data? → `/context-sync` (runs an initial full
  pull from your Notion workspace using the routing config just written)
- Starting fresh? → capture the first pieces of state:
  - `/log-decision` for a commitment already made
  - `/log-signal` for a recent observation
  - `/log-lead` for the first prospect in the pipeline
  - `/tasks` to add the current active work

## Anti-Patterns

- **Don't overwrite existing files.** Always check first; skip and log.
- **Don't create `context/` outside the consumer repo root.**
- **Don't populate with product data.** Scaffolding only — filling it is
  the job of writer skills (`/log-*`) or `/context-sync`.
- **Don't seed `leads-detail/` with placeholder files.** Empty directory
  is fine; glob handles discovery.
