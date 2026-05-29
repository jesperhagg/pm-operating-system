---
description: Incremental sync of context/ files from Notion, Gmail, and session memory. Detects semantic conflicts and staleness. Writes governance tasks to tasks/governance.md. Replaces /migrate-from-notion for ongoing sync.
---

# Context Sync

Keeps `context/` up to date with raw sources (Notion, Gmail, session memory).
Runs incrementally — only processes what changed since the last sync.
Detects conflicts between sources and surfaces them as governance tasks
rather than silently overwriting.

**When to run:**
- Manually via `/ctx-context-sync` any time you want a fresh pull.
- Prompted by the session-start hook when `CONTEXT_STALE=true` is set.

**Preconditions:**
- `context/` must exist. If not, run `/ctx-context-init` first.
- `context/.notion-routing.md` must exist with at least one DB mapping.
- Notion MCP and/or Gmail MCP must be connected for those sources.
  Missing sources are skipped gracefully — noted in the summary.

## Hydration

1. Read `CLAUDE.md` for product name (Repo Identity section).
2. Read `context/.sync-state.json`. Note `last_sync` timestamp. If file
   is missing or `last_sync` is null, this is a first run — treat all
   sources as fully changed.
3. Read `context/.notion-routing.md` for the DB-to-file mapping table.
4. Check which MCP servers are available:
   - `mcp__notion__*` available? → Notion sync enabled.
   - Gmail MCP available? → Gmail sync enabled.
   - Neither? → Session memory only. Note in summary.

Summarize to the user before proceeding:
*"Syncing context for {product}. Last sync: {date or 'never'}. Sources
active: {list}."*

## Step 1 — Notion Sync (incremental)

Skip entirely if Notion MCP is unavailable.

For each row in `context/.notion-routing.md`:

### 1a. Discover changed pages

Call `mcp__notion__search` with the database name to locate it, then query
for pages modified since `last_sync` using a `last_edited_time` filter.
If zero pages changed since last sync: **skip this context file entirely** —
no LLM call, no rewrite. Log: `{file}: skipped (Notion: 0 pages modified)`.

### 1b. Fetch changed pages

Call `mcp__notion__fetch` for each changed page. Run calls in parallel
where possible. Extract: title, last edited time, body content
(convert Notion blocks to markdown — handle headings, paragraphs, bullets,
numbered lists, code blocks, tables, callouts; replace unconvertible blocks
with `<!-- notion: unconverted {block_type} -->`).

### 1c. Conflict check (two-stage)

Before synthesizing, check whether new content contradicts existing context.

**Stage 1 — structural filter (no LLM):**
- Is the new content a strict superset of the existing file section? (existing
  text appears verbatim in new content) → No conflict; synthesize directly.
- Is the new content entirely novel with no overlap? → New information; append
  or synthesize without conflict check.
- Does the new content partially overlap with existing content, AND at least
  3 consecutive words from an existing claim appear in the new content with
  different surrounding context? → Proceed to Stage 2.

**Stage 2 — targeted LLM comparison (one call per flagged pair):**
1. Extract the specific H2/H3 section from the context file most likely
   affected.
2. Extract the specific claim from the new Notion content.
3. Ask: *"Do these two statements contradict each other? Answer YES or NO
   with one sentence of reasoning."*
   Use the fastest available model (prefer a cheap/fast variant).
4. YES → Write conflict task to `tasks/governance.md` (see format in
   `.claude/context/context-schemas.md`). **Preserve existing context
   file unchanged.** Log: `{file}: conflict detected, governance task written`.
5. NO → Proceed with synthesis.

### 1d. Synthesize

For each context file with new Notion content that passed conflict check:
1. Read the current context file.
2. Call LLM once to recompile the file from existing content + new Notion
   content. Instructions: synthesize into the topic-based format defined in
   `context-schemas.md`. Preserve existing anchors and cross-reference slugs.
   Do not invent frontmatter values — flag missing fields in summary.
3. Write the updated file.
4. Update `.sync-state.json` with new `last_synced` timestamp and page IDs
   for this file.

## Step 2 — Gmail Sync (incremental)

Skip entirely if Gmail MCP is unavailable.

For each Gmail query mapping in `context/.notion-routing.md`:

### 2a. Fetch new threads

Call `search_threads` with the query appended with `after:{last_sync_date}`.
If 0 new threads: **skip** — log: `{file}: skipped (Gmail: 0 new threads)`.

Call `get_thread` for each matched thread. Extract: subject, sender, date,
body first 500 chars (sufficient for signal extraction).

### 2b. Route by type

For each thread, determine signal type from subject + body snippet:
- Competitor/market content → `context/market/signals.md`
- User or customer content → `context/users/feedback.md`
- Internal/team discussion → `context/product/experiments.md`

### 2c. Append or synthesize

- 1–2 new threads for a file: append a brief H3 signal block directly.
  No full file recompilation — just prepend the block below the file header.
- 3+ new threads for the same file: run a targeted synthesis pass — read
  the current file + new thread summaries, rewrite just the top section
  (keep older entries intact below).

Signal block format follows the H3 convention in `context-schemas.md`.
Add `session:pending` if writing without full synthesis; write `session:synced`
after synthesis.

