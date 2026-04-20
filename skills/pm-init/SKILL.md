---
description: Initialize the data/ directory tree in a consumer repo with all subfolders and seed index/scaffold files. Idempotent — skips files that already exist. Run once at repo setup, safe to re-run.
---

# PM Init

Scaffolds the `data/` layer so the rest of PM OS (`/log-decision`,
`/log-signal`, `/log-lead`, `/tasks`, `/pipeline`, `/knowledge`, etc.)
has a place to read and write. Creates directories + empty seed files.
**Never** overwrites existing content.

**When to run:**
- Fresh consumer repo that doesn't yet have `data/`.
- Partial tree (some folders exist, some missing) — this fills gaps.

**When NOT to run:**
- Migrating legacy Notion data — use `/migrate-from-notion`, which
  creates the tree *and* populates it.

## Step 1 — Preconditions

1. Confirm the cwd is the consumer repo root (contains `CLAUDE.md`). If
   not, halt: *"Run `/pm-init` from the repo root."*
2. If `data/` already exists and contains any `.md` files beyond the
   seeds this skill writes, confirm before proceeding:
   *"`data/` already has content. I'll only fill missing seeds — nothing
   existing will be touched. Proceed? (y/n)"*

## Step 2 — Create Directories

Create the full tree (ok if they exist):

```
data/
├── signals/
│   └── archive/
├── decisions/
├── knowledge/
│   ├── people/
│   ├── reference/
│   ├── research/
│   └── market-landscape/
├── personas/
├── leads/
│   └── archive/
└── tasks/
```

## Step 3 — Seed Files

For each file: if it exists, **skip** and log it to the summary. Else
write the template below verbatim.

### `data/README.md`

```markdown
# Data

Product memory for this repo. One product per repo — the repo IS the
product. Skills under PM OS read and write these files directly; no
external database.

## Layout

- `signals/active.md` — dated observations (newest first). `archive/YYYY-QN.md` for closed quarters.
- `decisions/` — one file per decision (`YYYY-MM-DD-slug.md`) + `index.md` manifest.
- `knowledge/{people,reference,research,market-landscape}/` — durable synthesized understanding.
- `personas/` — one file per persona + `index.md`.
- `leads/` — pipeline: one file per lead, `index.md` board, `archive/` for Won/Lost.
- `tasks/active.md` (Now / Next / Later) and `tasks/done.md`.

See the plugin's `.claude/context/data-schemas.md` for frontmatter and
file conventions.
```

### `data/signals/active.md`

```markdown
# Active Signals

_Newest first. One H3 per signal. Written by `/log-signal`._
```

### `data/decisions/index.md`

```markdown
# Decisions

| Date | Type | Title | Status | Outcome | File |
|---|---|---|---|---|---|
```

### `data/personas/index.md`

```markdown
# Personas

| Slug | Title | Evidence | Last updated |
|---|---|---|---|
```

### `data/leads/index.md`

```markdown
# Leads

| Status | Company | Contact | Fit | Last Contact | Next Action | File |
|---|---|---|---|---|---|---|
```

### `data/tasks/active.md`

```markdown
# Active Tasks

## Now

## Next

## Later
```

### `data/tasks/done.md`

```markdown
# Done

_Completed tasks, chronological. Written by `/tasks` when items are checked off._
```

Knowledge subfolders intentionally have no index file — glob + frontmatter
is enough, per the data-schema convention.

## Step 4 — Summary

Print:

```
## pm-init — Summary

Directories ensured: {N}
Files created: {M}
Files skipped (already existed): {K}

| File | Result |
|---|---|
| data/README.md | {created|skipped} |
| data/signals/active.md | {created|skipped} |
| data/decisions/index.md | {created|skipped} |
| data/personas/index.md | {created|skipped} |
| data/leads/index.md | {created|skipped} |
| data/tasks/active.md | {created|skipped} |
| data/tasks/done.md | {created|skipped} |
```

## Follow-ups

- Migrating from a legacy Notion setup? → `/migrate-from-notion`
- Starting fresh? → capture the first pieces of state:
  - `/log-decision` for a commitment already made
  - `/log-signal` for a recent observation
  - `/log-lead` for the first prospect in the pipeline
  - `/tasks` to add the current active work

## Anti-Patterns

- **Don't overwrite existing files.** Always check first; skip and log.
- **Don't create `data/` outside the consumer repo root.** If cwd isn't
  the repo root, halt.
- **Don't populate with product data.** This skill is scaffolding only —
  filling it is the job of writer skills (`/log-*`) or
  `/migrate-from-notion`.
- **Don't seed knowledge subfolders with placeholder files.** Empty
  directories are fine; glob handles discovery.
