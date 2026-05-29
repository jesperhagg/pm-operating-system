---
description: Fetch live product context from the consumer repo's context/ files. Foundation skill used by other PM skills to self-hydrate with decisions, personas, backlog, recent signals, and market landscape entries.
---

# Fetch Product Context

This is a utility skill that loads product context from the consumer
repo's `context/` directory. Other skills call this pattern before doing
their work.

**What this skill reads:**
- `context/product/decisions.md` — commitments the PM has made
- `context/market/signals.md` — recent market and competitive observations
- `context/users/feedback.md` — recent user feedback signal stream
- `context/market/landscape.md` — competitive landscape (most recent scan)
- `context/users/personas.md` — defined customer personas
- `tasks/active.md` — active backlog and in-progress work

See the **Context Routing Rubric** in `.claude/context/context-schemas.md` for
what each file holds.

## How to Identify the Current Product

1. Read the repo's CLAUDE.md file
2. Look for the "Repo Identity" section
3. Extract the product name
4. If no Repo Identity section exists, ask the user which product they're
   working on. (One product per repo: the repo *is* the product.)

## How to Read Context Files

The consumer repo follows the layout in `.claude/context/context-schemas.md`.
Read only the sections you need — most files are multi-entry with H2 blocks.
Use grep for metadata filtering before opening full sections.

### Step 0 — Read `context/INDEX.md` first

If `context/INDEX.md` exists, read it before anything else. It is the
machine-facing router refreshed by `/ctx-context-sync` and lists the most
recent anchors per file. Use it to scope which downstream files you actually
need to open for the calling skill's task — open only those.

If `context/INDEX.md` is missing, fall back to the file-by-file procedure
below and note: *"INDEX.md missing — run `/ctx-context-init` and `/ctx-context-sync`
for routed reads."*

### Decisions (always fetch)

1. Grep `context/product/decisions.md` for `status:Active` in H2 metadata
   comments. Collect matching H2 block anchors.
2. Filter to decisions with `date:` within the last 90 days. Keep all
   `status:Active` regardless of age for type:Pricing, type:Positioning,
   or type:Architecture (long-lived constraints).
3. Read the 3–10 most relevant H2 blocks.
4. Summarize: what was decided, when, and any constraints imposed.

If `context/product/decisions.md` does not exist, note it: *"No decisions
logged yet for this product."*

### Personas (fetch when skill needs user context)

1. Grep `context/users/personas.md` for H2 headings.
2. Read the primary persona H2 block(s) — typically the first 1–2.
3. Extract: who they are, JTBD, pain, evidence strength from the metadata
   comment.

If `context/users/personas.md` is empty, suggest running `/strat-define-persona`.

### Backlog priorities (fetch when skill needs scope context)

1. Read `tasks/active.md`.
2. Extract the top 10 items by priority order (Now → Next → Later H2
   sections, in order).
3. Note current phase from the host CLAUDE.md if specified (Explore,
   Validate, Build, Scale).

If `tasks/governance.md` exists, grep for open items (`^- \[ \]`) and
note the count: *"{N} governance tasks await resolution."*

### Recent Signals (fetch when skill needs market or user-feedback context)

1. Grep `context/market/signals.md` for H3 headings with `date:` metadata
   within the last 30 days (extend to 60 if thin).
2. Grep `context/users/feedback.md` for the same date range.
3. Group by `type` from the metadata.
4. Highlight any with `action_required:true`.

### Market Landscape (fetch when skill needs competitive context)

1. Read `context/market/landscape.md`.
2. Find the most recent `## Scan — {date}` H2 section. Read only that
   section, not the full file history.
3. If the latest scan is older than 30 days, note it and suggest running
   `/gtm-market-scan` to refresh.

If no landscape file or no scans exist, note it: *"No prior scans on
file — suggest running /gtm-market-scan."*

## Output

Present a brief context summary to the user:
- Product: [name]
- Key decisions: [2-3 bullet summary, cite by H2 anchor]
- Persona: [one-line summary]
- Current focus: [phase + top priorities]
- Recent signals: [count by type, highlight any action-required]
- Market scan freshness: [date of last scan, or "none on file"]
- Governance tasks: [count if any open, or "none"]

This skill can be invoked directly for a quick context briefing, or used
as a foundation step by other skills.
