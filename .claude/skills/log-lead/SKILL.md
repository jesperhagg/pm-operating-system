---
description: Log a new prospect or customer to context/ops/leads-detail/ as a markdown file with structured frontmatter (status, contact details, fit, source, next action) and append a row to context/ops/leads.md. Use for anyone entering the outbound pipeline.
---

# Log Lead

This skill creates one file per lead under `context/ops/leads-detail/` and
keeps the pipeline board (`context/ops/leads.md`) in sync. Use it to add a
new prospect — a person or company you're actively cultivating.

**When to use vs. the alternatives:**

- Use `/log-lead` to add a **new** prospect.
- Use `/log-interaction` to append an event to an **existing** lead.
- Use `/knowledge people` for stakeholders you already work with — not cold prospects.
- Use `/log-signal` for aggregate market observations across many leads.

See the **Context Routing Rubric** in `.claude/context/context-schemas.md`.

## Before Starting — Self-Hydration

1. Identify the current product (read the host repo's CLAUDE.md, or ask).
2. If the lead was just discussed in this conversation, extract fields.
3. If not, ask the user (one focused prompt):
   - Who? (name + company + role)
   - How did they enter the pipeline? (source)
   - Have you contacted them yet? (determines default status)
4. Read `context/ops/leads.md` (create it with the table header if
   missing). Grep for the company and contact name to check for duplicates.
   If a match exists, **stop and redirect** to `/log-interaction`.

## Lead Structure

See `.claude/context/context-schemas.md` for the full schema.

### Required Fields (frontmatter)
- **title** — `{Contact name} — {Company}`.
- **company** — company name (or `""` if individual).
- **contact** — object with `name`, `role`, `email`, `linkedin`.
- **status** — one of: `Uncontacted`, `Contacted`, `Responded`,
  `Qualified`, `Demo`, `Negotiating`, `Won`, `Lost`.
- **source** — one of: `cold-email`, `referral`, `inbound`, `event`,
  `linkedin`, `other`.
- **fit** — `High`, `Medium`, or `Low`.
- **last_contact** — today's date if first interaction is being logged now.

### Optional Fields
- **persona** — slug ref to a persona anchor in `context/users/personas.md`.
- **next_action** — short sentence describing the immediate next step.
- **next_action_date** — YYYY-MM-DD or null.
- **tags** — list.

## Writing the Lead

1. Compute the slug from the company name (kebab-case, ~40 chars max).
   If individual with no company, use name slug.
2. Compute the filename: `context/ops/leads-detail/{slug}.md`.
3. If the file exists, append `-2`, `-3`, etc.
4. Write the file with frontmatter + empty `## Interactions` section +
   empty `## Notes` section. If the user provided first-contact details,
   seed Interactions with a single H3 entry per the format in
   `/log-interaction`.
5. Append a row to `context/ops/leads.md` in pipeline-status order.
   Row format:
   `| {status} | {company} | {contact.name} | {fit} | {last_contact} | {next_action short} | leads-detail/{filename} |`
6. Create `context/ops/leads.md` with the table header if missing:
   `| Status | Company | Contact | Fit | Last Contact | Next Action | File |`

## Output

```
## Lead Logged

**Company:** {company}
**Contact:** {contact.name} ({contact.role})
**Status:** {status}
**Fit:** {fit}
**Source:** {source}
**Next Action:** {next_action or "—"} ({next_action_date or "no date"})
**Written to:** context/ops/leads-detail/{filename}
**Board updated:** context/ops/leads.md
```

## Follow-ups

- If `status = Uncontacted`:
  → "Want me to add a task to `/tasks` to send first outreach?"
- If `status = Contacted` and no next_action set:
  → "When should you follow up if no reply? I can set next_action_date."
- If `fit = High` and no persona linked:
  → "Want to link this lead to a persona? Run `/define-persona` if needed."
- If this is the 3rd+ lead from the same source this month:
  → "That channel is producing. Worth logging a signal via `/log-signal`?"

## Anti-Patterns

- **Existing stakeholder, not a prospect** — redirect to `/knowledge people`.
- **Aggregate observation** — redirect to `/log-signal`.
- **A named persona, not a real person** — redirect to `/define-persona`.
- **Invented contact details** — leave fields empty. Never fabricate.
