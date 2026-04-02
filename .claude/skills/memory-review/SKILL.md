---
name: memory-review
description: Review memory files across all products and shared memory, identify stale or superseded entries, and propose archival to keep memory lean and relevant. Use when the user invokes /memory-review.
---

# Memory Review

You are a memory curator for the PM Operating System. Your job is to review
all memory files, identify entries that are stale, superseded, or no longer
relevant, and propose pruning to keep memory lean and useful.

Follow the steps below precisely.

## Step 1: Load All Memory Files

Read the following files (skip any that do not exist):

1. `/Sagokraft/memory.md`
2. `/Selftaped/memory.md`
3. `/FellingPal/memory.md`
4. `.claude/memory/shared.md`

## Step 2: Analyze Each File

For each memory file that exists and has entries, evaluate:

1. **Size vs. caps** — Is the file approaching or over its limits?
   - Product memory: max 30 decisions, 20 insights, 10 open questions
   - Shared memory: max 15 cross-agent learnings, 15 portfolio patterns
2. **Staleness** — Are any entries older than 90 days and not marked Active?
3. **Superseded entries** — Are any decisions marked "Superseded" that can be
   archived?
4. **Resolved questions** — Are any open questions now answered by later
   decisions or insights?
5. **Redundancy** — Do any entries say essentially the same thing?
6. **Relevance** — Have any insights been overtaken by newer information?

## Step 3: Present the Review

Output a structured report:

```
# Memory Review — {today's date}

## Summary
- Total entries across all files: X
- Entries flagged for review: Y

## {Product/Shared} — {filename}

### Entries to Archive
- [date] "Entry title" — Reason: [superseded / stale / redundant / resolved]

### Entries to Keep
- Brief confirmation that remaining entries are current and relevant

### Open Questions to Resolve
- [date] "Question" — Suggest: [still open / resolved by X / remove]
```

## Step 4: Execute Pruning (with confirmation)

After presenting the review:

1. Ask the user: "Would you like me to archive the flagged entries?"
2. If yes, for each file with entries to archive:
   - Create or update an archive file alongside the memory file:
     - `/<Product>/memory-archive.md` for product memory
     - `.claude/memory/shared-archive.md` for shared memory
   - Move flagged entries to the archive file under a `## Archived — {date}`
     heading
   - Remove them from the active memory file
3. Confirm what was archived and the new entry counts.

## Edge Cases

- If all memory files are empty or don't exist, say: "No memory entries to
  review yet. Memory will accumulate as you work with agents and skills."
- If no entries are flagged for review, say: "All memory entries look current
  and relevant. No pruning needed."
- Never delete entries permanently — always archive them first.
- Never modify entry content during archival — move entries as-is.
