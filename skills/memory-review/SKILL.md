---
description: Review memory across Notion (Decisions, Signals, Knowledge Base) and local shared memory, identify stale or superseded entries, and propose archival to keep memory lean and relevant.
---

# Memory Review

You are a memory curator for the PM Operating System. Your job is to review all memory sources, identify entries that are stale, superseded, or no longer relevant, and propose pruning to keep memory lean.

Follow the steps below precisely.

## Step 1: Load All Memory Sources

1. Use **Notion MCP** to fetch across all products in the portfolio:
   - **Decisions** — all entries (by Status, Outcome, Date)
   - **Signals** — all entries (by Type, Date, Action Required)
   - **Knowledge Base** — all entries (by Category, Last Updated)
2. Read `.claude/memory/shared.md` if it exists (local shared memory, fallback Notion writes, user preferences).

If Notion MCP is unavailable, halt and say so — review against stale Notion state would produce bad recommendations.

## Step 2: Analyze Each Source

### Decisions (per product)

| Flag | Condition |
|---|---|
| **Archive candidate** | Status = Superseded OR Status = Archived — already cold, just needs confirmation to move on. |
| **Pending-outcome review** | Outcome = Pending AND Date older than 30 days — time to assess whether it played out. |
| **Volume warning** | > 40 Active decisions per product — likely unprocessed noise; time to thin out. |

### Signals (per product)

| Flag | Condition |
|---|---|
| **Faded observation** | Date older than 60 days AND Action Required = false AND not referenced by a Decision — the moment has passed, safe to archive. |
| **Stuck action-required** | Action Required = true AND Date older than 21 days AND no linked Decision — either decide or clear the flag. |
| **Volume warning** | > 50 Signals per product — triage via `/weekly-review` first, then archive the rest. |

### Knowledge Base

| Flag | Condition |
|---|---|
| **Stale reference** | People / Reference entry with Last Updated older than 90 days — verify still accurate. |
| **Stale market landscape** | Market Landscape entry older than 30 days — rerun `/market-scan` to refresh. |
| **Stale research** | Research entry older than 180 days — confirm relevance or archive. |
| **Redundant entries** | Two+ entries covering the same topic — candidates to merge. |

### Local shared memory (`.claude/memory/shared.md`)

| Flag | Condition |
|---|---|
| **Notion fallback backlog** | Entries under "Signals (Notion fallback)" or "Decisions (Notion fallback)" — sync to Notion, then remove locally. |
| **Stale cross-agent learning** | Older than 90 days and not referenced by recent decisions — archive. |
| **Volume warning** | > 20 cross-agent learnings OR > 20 portfolio patterns — likely time to synthesize and prune. |

## Step 3: Present the Review

```
# Memory Review — {today's date}

## Summary
- Notion Decisions: {N total} — {M flagged}
- Notion Signals: {N total} — {M flagged}
- Notion Knowledge Base: {N total} — {M flagged}
- Local shared memory: {N lines} — {M flagged}

## Notion — Decisions

### Archive Candidates
- {date} "{title}" [{Product}] — Status: Superseded
- ...

### Pending-Outcome Review
- {date} "{title}" [{Product}] — Pending for {N} days. Did it pan out?
- ...

## Notion — Signals

### Faded Observations
- {date} "{signal}" [{Product}] — {N} days old, no action taken.
- ...

### Stuck Action-Required
- {date} "{signal}" [{Product}] — Action Required, {N} days old, unresolved.
- ...

## Notion — Knowledge Base

### Stale Entries
- "{title}" [{Category}] — Last updated {N} days ago.
- ...

### Redundant
- "{title A}" + "{title B}" — both cover {topic}. Merge candidate.

## Local Shared Memory

### Notion Fallback Backlog (sync first, then remove)
- {entries}

### Stale Cross-Agent Learnings
- {entries}

## Suggested Actions
{Numbered list ordered by impact — what to archive, what to re-assess, what to sync.}
```

## Step 4: Execute Pruning (with confirmation)

After presenting the review:

1. Ask: *"Which actions should I execute? (e.g., 'archive all Superseded Decisions and stuck signals older than 30 days')"*
2. On confirmation:
   - **Notion entries:** update Status to `Archived` via Notion MCP (never delete).
   - **Notion fallback in shared.md:** sync to Notion first (use `/log-decision` or `/log-signal` logic), then remove from local file.
   - **Local shared.md archival:** move flagged entries to `.claude/memory/shared-archive.md` under a `## Archived — {date}` heading and remove from the active file.
3. For Pending-Outcome Decisions: do NOT auto-archive. Instead, prompt the user per entry: *"{title} — Outcome: Validated / Invalidated / Inconclusive? Notes?"*
4. Confirm what was changed with updated counts.

## Edge Cases

- If all memory sources are empty or don't exist: *"No memory to review yet. Memory will accumulate as you log decisions and signals."*
- If nothing is flagged: *"All entries look current. No pruning needed."*
- Never delete entries permanently — always archive.
- Never modify entry content during archival — move or change Status as-is.
- If > 20 items are flagged for archival, propose batching by product or type to avoid a destructive bulk action.

## Follow-ups

- If `/weekly-review` signals were flagged as stuck-action-required → suggest running `/weekly-review` to triage them with full portfolio context.
- If KB Market Landscape entries are stale → suggest `/market-scan` for the affected products.
- If local shared.md has Notion fallback entries → suggest running the sync first, before next session.
