---
description: Run a weekly review — single-product (default) or portfolio (across repo paths). Reads decisions, signals, and tasks from data/ and produces a one-page focus plan.
---

# Weekly Review

## Modes

### Single-product (default)
Runs in the current repo. One product per repo.

### Portfolio
User provides a list of repo paths. Runs the review per repo and rolls up a
portfolio summary. Trigger: user says "portfolio review" or passes a list of
paths.

## Before Starting — Self-Hydration

For each repo in scope:

1. Read `CLAUDE.md` for repo identity (product name, bet stage).
2. Read:
   - `data/decisions/index.md` — filter rows where `date` is within the last 7 days. Open those decision files for "What shipped / decided" context.
   - `data/decisions/index.md` — filter rows where `outcome: Pending` AND `date` older than 14 days (the "pending outcome review" backlog).
   - `data/decisions/index.md` — filter rows where `outcome_date` is within the last 7 days (outcomes just assessed).
   - `data/tasks/active.md` — top 5 items by priority from Now → Next.
   - `data/tasks/done.md` — items with `done:` date within last 7 days (what shipped).
   - Grep `data/signals/active.md` for entries with `action_required:true` across all dates.
   - Grep `data/signals/active.md` for entries with `date:` in the last 7 days, grouped by `type:`.
3. Read `.claude/memory/shared.md` for cross-agent learnings relevant to this week (optional — skip if empty).
4. Note today's date for the review header.

If `data/` does not exist in a repo, note it in the review and skip that repo.

## Review Framework

### Per Product (repeat for each repo)

#### What Shipped
- Pull from `data/tasks/done.md` lines with `done:YYYY-MM-DD` in the last 7 days.
- Pull from `data/decisions/` files created in the last 7 days.
- If nothing shipped, say so plainly — no spin.

#### What's Blocked
- Scan `data/tasks/active.md` for lines with non-empty `blocker:"..."` metadata.
- For each blocker: note what's needed to unblock, and who/what can provide it.
- Flag any blocker older than 2 weeks as "stale blocker" (heuristic: check git log on the file if needed).

#### What's Next
- Top 1–2 priorities for the coming week from `data/tasks/active.md` Now section.
- Each priority should be concrete enough to start immediately.

#### Decision Outcomes Updated
- Decisions where `outcome:` is not `Pending` and `outcome_date:` is within the last 7 days.
- List each with the original `date` and the outcome assessment. If none, note: *"No decision outcomes assessed this week."*

#### Pending Outcome Review
- Decisions with `outcome: Pending` older than 14 days.
- If 3+ are pending, prompt: *"These decisions are still awaiting outcome assessment: [list top 5]. Want to update any now?"* (Updates edit the frontmatter `outcome:` / `outcome_date:` of the decision file.)

#### Action-Required Signals
- All H3 blocks in `data/signals/active.md` with `action_required:true`.
- Group by `type:`.
- For each: show headline, date, source, implication.
- Flag signals outstanding 14+ days as "stale — triage now."
- Prompt: *"Which should we act on this week? I can convert any into a decision via `/log-decision` or clear the action_required flag."*

#### Focus Score
Rate this week's focus:
- **Active** — meaningful progress (≥1 shipped task OR ≥1 decision made)
- **Maintenance** — kept alive (tasks updated but nothing shipped)
- **Drifting** — no activity in 7+ days (needs a decision: continue or park)

### Portfolio Level (portfolio mode only)

#### Cross-Product Patterns
- Shared blockers, recurring themes in signals, or resource conflicts.
- Flag if attention is unevenly distributed.

#### Top Priority This Week (Portfolio)
The single most important thing across all products.

## Output

### Single-product output

```
# Weekly Review — {product} — {date}

## Shipped
- [items or "nothing"]

## Blocked
- [items or "none"]

## Next week
- [1-2 priorities]

## Decision Outcomes Updated
- [list or "none"]

## Pending Outcome Review
- [list if 3+]

## Action-Required Signals
- [grouped by type]

## Focus Score: {Active | Maintenance | Drifting}
```

### Portfolio output

```
# Portfolio Weekly Review — {date}

## {Product 1} ({repo path})
[per-product block]

## {Product 2} ({repo path})
[per-product block]

## Portfolio Summary
- Focus scores: {Product 1} [Active] | {Product 2} [Drifting] | ...
- Cross-product patterns: [if any]
- Top priority this week: [single most important thing]
```

## After Completing

Suggest the user might want to:
- Run `/log-decision` to record any decisions made during the review.
- Run `/memory-review` if files are getting long.
- Consult the **startup-advisor** agent if portfolio balance needs rethinking.
- For Drifting products: `/sunset-product` to park or kill.
