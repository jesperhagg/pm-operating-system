# Data Schemas — In-Repo Markdown

Product data lives entirely in the consumer repo under `data/`. One product
per repo: there is no `Product` field — the repo *is* the product. Skills
read and write these files directly. No external database, no MCP fetch,
no fallback buffers.

## Layout

```
<consumer-repo>/
├── CLAUDE.md                         # Skill routing + Data Routing table + Repo Identity
└── data/
    ├── README.md                     # One-paragraph map for LLM navigation
    ├── signals/
    │   ├── active.md                 # H3 per signal, newest first, inline metadata
    │   └── archive/
    │       └── YYYY-QN.md            # Quarterly rollover (managed by /memory-review)
    ├── decisions/
    │   ├── index.md                  # One-line-per-decision scannable manifest
    │   └── YYYY-MM-DD-slug.md        # One file per decision, frontmatter + body
    ├── knowledge/
    │   ├── people/{slug}.md
    │   ├── reference/{slug}.md
    │   ├── research/{slug}.md
    │   └── market-landscape/{market-slug}.md   # Living doc; /market-scan appends `## Scan — YYYY-MM-DD`
    ├── personas/
    │   ├── index.md                  # One-line-per-persona scannable manifest
    │   └── {slug}.md                 # JTBD + evidence per persona
    └── tasks/
        ├── active.md                 # Now / Next / Later H2 sections; checkboxes + HTML-comment metadata
        └── done.md                   # Flat chronological completed-task list
```

`index.md` files live only where they pay off: `decisions/` (cited
constantly by PRDs, experiments) and `personas/` (referenced by PRDs,
pricing, opportunity evaluations). Knowledge subfolders skip indexes —
glob + frontmatter is enough and avoids drift.

## DB Routing Rubric

Three orthogonal axes distinguish the entity types. Every skill must
follow this rubric when writing data.

| Axis | Decisions | Signals | Knowledge / Personas |
|---|---|---|---|
| **What is it?** | A commitment we make | An observation of the world | A synthesized understanding we maintain |
| **Time shape** | Point in time, immutable | Time-stamped stream | Living document, updated over time |
| **Agency** | We chose this | The world did this (or we noticed it) | We compiled this |
| **Read pattern** | "What did we decide about X?" | "What changed recently?" | "What do I know about X?" |
| **Lifecycle** | Active → Superseded/Archived (frontmatter) | Active → Archived (file move) | Continually refreshed |

**Decision tree — where does this information go?**

```
Is this a commitment WE are making (scope, positioning, pricing, kill/park)?
├── YES → data/decisions/YYYY-MM-DD-slug.md
└── NO → Is this a time-stamped observation of something that happened
         (competitor moved, user said X, we discovered constraint Y)?
    ├── YES → data/signals/active.md (append H3)
    │         └── Does it also change our durable understanding of a topic?
    │             └── YES → Also update the relevant data/knowledge/ entry
    └── NO  → Is this durable, re-usable knowledge (who a person is,
              what the competitive landscape for X looks like, what
              research has taught us, who the persona is)?
        ├── YES → data/knowledge/{category}/{slug}.md  (or data/personas/{slug}.md for personas)
        └── NO  → Probably doesn't need to be logged. Discard.
