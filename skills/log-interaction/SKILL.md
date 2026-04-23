---
description: Append a dated interaction (email, reply, call, demo, meeting) to an existing lead in data/leads/. Updates last_contact, optionally bumps status and next_action, and keeps data/leads/index.md in sync.
---

# Log Interaction

This skill appends a single event to an existing lead's `## Interactions`
section and updates the lead's frontmatter (`last_contact`, and
optionally `status` / `next_action` / `next_action_date`). It also
re-syncs the row in `data/leads/index.md`.

**When to use vs. the alternatives:**

- Use `/log-interaction` for **per-lead events**: sent email, got reply,
  booked demo, prospect went silent, price objection raised.
- Use `/log-lead` to create a **new** prospect file.
- Use `/log-signal` for **aggregate** observations across many leads
  ("three prospects asked about pricing this week").

## Before Starting — Self-Hydration

1. Identify the current product (read the host repo's CLAUDE.md, or
   ask).
2. Identify the target lead. In priority order:
   - If the user named a slug directly, use it.
   - Otherwise read `data/leads/index.md` and fuzzy-match against
     the user's phrasing (company name or contact first/last name).
     If 1 match: use it. If >1 match: ask the user to pick. If 0
     matches: ask — and redirect to `/log-lead` if this is actually
     a new prospect.
3. Open the matched lead file and read the current frontmatter +
   existing `## Interactions` section (so we know last_contact and
   can avoid duplicate entries on the same date/channel).

## Interaction Structure

Each interaction is one H3 section inside `## Interactions`, newest
first. See `.claude/context/data-schemas.md` for the full format.

### Required Fields (from user or context)
- **date** — date the event happened (the actual event date, NOT
  today if they're logging late).
- **headline** — short verb-led phrase: "Sent cold email", "Got
  reply — interested", "Demo booked for 2026-04-25", "No reply to
  3rd follow-up".
- **channel** — one of: `email`, `call`, `linkedin`, `demo`,
  `meeting`, `research`, `other`.
- **outcome** — one of: `sent`, `replied`, `no-reply`, `booked`,
  `cancelled`, `added`, `other`.

### Optional
- **body** — 1–3 sentences of context: what was said, what you learned,
  what they objected to. Leave blank if the headline tells the whole
  story.

## Status & Next-Action Prompts

After capturing the interaction, ask (one focused question, not all at
once — only prompt if the interaction suggests a change):

- **Status change?** If the outcome is `replied`, suggest bumping
  `Contacted → Responded`. If `booked`, suggest `Responded → Demo`.
  If `cancelled` or `no-reply` on the 3rd+ attempt, suggest
  `→ Lost`. Don't auto-change; confirm with the user.
- **Next action?** Ask: "What's the next step and by when?" Update
  `next_action` (short sentence) and `next_action_date` (YYYY-MM-DD
  or null).

## Writing the Interaction

1. Construct the H3 block:

   ```markdown
   ### {YYYY-MM-DD} — {Headline}
   <!-- channel:{channel} outcome:{outcome} -->

   {Body, if any.}
   ```

2. Insert it at the **top** of the `## Interactions` section (newest
   first), immediately after the `## Interactions` heading and its
   `<!-- Newest first... -->` comment.
3. Update frontmatter in place:
   - `last_contact: {event date}` (only if the event date is newer
     than the current value).
   - `status: {new status}` if the user confirmed a bump.
   - `next_action: "{...}"` and `next_action_date: {YYYY-MM-DD or null}`
     if the user provided them.
4. Update the matching row in `data/leads/index.md`:
   - Replace the row's `Status`, `Last Contact`, and `Next Action`
     columns with the new values.
   - If status changed, re-sort the row into its new pipeline bucket
     (Uncontacted → … → Lost). Keep sort-by-next_action_date asc within
     a bucket.
   - If the new status is `Won` or `Lost`, **do not archive yet** —
     just update the index. `/memory-review` handles file moves to
     `data/leads/archive/`.

## Output

Confirm what was logged:

```
## Interaction Logged

**Lead:** {company} — {contact name}
**Event:** {headline} ({channel}, outcome: {outcome})
**Date:** {event date}
**Status:** {old} → {new}   (or just "{status}" if unchanged)
**Last Contact:** {date}
**Next Action:** {next_action or "—"} ({next_action_date or "no date"})
**Written to:** data/leads/{slug}.md (top of Interactions)
**Index updated:** data/leads/index.md
```

## Follow-ups

Suggest 1–3 contextual next steps:

- If `outcome = replied` and status just moved to `Responded`:
  → "Want to run `/design-experiment` to structure a discovery call,
  or draft an answer with the context in this lead file?"
- If `outcome = booked` (demo scheduled):
  → "Add a prep task to `/tasks` for the day before the demo?"
- If `outcome = no-reply` on the 2nd+ follow-up:
  → "Want to mark this lead `Lost` and note the reason in `## Notes`?"
- If this is the 5th+ lead with the same objection logged in `## Notes`
  this month:
  → "That's a recurring objection. Worth capturing as a signal via
  `/log-signal` (type: `User Feedback`)?"

## Anti-Patterns

- **Creating a duplicate interaction on the same day/channel** — if
  the last existing H3 matches today's date and channel, ask before
  writing. Likely the user meant to edit, not append.
- **Inventing a status change** — don't bump status without user
  confirmation. Status drives pipeline decisions.
- **Logging aggregate patterns here** — if the event is "three
  prospects said the same thing," redirect to `/log-signal`.
- **Writing to a lead that doesn't exist** — redirect to `/log-lead`
  instead of creating the file from this skill.
