---
description: Run a portfolio-level weekly review across all products. Reads memory, backlog, and recent decisions from Notion, then produces a one-page weekly focus plan.
---

# Weekly Review

## Before Starting — Self-Hydration

1. Read the host repo's `CLAUDE.md` to identify the current product(s)
2. Use **Notion MCP** to fetch context for each product in the portfolio:
   - Decisions from the last 7 days (Decisions database)
   - Top 5 backlog items by priority (Task Management database)
   - All rows from the **Signals** database with `Action Required = true`
     (across all dates, not just last 7 days — these are the outstanding
     observations that need PM response)
   - New Signals logged in the last 7 days grouped by `Type`
   - Open questions and pending outcomes from Decisions
3. Read `.claude/memory/shared.md` for cross-product patterns and any
   Signals (Notion fallback) entries that need syncing
4. Note today's date for the review header

## Review Framework

Produce the weekly review using this structure:

### Per Product (repeat for each active product)

#### What Shipped
- List concrete deliverables completed this week
- Reference decisions or backlog items that were resolved
- If nothing shipped, say so plainly — no spin

#### What's Blocked
- List blockers, unresolved questions, or stalled work
- For each blocker, note: what's needed to unblock, and who/what can provide it
- Flag any blocker older than 2 weeks as "stale blocker"

#### What's Next
- Top 1-2 priorities for the coming week
- These should be pulled from the Notion backlog or from unblocked items
- Each priority should be concrete enough to start immediately

### Portfolio Level

#### Agent Interactions This Week
- Query the Decisions database for entries created in the last 7 days that
  have the `Agent` property set.
- Summarize in a table: which agents contributed, how many decisions they
  were involved in, and the key topics.
- If no agent interactions occurred, note: "No agent-assisted decisions
  this week."

#### Decision Outcomes Updated
- Query the Decisions database for entries where `Outcome` was changed from
  `Pending` to `Validated`, `Invalidated`, or `Inconclusive` in the last
  7 days.
- List each with the original decision date and outcome assessment.
- If no outcomes were updated, note: "No decision outcomes assessed this
  week."

#### Pending Outcome Review
- Query decisions with `Outcome: Pending` older than 14 days.
- If 3+ are pending, prompt: "These decisions are still awaiting outcome
  assessment: [list top 5]. Want to update any of them now?"

#### Action Required Signals
- Query the Signals database for all rows with `Action Required = true`,
  across all products and dates.
- Group by Product, then by Type.
- For each signal, show: headline, date, source, implication.
- If any signals have been outstanding for 14+ days, flag them as
  "stale — triage now."
- After listing, prompt: "Which of these should we act on this week?
  I can convert any of them into a decision via `/log-decision` or
  clear the Action Required flag in Notion."

#### Cross-Product Patterns
- Note any patterns spanning products (shared blockers, resource conflicts,
  similar learnings)
- Flag if attention is unevenly distributed (one product getting all focus
  while others drift)

#### Focus Score
Rate this week's focus for each product:
- **Active** — meaningful progress made
- **Maintenance** — kept alive but no forward motion
- **Drifting** — no attention, needs a decision (continue or park)

## Output

```
# Weekly Review — {date}

## {Product 1}
### Shipped: [items or "nothing"]
### Blocked: [items or "none"]
### Next week: [1-2 priorities]

## {Product 2}
### Shipped: [items or "nothing"]
### Blocked: [items or "none"]
### Next week: [1-2 priorities]

(repeat for each product in the portfolio)

## Portfolio
### Focus scores: {Product 1} [X] | {Product 2} [X] | ...
### Cross-product patterns: [if any]
### Top priority this week: [single most important thing across all products]

## Agent Activity
### Agent interactions: [table of agent | decisions | topics]
### Decision outcomes: [list of decisions with outcomes updated, or "none"]
### Pending outcome review: [decisions awaiting outcome assessment, if 3+]
```

## After Completing

Suggest the user might want to:
- Run `/log-decision` to record any decisions made during the review
- Run `/memory-review` if memory files are getting long
- Consult the **startup-advisor** agent if portfolio balance needs rethinking
- Save the review to memory: offer to log key insights to Notion via
  `/log-decision` or directly via Notion MCP
