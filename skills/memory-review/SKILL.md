---
description: Review memory across data/ (Decisions, Signals, Knowledge, Personas, Leads, Tasks) and local shared memory, identify stale or superseded entries, and archive them so memory stays lean.
---

# Memory Review

You are a memory curator for the PM Operating System. Your job is to walk the
repo's `data/` tree, identify entries that are stale, superseded, or no longer
relevant, and propose pruning to keep memory lean.

Follow the steps below precisely.

## Step 1: Load All Memory Sources

1. Glob `data/**/*.md` and read **frontmatter only** for every file (don't read bodies yet — saves tokens).
2. Read `data/signals/active.md` — parse H3 sections and their `<!-- ... -->` metadata comments.
3. Read `data/tasks/active.md` — parse checkbox lines and metadata comments.
4. Read `data/decisions/index.md`, `data/personas/index.md`, and `data/leads/index.md` if they exist.
5. Read `.claude/memory/shared.md` if it exists (cross-agent user preferences / learnings — not a data store).

If `data/` does not exist, halt and say so — nothing to review yet.

## Step 2: Analyze Each Source

### Decisions (`data/decisions/*.md`)

| Flag | Condition |
|---|---|
| **Archive candidate** | `status: Superseded` OR `status: Archived` in frontmatter — cold, confirm and update `status: Archived`. |
| **Pending-outcome review** | `outcome: Pending` AND `date` older than 30 days — time to assess whether it played out. |
| **Volume warning** | > 40 Active decisions — likely unprocessed noise; thin out. |

### Signals (`data/signals/active.md`)

| Flag | Condition |
|---|---|
| **Faded observation** | `date` older than 60 days AND `action_required:false` AND not linked from any decision — move to `archive/YYYY-QN.md`. |
| **Stuck action-required** | `action_required:true` AND `date` older than 21 days AND no `linked_decision:` — either decide or clear the flag. |
| **Volume warning** | > 50 active signals — triage via `/weekly-review` first, then archive the rest. |

### Knowledge (`data/knowledge/{people,reference,research,market-landscape}/*.md`)

| Flag | Condition |
|---|---|
| **Stale people/reference** | `last_updated` older than 90 days — verify still accurate. |
| **Stale market landscape** | `last_updated` older than 30 days — rerun `/market-scan`. |
| **Stale research** | `last_updated` older than 180 days — confirm relevance or archive. |
| **Redundant entries** | Two+ files in the same category covering the same topic (match on `title` or `tags`) — candidates to merge. |

### Personas (`data/personas/*.md`)

| Flag | Condition |
|---|---|
| **Stale persona** | `last_updated` older than 180 days — rerun `/define-persona` or confirm still accurate. |
| **Thin evidence** | `evidence_strength: Thin` AND older than 60 days — either fill evidence or archive. |

### Leads (`data/leads/*.md`)

| Flag | Condition |
|---|---|
| **Closed** | `status: Won` OR `status: Lost` — move file to `data/leads/archive/` and drop the row from `data/leads/index.md`. |
| **Stale active** | `status` is not Won/Lost/Uncontacted AND `last_contact` older than 45 days AND `next_action_date` empty or past — prompt: bump status to `Lost` or set a new `next_action`. |
| **Orphaned Uncontacted** | `status: Uncontacted` AND `last_contact` empty AND file age > 30 days — likely forgotten. Prompt: reach out or archive. |
| **Volume warning** | > 60 active leads — thin the pipeline or move older Lost entries to archive. |

### Tasks (`data/tasks/active.md`)

| Flag | Condition |
|---|---|
| **Overdue** | `due:` date earlier than today, checkbox not checked. |
| **Blocker rot** | `blocker:"..."` set AND line hasn't moved in 30+ days (detect via git log on the file, optional). |
| **Stale Later** | Items in the `## Later` section older than 90 days — consider dropping. |

### Local shared memory (`.claude/memory/shared.md`)

| Flag | Condition |
|---|---|
| **Stale cross-agent learning** | Entry older than 90 days and not referenced by recent decisions — archive. |
| **Volume warning** | > 20 cross-agent learnings OR > 20 portfolio patterns — synthesize and prune. |

Note: `.claude/memory/shared.md` is **not** a data store. It's only for user
prefs and cross-agent learnings. Product data belongs in `data/`.

## Step 3: Present the Review

```
# Memory Review — {today's date}

## Summary
- Decisions: {N total} — {M flagged}
- Signals (active.md): {N total} — {M flagged}
- Knowledge: {N total} across {K} categories — {M flagged}
- Personas: {N total} — {M flagged}
- Leads: {N total active} — {M flagged}
- Tasks (active.md): {N total} — {M flagged}
- Local shared memory: {N lines} — {M flagged}

## Decisions

### Archive Candidates
- `data/decisions/{file}.md` — status: Superseded
- ...

### Pending-Outcome Review
- `data/decisions/{file}.md` — Pending for {N} days. Did it pan out?
- ...

## Signals

### Faded Observations
- "{signal headline}" ({N} days old) — no action taken.
- ...

### Stuck Action-Required
- "{signal headline}" ({N} days old) — Action Required, unresolved.
- ...

## Knowledge

### Stale Entries
- `data/knowledge/{category}/{file}.md` — last_updated {N} days ago.
- ...

### Redundant
- `{file A}` + `{file B}` — both cover {topic}. Merge candidate.

## Personas

### Stale / Thin Evidence
- `data/personas/{file}.md` — {reason}

## Tasks

### Overdue / Blocker Rot / Stale Later
- {line preview} — {reason}

## Local Shared Memory
- {flagged entries, if any}

## Suggested Actions
{Numbered list ordered by impact — what to archive, merge, re-assess, or drop.}
```

## Step 4: Execute Pruning (with confirmation)

After presenting the review:

1. Ask: *"Which actions should I execute? (e.g., 'archive all Superseded decisions and faded signals older than 60 days')"*
2. On confirmation:
   - **Decisions** — edit the file's frontmatter: set `status: Archived`. Do not move the file. Update the row in `data/decisions/index.md` to match.
   - **Signals** — cut the H3 section (headline + metadata comment + Implication block) from `data/signals/active.md` and append it to `data/signals/archive/YYYY-QN.md` (create if missing, where `QN` = current quarter). Preserve original ordering within the archive file (newest first).
   - **Knowledge** — edit the file's frontmatter: set `status: archived`. Do not move the file.
   - **Personas** — for thin/stale, flag in frontmatter (`last_updated` bumped only if actually refreshed; otherwise leave and note in suggestions).
   - **Leads (Won/Lost)** — move the file from `data/leads/{slug}.md` to `data/leads/archive/{slug}.md` (create `archive/` if missing). Remove the matching row from `data/leads/index.md`. For stale-active flags, prompt per item: mark `Lost`, set a new `next_action`, or keep as-is.
   - **Tasks** — for overdue/stale Later items, ask per item: drop, move to Next, or push out the due date.
   - **`.claude/memory/shared.md`** — move flagged entries to `.claude/memory/shared-archive.md` under a `## Archived — {date}` heading, then delete from the active file.
3. For Pending-Outcome Decisions: do NOT auto-archive. Prompt per entry: *"{title} — Outcome: Validated / Invalidated / Inconclusive? Notes?"* Then edit the frontmatter `outcome:` and `outcome_date:`, and append the notes to the `## Outcome Notes` section of the decision file.
4. Confirm what was changed with updated counts.

## Edge Cases

- If all memory sources are empty or don't exist: *"No memory to review yet. Memory will accumulate as you log decisions and signals."*
- If nothing is flagged: *"All entries look current. No pruning needed."*
- Never delete entries permanently — always archive (edit frontmatter or move to archive file).
- Never modify entry content during archival — edit only `status:` / move the block as-is.
- If > 20 items are flagged for archival, propose batching by category or type to avoid a destructive bulk action.

## Follow-ups

- If signals were flagged as stuck-action-required → suggest running `/weekly-review` to triage them with full portfolio context.
- If market-landscape entries are stale → suggest `/market-scan` to refresh.
- If personas are thin → suggest `/define-persona` to run discovery and strengthen evidence.
- If tasks are overdue with no progress → suggest `/break-down` to split and re-scope.
