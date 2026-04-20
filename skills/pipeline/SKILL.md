---
description: Read-only view of the sales pipeline from data/leads/. Groups leads by status, flags overdue follow-ups and stale contacts, and highlights high-fit leads that need attention. Use when asking "what's in my pipeline?" or "who should I follow up with?".
---

# Pipeline

Read-only skill. Never writes to `data/`. Surfaces the current state of
the prospect pipeline so you know exactly where to spend outreach time.

**When to use vs. the alternatives:**

- Use `/pipeline` for a **CRM-style view**: status buckets, overdue
  follow-ups, stale leads.
- Use `/log-interaction` to **record** a follow-up once you've done it.
- Use `/weekly-review` for a broader PM review across decisions,
  signals, and tasks (pipeline is one section there too, but narrower
  here).

## Modes

This skill is read-only but has three view modes. Default is `board`.

- **board** (default) — full pipeline grouped by status. Triggered by:
  "pipeline", "deal flow", "show me my leads".
- **followups** — only leads where `next_action_date` is today or
  overdue. Triggered by: "who should I follow up with", "what's
  overdue", "any follow-ups".
- **stale** — leads where `last_contact` is older than N days
  (default 14) AND status is not `Won`, `Lost`, or `Uncontacted`.
  Triggered by: "who's gone quiet", "stale leads", "who haven't I
  contacted lately".

If the user passes `/pipeline {status}` or mentions a single status
(e.g., "show me qualified leads"), filter the board view to that bucket.

## Before Starting — Self-Hydration

1. Identify the current product (read the host repo's CLAUDE.md, or
   ask).
2. Check that `data/leads/index.md` exists. If not, surface:
   *"No pipeline yet — run `/log-lead` to add your first prospect."*
   Do not invent data.
3. Read `data/leads/index.md`. Parse each row.
4. For `followups` and `stale` modes, compare against today's date
   (from the system context — never guess).

## Framework — Pipeline Health

Use this lens when ranking leads within each status bucket:

1. **Urgency** — is `next_action_date` past, today, or within 2 days?
2. **Fit** — `High` fit leads jump to the top of their bucket.
3. **Staleness** — leads with `last_contact` > 14 days ago get a
   ⚠️ flag (keep as text — `[stale]`).
4. **Stage** — leads further down the pipeline (Demo, Negotiating) are
   more valuable than Uncontacted; surface them first in mixed views.

## Output — Board Mode (default)

```
## Pipeline — {today's date}

**Totals:** {N} active leads | {N_high} high-fit | {N_overdue} overdue | {N_stale} stale

### Negotiating ({count})
- **{Company} — {Contact}** ({fit}) · last: {last_contact} · next: {next_action} ({next_action_date})
  {"[stale]" if last_contact > 14 days} {"[overdue]" if next_action_date past}
  → data/leads/{slug}.md

### Demo ({count})
...

### Qualified ({count})
...

### Responded ({count})
...

### Contacted ({count})
...

### Uncontacted ({count})
...

{Omit Won/Lost from the default board view. Note their counts in
Totals if non-zero:
"**Closed this quarter:** {N_won} won, {N_lost} lost — see
data/leads/archive/ for history."}
```

**Within each bucket:** sort by (1) overdue first, (2) fit High >
Medium > Low, (3) next_action_date ascending. Leads with no
next_action_date sink to the bottom.

## Output — Followups Mode

```
## Follow-ups Due — {today's date}

**{N} leads need action today or are overdue.**

### Overdue ({count})
- **{Company} — {Contact}** ({status}, {fit}) · due: {next_action_date} ({N days late})
  Next: {next_action}
  → data/leads/{slug}.md

### Due Today ({count})
...

### No next_action set ({count})
{Call out leads in active pipeline stages with no next step. These
need a decision: bump the action or mark Lost.}
- **{Company} — {Contact}** ({status}) · last contact: {last_contact}
  → data/leads/{slug}.md
```

## Output — Stale Mode

```
## Stale Leads — {today's date}

**{N} leads haven't been touched in >{threshold} days.**

- **{Company} — {Contact}** ({status}, {fit}) · last: {last_contact} ({N days ago})
  Last next_action: {next_action or "—"}
  → data/leads/{slug}.md

{Sort by days-since-last-contact descending. Highest fit first within
the same age band.}
```

## Follow-ups

Suggest 1–3 contextual next steps based on what the view surfaced:

- If there are **overdue** follow-ups:
  → "Pick the top one and run `/log-interaction` once you've sent the
  follow-up, or bump `next_action_date` if you need more time."
- If there are **stale** High-fit leads:
  → "These are leaking. Run `/log-interaction` with outcome `no-reply`
  and decide: send a break-up email or mark `Lost`."
- If **Uncontacted** > 5:
  → "Backlog's building. Want to add a `/tasks` item to batch 5
  outreach messages?"
- If the pipeline is thin (< 3 active leads across Contacted+):
  → "Pipeline's shallow. Want to run `/market-scan` or
  `/evaluate-opportunity` on a new channel?"

## Anti-Patterns

- **Don't write anything.** This skill is strictly read-only. If the
  user wants to update a lead, route them to `/log-interaction`.
- **Don't open every lead file.** Read `index.md` first and only open
  individual files if the user asks for detail on a specific lead
  (e.g., "what's the history on Acme?").
- **Don't silently hide Won/Lost.** Show the counts in Totals so the
  user sees activity, even if the detail is archived.
- **Don't invent dates.** If `last_contact` or `next_action_date` is
  empty in the index, say so ("no date set") — never guess.
