---
description: One-shot migration of legacy Notion product data (Decisions, Signals, Knowledge Base, Task Management) into the repo's data/ markdown layout. Idempotent — skips files that already exist.
---

# Migrate From Notion

PM OS v2 reads and writes product data from `data/` in the consumer repo.
This skill exports the legacy Notion databases into that layout so you
can cut over without losing history.

Internal skill — run once per repo during the cutover, then never again.

## Preconditions

1. The Notion MCP server must be connected (`mcp__notion__*` tools available). If it isn't, halt: *"Connect the Notion MCP server, then rerun `/migrate-from-notion`."*
2. The consumer repo must have a `CLAUDE.md` with a Repo Identity block naming the product. One product per repo — if the Notion portfolio spans multiple products, the user must cherry-pick which product this repo represents and run the migration separately per repo.
3. Ask: *"This repo will become the `{product}` product. Migrate only pages where `Product = {product}` (or rows in Notion tagged to this product). Confirm?"*

## Step 1 — Resolve Database IDs

In order of preference:

1. Read `.claude/context/notion-routing.md` if it still exists (legacy file). Parse the table to get DB IDs for Decisions, Signals, Knowledge Base, Task Management.
2. If that file is missing, use `mcp__notion__search` with queries for each DB name ("Decisions", "Signals", "Knowledge Base", "Task Management") and let the user confirm which IDs are correct.
3. Print the 4 resolved IDs back to the user and ask for confirmation before fetching anything.

## Step 2 — Fetch All Rows (filtered to this product)

For each of the 4 DBs, use `mcp__notion__query_database` with a filter on `Product = {product}` (if the property exists). Fetch all pages (paginate if needed). Keep the page content — you'll need it for bodies.

Keep counts: `{N_decisions, N_signals, N_knowledge, N_tasks}`. Print them before writing.

## Step 3 — Write Files

Create the directory scaffolding if missing:

```
data/
├── decisions/
├── signals/
├── knowledge/
│   ├── people/
│   ├── reference/
│   ├── research/
│   └── market-landscape/
├── personas/
└── tasks/
```

Write in this order (it matters for cross-references):

### 3a. Knowledge Base → `data/knowledge/{category}/{slug}.md`

For each KB page:
- Derive category from the Notion `Category` property (people | reference | research | market-landscape). Normalize the Notion category values to these four.
- Derive slug from the page title (kebab-case, alphanumeric only).
- **Personas** live at the top level, not in knowledge. If the KB page is a persona (look at category = `Research` with "Persona" in the title, or a dedicated `Personas` database if the legacy setup had one), write to `data/personas/{slug}.md` instead.
- Frontmatter: `title`, `category`, `tags` (from Notion tags or multi-select), `last_updated` (use Notion `Last Edited Time`), `status: active`.
- Body: the page content, converted from Notion blocks to markdown (handle headings, paragraphs, bullets, numbered lists, code blocks, tables, callouts).

**Market Landscape special case:** If the category is `market-landscape` and the Notion page has dated scan sections, preserve the `## Scan — YYYY-MM-DD` structure verbatim. If it has none, wrap the body in a single `## Scan — {last_edited_date}` section so the living-document format is consistent going forward.

### 3b. Personas → `data/personas/{slug}.md` + `data/personas/index.md`

For each persona (filtered from KB or from a separate Notion Personas DB if present):
- Frontmatter: `title`, `jtbd` (one-line), `last_updated`, `evidence_strength` (Strong / Moderate / Thin — infer from Notion Evidence property if present, else `Thin`), `evidence` (list of relative signal anchors — may be empty on first migration).
- Body follows the `/define-persona` template (Who / JTBD / Pain / Current Workaround / Buying Trigger / Anti-Persona).

Append a row per persona to `data/personas/index.md`:
```
| slug | title | evidence_strength | last_updated |
```
Create `index.md` with the header row if missing.

### 3c. Decisions → `data/decisions/{date}-{slug}.md` + `data/decisions/index.md`

For each decision:
- `date` = Notion `Date` property (or `Created Time` fallback), formatted `YYYY-MM-DD`.
- `slug` = kebab-case of the title, truncated to ~60 chars.
- Frontmatter: `title`, `date`, `type` (Architecture | Scope | Positioning | Pricing | Go-to-Market | Technical | Design | Partnership | Kill/Park), `status` (Active | Superseded | Experimental | Archived), `outcome` (Pending | Validated | Invalidated | Inconclusive), `outcome_date` (null if Pending), `agent` (list from Notion Agent property), `linked_signals` (list of relative paths, empty on first migration — fill in Step 4).
- Body sections: `## Context`, `## Impact`, `## Outcome Notes` — pull from matching Notion properties or body blocks. Fall back to the full page content under `## Context` if no structured fields exist.

Append a row per decision to `data/decisions/index.md`:
```
| date | title | type | status | outcome | file |
```
Create `index.md` with the header row if missing.

### 3d. Signals → `data/signals/active.md`

All signals get written into a single file, newest first.

