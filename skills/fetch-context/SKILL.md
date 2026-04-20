---
description: Fetch live product context from the consumer repo's data/ files. Foundation skill used by other PM skills to self-hydrate with decisions, personas, backlog, recent Signals, and Market Landscape entries.
---

# Fetch Product Context

This is a utility skill that loads product context from the consumer
repo's `data/` directory. Other skills call this pattern before doing
their work.

**What this skill reads:**
- `data/decisions/` — commitments the PM has made
- `data/signals/active.md` — recent time-stamped observations
- `data/knowledge/` — people, reference, research, market-landscape
- `data/personas/` — defined customer personas
- `data/tasks/active.md` — active backlog and in-progress work

See the **DB Routing Rubric** in `.claude/context/data-schemas.md` for
what each entity type holds.

## How to Identify the Current Product

1. Read the repo's CLAUDE.md file
2. Look for the "Repo Identity" section
3. Extract the product name
4. If no Repo Identity section exists, ask the user which product they're
   working on. (One product per repo: the repo *is* the product.)

## How to Read Data Files

The consumer repo follows the layout in `.claude/context/data-schemas.md`.
Always read indexes before opening individual files — this keeps token
usage bounded.

### Decisions (always fetch)

1. Read `data/decisions/index.md` (one-line-per-decision table).
2. Filter rows by `Status = Active` and `Date` within the last 90 days
   (extend if thin). Keep all `Status = Active` regardless of age if the
   decision is type Positioning, Pricing, or Architecture (these are
   long-lived constraints).
3. Open the 3–10 most relevant decision files referenced from the index.
4. Summarize: what was decided, when, and any constraints imposed.

If `data/decisions/` does not exist, note it: *"No decisions logged yet
for this product."*

### Personas (fetch when skill needs user context)

1. Read `data/personas/index.md`.
2. Open the primary persona file (or all if multiple are clearly distinct).
3. Extract: who they are, JTBD, pain, evidence strength.

If `data/personas/` is empty, suggest running `/define-persona`.

### Backlog priorities (fetch when skill needs scope context)

1. Read `data/tasks/active.md`.
2. Extract the top 10 items by priority order (Now → Next → Later H2
   sections, in order).
3. Note current phase from the host CLAUDE.md if specified (Explore,
   Validate, Build, Scale).

### Recent Signals (fetch when skill needs market or user-feedback context)

1. Grep `data/signals/active.md` for H3 headings with `date:` metadata
   within the last 30 days (extend to 60 if thin).
2. Group by `type` from the metadata: User Feedback, Technical Constraint,
   Market Signal, Competitive Move, Internal Learning.
3. Highlight any with `action_required:true`.
4. If looking for evaluation context, also note any decisions of type
   `Scope` or `Go-to-Market` from the decisions step.

### Market Landscape (fetch when skill needs competitive context)

1. Glob `data/knowledge/market-landscape/*.md`.
2. Pick the file matching the current product's market category (the file
   name is typically `{market-slug}.md`).
3. Read only the most recent `## Scan — {date}` H2 section, not the full
   file history.
4. If the latest scan is older than 30 days, note it and suggest running
   `/market-scan` to refresh.

If no Market Landscape file exists, note it: *"No prior scans on file —
suggest running /market-scan."*

## Output

Present a brief context summary to the user:
- Product: [name]
- Key decisions: [2-3 bullet summary, cite by file path]
- Persona: [one-line summary]
- Current focus: [phase + top priorities]
- Recent signals: [count by type, highlight any action-required]
- Market scan freshness: [date of last scan, or "none on file"]

This skill can be invoked directly for a quick context briefing, or used
as a foundation step by other skills.