Update `.sync-state.json` with new `last_synced`, query, and `thread_count`.

## Step 3 — Session Memory Reconciliation

Grep all `context/**/*.md` files for `session:pending` in inline metadata
comments. For each found:

1. Verify the block has required fields for its type (date, type, status, etc.).
   If fields are missing, note in summary — do not fail the sync.
2. Run Stage 1 conflict check against other sections in the same file.
   If conflict flagged: run Stage 2 LLM check.
   - Conflict confirmed: write governance task, leave `session:pending` as-is.
   - No conflict: proceed.
3. Change `session:pending` to `session:synced` in the metadata comment.
4. Update `.sync-state.json` `session_memory.last_appended` for this file.

## Step 4 — Staleness Check

For each context file in the staleness thresholds table (from
`context-schemas.md`):

1. Read `last_synced` from `.sync-state.json`. If missing, treat as never
   synced.
2. Compare against hard threshold for that file.
3. If past hard threshold AND source has a newer checksum (or no checksum
   tracked): write a staleness task to `tasks/governance.md`.
4. If past soft warning threshold only: add a note to the sync summary
   output (not a governance task).
5. If past hard threshold but no detectable newer source content: add a
   soft note to summary only — do not create a governance task for
   externally-unchanged content.

Create `tasks/governance.md` if it does not exist (with the header from
`context-schemas.md`). Append to it if it exists — never overwrite.

## Step 5 — Refresh `context/INDEX.md`

`context/INDEX.md` is the machine-facing router skills consult before
opening downstream files. It must mirror the live state of `context/`.

1. If `context/INDEX.md` does not exist, skip — `/ctx-context-init` is responsible
   for the initial scaffold. Note in summary: *"INDEX.md missing — run
   `/ctx-context-init` to scaffold."*
2. For each file with a `Recent:` placeholder in the seeded INDEX
   (`product/decisions.md`, `market/signals.md`, `users/feedback.md`):
   - Read the file. Collect the top 3 H2 (for decisions) or H3 (for signals
     / feedback) anchor slugs in document order.
   - Replace the `Recent: _(refreshed by /ctx-context-sync)_` line (or the
     prior `Recent:` line from a previous sync) with `Recent: anchor-1,
     anchor-2, anchor-3` — bare slugs, comma-separated, no link syntax.
   - If a file is empty (header only), write `Recent: _(none yet)_`.
3. For `context/learnings/`: glob `*.md`, list each as a bullet under the
   `## learnings/` section as `- \`<skill>.md\` — N entries (last:
   YYYY-MM-DD)`. If `learnings/` is empty, leave the placeholder line.
4. For `context/users/icp.md`: if the file does not exist, leave the
   seeded placeholder line. If it exists, drop the parenthetical and add
   `Recent: anchor-1, anchor-2` as above.

INDEX.md is machine-written from Step 5 forward. The PM should not
hand-edit it; manual edits will be overwritten on next sync.

## Step 6 — Summary Output

```
## /ctx-context-sync — {product} — {date}

### Sources checked
- Notion: {N} DB mappings checked, {M} pages modified since last sync
- Gmail: {N} query mappings checked, {M} threads matched
- Session memory: {N} pending annotations reconciled

### Context files updated
| File | Change | Source |
|---|---|---|
| context/market/landscape.md | Recompiled (3 new Notion pages) | Notion |
| context/users/feedback.md | +2 signal blocks appended | Gmail |

### Files skipped (no change detected)
- context/product/decisions.md (Notion: 0 pages modified, 0 pending annotations)
- context/users/research.md (Notion: 0 pages modified)

### Governance tasks written: {N}
- tasks/governance.md: {N} semantic conflicts, {M} staleness alerts

### Next sync recommended: {date}
_(Based on the shortest staleness threshold across active files.)_
```

## Output

Updated context files are written silently. Sync summary is printed to
the conversation. Governance tasks are appended to `tasks/governance.md`.

## Follow-ups

- Review open governance tasks → open `tasks/governance.md` and address each
  conflict manually, then re-run `/ctx-context-sync` to confirm resolution.
- Surface active work → `/ops-tasks`
- Full context briefing after sync → `/ctx-fetch-context`
- Weekly synthesis → `/ops-weekly-review`

## Anti-Patterns

- **Don't overwrite a context file when a conflict is detected.** Preserve
  the existing content and write the governance task. The PM resolves it.
- **Don't synthesize the full file on every run.** Incremental check first —
  skip unchanged sources to avoid unnecessary LLM calls.
- **Don't write `session:synced` except in Step 3.** Write skills write
  `session:pending`; this skill resolves them.
- **Don't create or overwrite `context/.notion-routing.md`.** That file is
  owned by the PM (created by `/ctx-context-init`, edited manually). Never touch it.
- **Do overwrite `context/INDEX.md` Recent: lines in Step 5.** That file is
  machine-owned from the first sync onward — anchor lists must mirror live
  context. Preserve the static directory structure; only refresh the
  `Recent:` placeholders and the `learnings/` list.
- **Don't delete anything from source systems.** Read-only access to Notion
  and Gmail. No writes to external sources.
- **Don't fail hard on missing MCP server.** If Notion or Gmail is
  unavailable, skip that source and note it in the summary. Session memory
  reconciliation can still run.
