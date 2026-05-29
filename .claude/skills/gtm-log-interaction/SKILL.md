---
description: Append a dated interaction (email, reply, call, demo, meeting) to an existing lead in context/ops/leads-detail/. Updates last_contact, optionally bumps status and next_action, and keeps context/ops/leads.md in sync.
---

# Log Interaction

This skill appends a single event to an existing lead's `## Interactions`
section and updates the lead's frontmatter (`last_contact`, and optionally
`status` / `next_action` / `next_action_date`). It also re-syncs the row
in `context/ops/leads.md`.

**When to use vs. the alternatives:**

- Use `/gtm-log-interaction` for **per-lead events**: sent email, got reply,
  booked demo, prospect went silent.
- Use `/gtm-log-lead` to create a **new** prospect file.
- Use `/gtm-log-signal` for **aggregate** observations across many leads.

## Before Starting — Self-Hydration

1. Identify the current product (read the host repo's CLAUDE.md, or ask).
2. Identify the target lead. In priority order:
   - If the user named a slug directly, use it.
   - Otherwise read `context/ops/leads.md` and fuzzy-match against
     the user's phrasing. If 1 match: use it. If >1: ask. If 0: redirect
     to `/gtm-log-lead`.
3. Open `context/ops/leads-detail/{slug}.md` and read the current
   frontmatter + existing `## Interactions` section.

## Interaction Structure

Each interaction is one H3 section inside `## Interactions`, newest first.
See `.claude/context/context-schemas.md` for the full format.

### Required Fields
- **date** — the actual event date (not today if logging late).
- **headline** — short verb-led phrase.
- **channel** — one of: `email`, `call`, `linkedin`, `demo`,
  `meeting`, `research`, `other`.
- **outcome** — one of: `sent`, `replied`, `no-reply`, `booked`,
  `cancelled`, `added`, `other`.

### Optional
- **body** — 1–3 sentences of context.

## Status & Next-Action Prompts

After capturing the interaction, ask (one focused question at a time):
- **Status change?** If outcome `replied` → suggest `Contacted → Responded`.
  If `booked` → suggest `Responded → Demo`. If `no-reply` on 3rd+ attempt
  → suggest `→ Lost`. Don't auto-change; confirm.
- **Next action?** Ask: "What's the next step and by when?"

## Writing the Interaction

1. Construct the H3 block:

```markdown
### {YYYY-MM-DD} — {Headline}
<!-- channel:{channel} outcome:{outcome} -->

{Body, if any.}
```

2. Insert at the **top** of `## Interactions` (newest first), after the
   heading and its `<!-- Newest first... -->` comment.
3. Update frontmatter:
   - `last_contact: {event date}` if newer than current value.
   - `status: {new status}` if user confirmed a bump.
   - `next_action` and `next_action_date` if user provided them.
4. Update the matching row in `context/ops/leads.md`:
   - Replace the row's `Status`, `Last Contact`, and `Next Action` columns.
   - Re-sort the row into its new pipeline bucket if status changed.
   - If new status is `Won` or `Lost`, just update the board — no file
     archival yet (handled by `/ctx-context-sync` governance).

## Output

```
## Interaction Logged

**Lead:** {company} — {contact name}
**Event:** {headline} ({channel}, outcome: {outcome})
**Date:** {event date}
**Status:** {old} → {new}  (or just "{status}" if unchanged)
**Last Contact:** {date}
**Next Action:** {next_action or "—"} ({next_action_date or "no date"})
**Written to:** context/ops/leads-detail/{slug}.md
**Board updated:** context/ops/leads.md
```

## Follow-ups

- If `outcome = replied` and status moved to `Responded`:
  → "Want to run `/disc-design-experiment` to structure a discovery call?"
- If `outcome = booked` (demo scheduled):
  → "Add a prep task to `/ops-tasks` for the day before the demo?"
- If `outcome = no-reply` on the 2nd+ follow-up:
  → "Want to mark this lead `Lost`?"
- If this is the 5th+ lead with the same objection this month:
  → "That's a recurring objection. Capture as a signal via `/gtm-log-signal`?"

## Anti-Patterns

- **Duplicate interaction on same day/channel** — check before writing.
- **Inventing a status change** — always confirm with user.
- **Logging aggregate patterns here** — redirect to `/gtm-log-signal`.
- **Writing to a lead that doesn't exist** — redirect to `/gtm-log-lead`.