For each signal:
- Headline = Notion page title.
- HTML-comment metadata: `date:YYYY-MM-DD type:"..." source:"..." action_required:true|false linked_decision:"..."`.
- Anchor slug (for cross-referencing) = kebab-case of headline + `-{YYYY-MM-DD}`. Use this in the H3 heading so `#anchor` links work.
- Body: `**Implication:** {1–2 sentences}` — pull from Notion `Implication` property or the first paragraph of the page body.

Write each signal as:
```markdown
### {Headline} {#anchor-slug}
<!-- date:2026-04-20 type:"User Feedback" source:"..." action_required:false linked_decision:"" -->

**Implication:** {...}
```

Sort by date DESC before writing.

**Archive handling:** Signals with `date` in a closed quarter (more than 90 days old) go to `data/signals/archive/YYYY-QN.md` instead of `active.md`. Group by quarter, newest first within each quarter file.

### 3e. Task Management → `data/tasks/active.md` + `data/tasks/done.md`

- Active tasks (Notion Status ≠ Done/Abandoned) → `data/tasks/active.md` under H2 sections matching Notion Priority: `## Now`, `## Next`, `## Later`. Default to `## Next` if no priority set.
- Completed tasks (Status = Done) → `data/tasks/done.md` flat chronological list.

Format each line:
```markdown
- [ ] {Task title} <!-- priority:{now|next|later} due:{YYYY-MM-DD or ""} blocker:"{text or ""}" -->
- [x] {Task title} <!-- priority:now done:{YYYY-MM-DD} -->
```

Scaffold `active.md` with H1 + Now/Next/Later H2s if missing. Create `done.md` if missing.

## Step 4 — Back-fill Cross-References

After all files are written:

1. For each decision, read its original Notion page for any signal links (`Linked Signals` property or inline mentions). Map Notion page IDs to the newly-written signal anchors and update the decision file's `linked_signals:` frontmatter list with relative paths.
2. For each signal, reverse-map: if the signal linked to a decision in Notion, update its `linked_decision:` metadata comment with the relative path to the new decision file.
3. For each persona, scan `evidence:` and back-fill with any signal anchors that reference the persona in Notion.

## Step 5 — Idempotency

The skill is safe to re-run:
- Before writing any file, check if it already exists. If yes, **skip** (do not overwrite) and log it to the summary as `skipped: already exists`.
- For index files (`decisions/index.md`, `personas/index.md`), read existing rows first and append only new ones (dedupe by slug / file path).
- For `signals/active.md`, dedupe by anchor slug before appending.

If the user wants to force a re-migrate, ask them to manually delete the target files first — never bulk-overwrite.

## Step 6 — Summary

Print a summary to the conversation:

```
## Migration Summary — {product} — {date}

| Database | Rows fetched | Files written | Skipped (already existed) |
|---|---|---|---|
| Decisions | {N} | {M} | {K} |
| Signals (active) | {N} | {M} | {K} |
| Signals (archive) | {N} | {M} | {K} |
| Knowledge | {N} | {M} | {K} |
| Personas | {N} | {M} | {K} |
| Tasks (active) | {N} | {M} | {K} |
| Tasks (done) | {N} | {M} | {K} |

**Manual review needed:**
- {list any rows with missing Category, Type, Priority, or other required fields}
- {list any Notion-block content that didn't convert cleanly (embeds, databases, etc.)}

**Next steps:**
1. Skim `data/decisions/index.md` for accuracy.
2. Run `/tasks` to confirm active.md parses.
3. Run `/fetch-context` to confirm hydration works end-to-end.
4. After verifying: delete `.claude/context/notion-routing.md` and drop the Notion MCP server from `.mcp.json`.
```

## Edge Cases

- **Notion page has no title:** derive from body content first-line or `page-{short-id}`.
- **Slug collision:** append `-2`, `-3`, etc. until unique.
- **Duplicate Decision on the same date with the same slug:** append `-2` to the filename and note in the summary for manual review.
- **Signal with no Implication:** use the page body first paragraph, else `**Implication:** (migration — original Notion page had no Implication field)`.
- **Task with no Priority:** default to `## Next`.
- **Empty DB:** print `{DB}: 0 rows, skipped` in the summary.
- **Notion MCP rate limits:** batch queries by page ranges of 50; retry with exponential backoff on 429 errors.

## Anti-Patterns

- **Don't overwrite existing files.** Always check first.
- **Don't invent frontmatter values.** If a property is missing, leave the field empty and flag it in the summary for manual review.
- **Don't migrate body HTML as-is.** Convert to markdown. If a Notion block can't be converted (embed, database view), replace with a `<!-- migration: unconverted {block_type} -->` comment and flag it.
- **Don't delete anything from Notion.** This is a one-way export. The user decides when to archive/delete the Notion workspace.

## Follow-ups

After migration succeeds:
- Suggest deleting `.claude/context/notion-routing.md` if it still exists in the consumer repo.
- Suggest removing the Notion entry from `.mcp.json`.
- Suggest running `/memory-review` to triage the just-migrated backlog.