```

## File conventions

### Decision file — `data/decisions/YYYY-MM-DD-slug.md`

```markdown
---
title: Price Pro tier at $49/mo
date: 2026-04-20
type: Pricing                # Architecture | Scope | Positioning | Pricing | Go-to-Market | Technical | Design | Partnership | Kill/Park
status: Active               # Active | Superseded | Experimental | Archived
outcome: Pending             # Pending | Validated | Invalidated | Inconclusive
outcome_date: null
outcome_notes: null
agent: [startup-advisor]     # which agent persona contributed (or [])
linked_signals: [../signals/active.md#wtp-feedback-2026-04-15]
linked_decision: null        # relative path to a decision this supersedes/builds on
---

## Context

Why this decision was made — alternatives considered, evidence weighed.

## Impact

What this changes or constrains going forward.

## Outcome Notes

(Filled in when outcome is assessed via /weekly-review.)
```

`Type: Insight` is retired — observations belong in Signals.

### Signal entry — H3 section inside `data/signals/active.md`

```markdown
### {Headline one-liner}
<!-- date:2026-04-20 type:"User Feedback" source:"interview-2026-04-15" action_required:true linked_decision:"../decisions/2026-04-20-price-pro-49.md" -->

**Implication:** What this means for the product (1–2 sentences).
```

- `date` is the source event's date, **not** today.
- `type` is one of: `User Feedback`, `Technical Constraint`, `Market Signal`, `Competitive Move`, `Internal Learning`.
- `source` must be concrete (URL, interview ID, analytics dashboard, competitor site).
- `action_required:true` means a PM response is required. Surfaces in `/weekly-review`.
- Newest signal at the top of the file. `/memory-review` rolls faded entries to `archive/YYYY-QN.md`.

### Knowledge entry — `data/knowledge/<category>/<slug>.md`

```markdown
---
title: Jane Doe — CEO at Acme
category: people             # people | reference | research | market-landscape
tags: [stakeholder, fund]
last_updated: 2026-04-20
status: active               # active | archived
---

(Body is category-specific. See per-category templates in /knowledge.)
```

Categories:
- **people** — stakeholder profiles, communication styles, working preferences.
- **reference** — company info, product overviews, team structure, OKR history.
- **research** — domain research, literature reviews, one-shot insights.
- **market-landscape** — living documents of the competitive landscape. Written exclusively by `/market-scan` as append-only `## Scan — YYYY-MM-DD` H2 sections. See the full structure below.

### Persona file — `data/personas/<slug>.md`

```markdown
---
title: Solo Multi-Product PM
jtbd: Prevent drift across multiple products in under 10 minutes/week
last_updated: 2026-04-20
evidence_strength: Moderate  # Strong (≥5 signals) | Moderate (2–4) | Thin (<2)
evidence: [../signals/active.md#three-tasks-missed-2026-03-02, ../signals/active.md#forgot-competitor-move-2026-03-15]
---

(Body is the 6-field persona template defined in /define-persona.)
```

### Task entries — `data/tasks/active.md` and `done.md`

Markdown checkboxes with HTML-comment metadata. Grouped by H2 in
`active.md` (Now / Next / Later).

```markdown
## Now

- [ ] Ship pricing page update <!-- priority:now due:2026-05-01 blocker:"" -->
- [ ] Interview 3 design agencies <!-- priority:now due:"" blocker:"waiting on intros" -->

## Next

- [ ] Draft Q3 OKRs <!-- priority:next due:2026-05-15 blocker:"" -->

## Later

- [ ] Migrate auth to Clerk <!-- priority:later due:"" blocker:"" -->
```

`done.md` is flat chronological with `done:` date in metadata:

```markdown
- [x] Interview 3 design agencies <!-- priority:now done:2026-04-18 -->
```

### Index files — `data/decisions/index.md`, `data/personas/index.md`

Compact one-line-per-row scannable tables. Updated by the writer skill
when a new entry is created. Format:

```markdown
# Decisions

| Date | Type | Title | Status | Outcome | File |
|---|---|---|---|---|---|
| 2026-04-20 | Pricing | Price Pro at $49/mo | Active | Pending | 2026-04-20-price-pro-49.md |
| 2026-04-15 | Scope | Cut multiplayer for v1 | Active | Pending | 2026-04-15-cut-multiplayer.md |
```

```markdown
# Personas

| Slug | Title | Evidence | Last updated |
|---|---|---|---|
| solo-pm | Solo Multi-Product PM | Moderate | 2026-04-20 |
```

### `data/README.md` template

Two short paragraphs (what this folder holds + the file tree from
"Layout" above). Shipped to consumer repos verbatim or via
`/migrate-from-notion`.

## Cross-references

Always relative paths from the file you're in.

- A decision citing signals → `linked_signals: [../signals/active.md#headline-slug]`
- A signal citing a decision → `linked_decision:"../decisions/YYYY-MM-DD-slug.md"` in the metadata comment
- A persona citing signals → `evidence: [../signals/active.md#headline-slug]`

Anchors in `signals/active.md` are auto-derived from the H3 headline
(GitHub-flavored markdown rules: lowercase, spaces → hyphens, strip
punctuation). Don't invent a separate ID system.

## Market Landscape entry structure

Maintained exclusively by `/market-scan`. Strict heading set so other
skills can parse by heading.

```markdown
---
title: Weekly Review SaaS — Market Landscape — Solo PM Tools
category: market-landscape
tags: [pm-tools, indie-saas]
last_updated: 2026-04-20
status: active
---

# Weekly Review SaaS — Market Landscape — Solo PM Tools

_Living document. New scans append dated sections below._

---

## Scan — 2026-04-20

### Competitor Radar
- **Known & Active**
  - {Competitor} — {one-line what they did} [source]
- **Newly Discovered**
  - {Competitor} — {description} [source]
- **Quiet / No Activity**
  - {Competitor}

### Product & Feature Moves
- {bullet} [source]

### Funding & Business Moves
- {bullet} [source]

### Customer Sentiment
- **Theme:** {theme}
  - {bullet} [source]

### Strategic Implications
- {bullet}

### What's New vs. Prior Scans
- {bullet}

### Sources
1. {title} — {type} — {date} — {url}

---

## Scan — 2026-03-15
...
```

When a skill needs the latest scan, it reads only the most recent
`## Scan — {date}` H2 section, not the full file history.

## Token-efficiency rules for skills

1. **Read indexes first.** Decisions and personas have `index.md`.
   Glob the index, pick the rows you need, then open targeted files.
2. **Read frontmatter, not bodies, when filtering.** `Grep -B 0 -A 8`
   the frontmatter block. Only open the body when the entry passes the
   filter.
3. **Use `data/signals/active.md` for recent signals.** Never load the
   archive unless explicitly looking up history.
4. **Cache nothing across skill invocations.** Files are cheap; staleness
   is dangerous. Always read fresh.
