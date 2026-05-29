---
description: Log a product decision to context/product/decisions.md as an H2 block with inline metadata (type, status, outcome, context, impact) so it can be referenced by future skills.
---

# Log Decision

## Before Starting — Self-Hydration

1. Identify the current product (read CLAUDE.md for Repo Identity, or ask).
2. If the decision was just discussed in this conversation, extract it from
   context.
3. If not, ask the user:
   - What was decided?
   - What's the type? (see list below)
4. Grep `context/product/decisions.md` for `date:` values within the last
   30 days to check for duplicates or related decisions worth linking.

## Decision Structure

This skill appends one H2 block to `context/product/decisions.md`. See
`.claude/context/context-schemas.md` for the full inline metadata schema.

### Required Fields (inline metadata comment)
- **title** — one-sentence description of what was decided.
- **date** — today's date (YYYY-MM-DD).
- **type** — one of: Architecture, Scope, Positioning, Pricing,
  Go-to-Market, Technical, Design, Partnership, Kill/Park.
  (Note: `Insight` is retired. If the user is logging an observation
  rather than a commitment, redirect to `/gtm-log-signal`.)
- **status** — one of: Active, Superseded, Experimental.
- **outcome** — `Pending` by default.
- **agent** — list of agent persona(s) that contributed. Empty `[]` if none.

### Body Sections
- **Context** (H3) — why this decision was made (2-3 sentences). What
  alternatives were considered? What evidence or reasoning drove the choice?
- **Impact** (H3) — what this decision changes or constrains going forward.
- **Outcome Notes** (H3) — left empty initially. Filled in later via
  `/ops-weekly-review`.

### Optional Fields
- **linked_decision** — relative anchor to a prior decision this supersedes
  or builds on (e.g., `context/product/decisions.md#old-slug-YYYY-MM-DD`).
- **linked_signals** — list of relative anchors to signals or feedback that
  informed this decision.

## Writing the Decision

1. Compute the anchor slug from the title: lowercase, spaces → hyphens,
   strip punctuation, append `-YYYY-MM-DD` for uniqueness.
2. Open `context/product/decisions.md`. If the file does not exist, create
   it with a `# Decisions` H1 header.
3. Insert the new H2 block at the **top** of the file (newest first),
   immediately after the H1 header.

```markdown
## {Title} {#slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD type:{Type} status:Active outcome:Pending agent:[] linked_signals:[] linked_decision:null session:pending -->

### Context

{Why this decision was made.}

### Impact

{What this changes or constrains.}

### Outcome Notes

_(Filled in via /ops-weekly-review.)_

---
```

4. The `session:pending` annotation marks this as a session-written block
   awaiting reconciliation by `/ctx-context-sync`.

## Output

Confirm what was logged:

```
## Decision Logged

**Type:** {type}
**Title:** {title}
**Status:** {status}
**Outcome:** Pending
**Agent:** {agent(s) or "none"}
**Written to:** context/product/decisions.md (top of file)
**Anchor:** #{slug-YYYY-MM-DD}
```

## After Completing

Suggest the user might want to:
- Run `/strat-evaluate-opportunity` if this decision opens or closes a product bet
- Run `/strat-write-prd` if this decision defines scope for a new feature
- Run `/disc-break-down` if an existing PRD needs updating based on this decision
