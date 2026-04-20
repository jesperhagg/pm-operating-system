---
description: Log a product decision to data/decisions/ as a markdown file with structured frontmatter (type, status, outcome, context, impact) so it can be referenced by future skills.
---

# Log Decision

## Before Starting — Self-Hydration

1. Identify the current product (read CLAUDE.md for Repo Identity, or ask).
2. If the decision was just discussed in this conversation, extract it from
   context.
3. If not, ask the user:
   - What was decided?
   - What's the type? (see list below)
4. Read `data/decisions/index.md` (or glob `data/decisions/*.md` if no index)
   for recent decisions in the last 30 days, to check for duplicates or
   related decisions worth linking.

## Decision Structure

This skill writes one file per decision under `data/decisions/`. See
`.claude/context/data-schemas.md` for the full frontmatter schema.

### Required Fields (frontmatter)
- **title** — one-sentence description of what was decided.
- **date** — today's date (YYYY-MM-DD).
- **type** — one of: Architecture, Scope, Positioning, Pricing,
  Go-to-Market, Technical, Design, Partnership, Kill/Park.
  (Note: `Insight` is retired. If the user is logging an observation
  rather than a commitment, redirect to `/log-signal`.)
- **status** — one of: Active, Superseded, Experimental.
- **outcome** — `Pending` by default. Updated later via `/weekly-review`
  to one of: Validated, Invalidated, Inconclusive.
- **agent** — list of agent persona(s) that contributed to this decision
  in the current conversation. Empty list `[]` if no agent involved.

### Body Sections
- **Context** (H2) — why this decision was made (2-3 sentences). What
  alternatives were considered? What evidence or reasoning drove the
  choice?
- **Impact** (H2) — what this decision changes or constrains going
  forward. Reference specific features, flows, or priorities affected.
- **Outcome Notes** (H2) — left empty initially. Filled in later via
  `/weekly-review`.

### Optional Fields
- **linked_decision** (frontmatter) — relative path to a prior decision
  this supersedes or builds on (e.g., `../decisions/2026-03-15-old.md`).
- **linked_signals** (frontmatter) — list of relative paths to signal
  anchors that informed this decision (e.g.,
  `[../signals/active.md#wtp-feedback-2026-04-15]`).

## Writing the Decision

1. Compute the slug from the title: lowercase, spaces → hyphens, strip
   punctuation. Truncate to ~50 chars.
2. Compute the filename: `data/decisions/YYYY-MM-DD-{slug}.md`.
3. If the file already exists (rare, same title same day), append
   `-2`, `-3`, etc. to the slug.
4. Write the file with frontmatter + Context + Impact + empty Outcome
   Notes section.
5. Append a new row to `data/decisions/index.md`. Format:
   `| {date} | {type} | {title} | {status} | Pending | {filename} |`
   Insert in date-descending order (newest first). If the index file does
   not exist, create it with the table header.

## Output

Confirm what was logged:

```
## Decision Logged

**Type:** {type}
**Title:** {title}
**Status:** {status}
**Outcome:** Pending
**Agent:** {agent(s) involved, or "none"}
**Written to:** data/decisions/{filename}
**Index updated:** data/decisions/index.md
```

## After Completing

Suggest the user might want to:
- Run `/evaluate-opportunity` if this decision opens or closes a product bet
- Run `/write-prd` if this decision defines scope for a new feature
- Run `/break-down` if an existing PRD needs updating based on this decision
