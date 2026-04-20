---
description: Log a new prospect or customer to data/leads/ as a markdown file with structured frontmatter (status, contact details, fit, source, next action) and append a row to data/leads/index.md. Use for anyone entering the outbound pipeline.
---

# Log Lead

This skill creates one file per lead under `data/leads/` and keeps the
pipeline board (`data/leads/index.md`) in sync. Use it to add a new
prospect — a person or company you're actively cultivating.

**When to use vs. the alternatives:**

- Use `/log-lead` to add a **new** prospect (any stage from uncontacted
  to first demo).
- Use `/log-interaction` to append an event (sent email, got reply,
  booked demo) to an **existing** lead.
- Use `/knowledge people` for stakeholders you already work with — not
  for cold prospects.
- Use `/log-signal` for aggregate market observations (e.g., "three
  founders asked about pricing this week"), not per-prospect events.

See the **DB Routing Rubric** in `.claude/context/data-schemas.md`.

## Before Starting — Self-Hydration

1. Identify the current product (read the host repo's CLAUDE.md for
   Repo Identity, or ask the user).
2. If the lead was just discussed in this conversation, extract fields
   from context.
3. If not, ask the user (one focused prompt, not a 10-field form):
   - Who? (name + company + role)
   - How did they enter the pipeline? (source: cold-email, referral,
     inbound, event, linkedin, other)
   - Have you contacted them yet? (determines default status)
4. Read `data/leads/index.md` (create it with the table header if
   missing). Grep for the company and contact name to check for
   duplicates. If a match exists, **stop and redirect** to
   `/log-interaction` instead of creating a duplicate file.

## Lead Structure

See `.claude/context/data-schemas.md` for the full schema.

### Required Fields (frontmatter)
- **title** — `{Contact name} — {Company}`.
- **company** — company name (or `""` if individual).
- **contact** — object with `name`, `role`, `email`, `linkedin`. Leave
  missing fields as empty strings rather than inventing values.
- **status** — one of: `Uncontacted`, `Contacted`, `Responded`,
  `Qualified`, `Demo`, `Negotiating`, `Won`, `Lost`. Default:
  `Contacted` if the user already reached out, else `Uncontacted`.
- **source** — one of: `cold-email`, `referral`, `inbound`, `event`,
  `linkedin`, `other`.
- **fit** — `High`, `Medium`, or `Low`. Ask if unclear — don't guess.
- **last_contact** — today's date if the first interaction is also being
  logged now; otherwise empty string.

### Optional Fields (frontmatter)
- **persona** — slug ref to a file in `data/personas/` (e.g.,
  `solo-pm`). Empty string if no persona match.
- **next_action** — short sentence describing the immediate next step.
- **next_action_date** — date by which the next action must happen.
  Null if no dated action pending.
- **tags** — list (industry, stage, segment). Empty list if none.

### Body Sections
- **Interactions** (H2) — append-only event log. Seeded empty, or with
  one H3 if the user is logging first-contact simultaneously.
- **Notes** (H2) — free-form. Start empty or with 1–2 sentences of
  context (pain points heard, budget signals, objections).

## Writing the Lead

1. Compute the slug. Prefer `{company-slug}` (kebab-case). If the lead
   is an individual with no company, use `{name-slug}`. Truncate to
   ~40 chars.
2. Compute the filename: `data/leads/{slug}.md`.
3. If the file already exists, append `-2`, `-3`, etc. (rare — usually
   means there are two contacts at the same company; prefer
   `{company}-{contact-first-name}` in that case).
4. Write the file with frontmatter + empty `## Interactions` section +
   empty `## Notes` section. If the user provided first-contact details
   alongside the lead, seed the Interactions section with a single H3
   entry following the format in `/log-interaction`.
5. Append a row to `data/leads/index.md` in pipeline-status order
   (Uncontacted → Contacted → Responded → Qualified → Demo →
   Negotiating → Won → Lost). Within a status, sort by
   `next_action_date` ascending (empty last). Row format:
   `| {status} | {company} | {contact.name} | {fit} | {last_contact} | {next_action short} | {filename} |`
6. Create `data/leads/index.md` with the table header if missing:
   `| Status | Company | Contact | Fit | Last Contact | Next Action | File |`

## Output

Confirm what was logged:

```
## Lead Logged

**Company:** {company}
**Contact:** {contact.name} ({contact.role})
**Status:** {status}
**Fit:** {fit}
**Source:** {source}
**Next Action:** {next_action or "—"} ({next_action_date or "no date"})
**Written to:** data/leads/{filename}
**Index updated:** data/leads/index.md
```

## Follow-ups

Suggest 1–3 contextual next steps:

- If `status = Uncontacted`:
  → "Want me to add a task to `/tasks` to send first outreach?"
- If `status = Contacted` and no next_action was set:
  → "When should you follow up if no reply? I can set next_action_date
  and add a nudge task."
- If `fit = High` and no persona is linked:
  → "Want to link this lead to a persona in `data/personas/`? Run
  `/knowledge` if you haven't defined one yet."
- If this is the 3rd+ lead from the same source this month:
  → "That channel is producing. Worth logging a signal via
  `/log-signal` (type: `Internal Learning`)?"

## Anti-Patterns

Reject or redirect these inputs rather than creating a lead file:

- **Existing stakeholder, not a prospect** — someone already in
  `data/knowledge/people/`. Redirect to `/knowledge people` for
  profile updates.
- **Aggregate observation** — "three founders asked about pricing."
  Redirect to `/log-signal`.
- **A named persona, not a real person** — redirect to `/define-persona`.
- **Invented contact details** — if the user doesn't know the email or
  LinkedIn, leave fields empty. Never fabricate.
