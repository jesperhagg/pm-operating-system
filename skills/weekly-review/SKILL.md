---
description: Run a portfolio-level weekly review across all products. Reads memory, backlog, and recent decisions from Notion, then produces a one-page weekly focus plan.
---

# Weekly Review

## Before Starting — Self-Hydration

1. Read the root `CLAUDE.md` to confirm the current product set
2. For each product (Sagokraft, Selftaped, FellingPal):
   - Read `/<Product>/memory.md` for recent decisions and insights
   - Read `/<Product>/context.md` if it exists (current build state)
   - Use Notion MCP to fetch:
     - Decisions from the last 7 days for this product
     - Top 5 backlog items by priority
     - Any signals flagged as "Action Required"
3. Read `.claude/memory/shared.md` for cross-product patterns
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

## Sagokraft
### Shipped: [items or "nothing"]
### Blocked: [items or "none"]
### Next week: [1-2 priorities]

## Selftaped
### Shipped: [items or "nothing"]
### Blocked: [items or "none"]
### Next week: [1-2 priorities]

## FellingPal
### Shipped: [items or "nothing"]
### Blocked: [items or "none"]
### Next week: [1-2 priorities]

## Portfolio
### Focus scores: Sagokraft [X] | Selftaped [X] | FellingPal [X]
### Cross-product patterns: [if any]
### Top priority this week: [single most important thing across all products]
```

## After Completing

Suggest the user might want to:
- Run `/log-decision` to record any decisions made during the review
- Run `/memory-review` if memory files are getting long
- Consult the **startup-advisor** agent if portfolio balance needs rethinking
- Save the review to memory: offer to append key insights to the relevant
  product `memory.md` files
