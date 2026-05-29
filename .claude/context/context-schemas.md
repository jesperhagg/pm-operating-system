# Context Schemas — In-Repo Markdown

Product context lives entirely in the consumer repo under `context/`. One
product per repo: there is no `Product` field — the repo *is* the product.
Skills read and write these files directly. No external database, no fallback
buffers. Operational work items live in `tasks/` alongside `context/`.

## Layout

```
<consumer-repo>/
├── CLAUDE.md                             # Skill routing + Context Routing table + Repo Identity
├── context/
│   ├── README.md                         # One-paragraph map for LLM navigation
│   ├── INDEX.md                          # Machine-facing router; anchor lists refreshed by /context-sync
│   ├── .sync-state.json                  # Machine-written by /context-sync; tracks last-sync per file
│   ├── .notion-routing.md                # Notion DB / page → context file mapping table
│   ├── product/
│   │   ├── decisions.md                  # H2-per-decision, newest first
│   │   ├── strategy.md                   # Positioning, bets, north-star — living doc
│   │   ├── roadmap.md                    # Committed / next / later — living doc
│   │   └── experiments.md               # Active hypotheses + outcome log
│   ├── market/
│   │   ├── landscape.md                  # Living competitive doc; /market-scan appends ## Scan — YYYY-MM-DD
│   │   ├── signals.md                    # Market and competitive observations, newest first
│   │   └── archive/
│   │       └── signals-YYYY-QN.md        # Quarterly rollover (managed by /context-sync)
│   ├── users/
│   │   ├── personas.md                   # H2-per-persona, all personas in one file
│   │   ├── feedback.md                   # User-feedback signal stream, newest first
│   │   ├── research.md                   # Domain research, literature, one-shot insights
│   │   └── icp.md                        # H2-per-ICP (lazy; written by /ideal-customer-profile)
│   ├── ops/
│   │   ├── people.md                     # Stakeholder profiles
│   │   ├── leads.md                      # Pipeline board: one row per active lead
│   │   └── leads-detail/
│   │       └── {slug}.md                 # One file per lead; append-only interaction log
│   └── learnings/
│       └── {skill-name}.md               # H3-per-run lesson log; written by looped skills
└── tasks/
    ├── active.md                         # Now / Next / Later H2; checkboxes + HTML-comment metadata
    ├── done.md                           # Flat chronological completed-task list
    └── governance.md                     # Auto-written by /context-sync for conflicts requiring PM review
```

## Context Routing Rubric

Three axes distinguish where information belongs. Every skill must follow
this rubric when writing context.

| Axis | Decisions | Signals / Feedback | Knowledge / Personas | Leads |
|---|---|---|---|---|
| **What is it?** | A commitment we make | An observation of the world | A synthesized understanding we maintain | A tracked relationship under active cultivation |
| **Time shape** | Point in time, immutable | Time-stamped stream | Living document, updated over time | Hybrid — living frontmatter + append-only interaction log |
| **Agency** | We chose this | The world did this (or we noticed it) | We compiled this | Mixed — we act, they react |
| **Read pattern** | "What did we decide about X?" | "What changed recently?" | "What do I know about X?" | "What's in my pipeline?" |
| **Lifecycle** | Active → Superseded/Archived (inline frontmatter) | Active → Archived (quarterly file move) | Continually refreshed | Uncontacted → … → Won/Lost → archived |

**Signal routing by type:**

| Signal type | File |
|---|---|
| User Feedback | `context/users/feedback.md` |
| Market Signal, Competitive Move | `context/market/signals.md` |
| Internal Learning | `context/product/experiments.md` |
| Technical Constraint | `context/product/decisions.md` (if commitment) or `context/market/signals.md` |

**Skill artifact routing:**

| Artifact | File |
|---|---|
| Per-skill accumulated learning | `context/learnings/{skill-name}.md` (H3 block) |
| ICP profile | `context/users/icp.md` (H2 block) |
| North Star Metric definition | `context/product/strategy.md` (H2 block: "North Star Metric") |
| Cohort analysis insight (when persisted) | `context/product/experiments.md` (H2 block) |
| Lean Canvas | `docs/lean-canvas-{product-slug}.md` (full doc — not in `context/`) |

**Decision tree — where does this information go?**

```
Is this about a specific prospect/customer we're cultivating?
├── YES → context/ops/leads-detail/{slug}.md + context/ops/leads.md board
└── NO → Is this a commitment WE are making (scope, positioning, pricing, kill/park)?
    ├── YES → context/product/decisions.md (new H2 block)
    └── NO → Is this a time-stamped observation of something that happened?
        ├── YES → context/market/signals.md or context/users/feedback.md (H3 block)
        │         └── Does it also change our durable understanding of a topic?
        │             └── YES → Also update the relevant context/ file
        └── NO  → Is this durable, synthesized knowledge about a topic?
            ├── YES → appropriate context/ file (strategy, research, people, personas)
            └── NO  → Probably doesn't need to be logged. Discard.
```

## File Conventions

### Decisions — `context/product/decisions.md`

All decisions in one file, newest first. Each decision is an H2 block with
an inline frontmatter comment and three body sections.

```markdown
## Price Pro tier at $49/mo {#price-pro-49-2026-04-20}
<!-- date:2026-04-20 type:Pricing status:Active outcome:Pending agent:[] linked_signals:[context/market/signals.md#wtp-feedback-2026-04-15] linked_decision:null session:synced -->

### Context

Why this decision was made — alternatives considered, evidence weighed.

### Impact

What this changes or constrains going forward.

### Outcome Notes

_(Filled in via /weekly-review when outcome is assessed.)_

---
```

- **Anchor slug** — derived from H2 title: lowercase, spaces → hyphens, strip punctuation, append `-YYYY-MM-DD`. Used for `linked_decision` cross-references.
- `type` — one of: Architecture | Scope | Positioning | Pricing | Go-to-Market | Technical | Design | Partnership | Kill/Park
- `status` — one of: Active | Superseded | Experimental | Archived
- `outcome` — one of: Pending | Validated | Invalidated | Inconclusive
- `session` — one of: `pending` (written this session, not yet reconciled with sources) | `synced` (reconciled by `/context-sync`)

### Signal entries — `context/market/signals.md` and `context/users/feedback.md`

Same H3 format in both files. Newest first. Each file has a thin H1 header.

```markdown
# Market Signals

_Newest first. One H3 per signal. Market / competitive observations._

### {Headline one-liner} {#headline-slug-YYYY-MM-DD}
<!-- date:2026-04-20 type:"Competitive Move" source:"competitor-blog-2026-04-19" action_required:true linked_decision:"context/product/decisions.md#cut-multiplayer-2026-04-15" session:synced -->

**Implication:** What this means for the product (1–2 sentences).
```

```markdown
# User Feedback

_Newest first. One H3 per signal. User feedback and customer observations._
```

- `date` is the source event's date, not today.
- `type` — one of: User Feedback | Technical Constraint | Market Signal | Competitive Move | Internal Learning
- `source` must be concrete (URL, email thread ID, interview date, analytics dashboard).
- `action_required:true` surfaces in `/weekly-review`.
- Quarterly rollover: signals older than 90 days move to `context/market/archive/signals-YYYY-QN.md` by `/context-sync`.

### Personas — `context/users/personas.md`

All personas in one file; H2 per persona with inline frontmatter comment.

```markdown
# Personas

_One H2 per persona. Evidence-backed customer segments._

## Solo Multi-Product PM {#solo-pm}
<!-- jtbd:"Prevent drift across multiple products in under 10 min/week" last_updated:2026-04-20 evidence_strength:Moderate evidence:[context/users/feedback.md#three-tasks-missed-2026-03-02] session:synced -->

**Who:** ...

**JTBD:** ...

**Pain:** ...

**Current Workaround:** ...

**Buying Trigger:** ...

**Anti-Persona:** ...

---
```

- `evidence_strength` — Strong (≥5 signals) | Moderate (2–4) | Thin (<2)
- `evidence` — list of relative anchors to feedback/signal entries

### Learnings — `context/learnings/{skill-name}.md`

One file per skill that adopts the learnings loop. Created lazily by the
skill on first capture. H3 per run, newest first. Same lifecycle as other
session-written context: `session:pending` flips to `session:synced` via
`/context-sync`.

```markdown
# Learnings — {skill-name}

### {one-line headline of what made this run distinctive} {#headline-slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD skill:{skill-name} session:pending -->

**Worked:** {one sentence}.
**Missed:** {one sentence}.
**Next time:** {one adjustment}.
```

Rules:
- Newest entry at top, immediately after the H1 header.
- Three lines (`Worked` / `Missed` / `Next time`). Not three paragraphs.
- Looped skills read the top 3–5 entries during Hydration and apply
  silently — they do not narrate prior lessons back to the user.
- Looped skills (current set): `/write-prd`, `/define-persona`, `/pricing`,
  `/evaluate-opportunity`, `/design-experiment`, `/market-scan`,
  `/tech-review`, `/break-down`, `/weekly-review`.

### ICP — `context/users/icp.md`

Created lazily by `/ideal-customer-profile` on first run. One H2 per ICP
(most solo products have one; a few have two). Distinct from personas:
ICP describes the *segment we sell to* with disqualifiers and a fit-score
rubric; personas describe the *individual buyer's* JTBD.

```markdown
# ICP

## {Short ICP name} {#slug}
<!-- last_updated:YYYY-MM-DD fit_score_rubric:"see below" session:pending -->

**Firmographics:** {company size, stage, geo, industry}.
**Tech stack:** {required / preferred / disqualifying tools}.
**Use case:** {the specific job they hire us for}.
**Buying trigger:** {discrete event that starts the buying motion}.
**Buying committee:** {decision-maker + influencers + blockers}.
**Disqualifiers:** {explicit list — required, non-empty}.
**Fit-score rubric:** {1–5 scale + what each score means}.

---
```

### Research — `context/users/research.md`

Living doc; sections added over time. No strict per-entry format — each
H2 is a research area or study, with a `last_updated` comment.

```markdown
# Research

## PLG Conversion Benchmarks {#plg-conversion}
<!-- last_updated:2026-04-20 source:"openviewpartners.com/report-2025" session:synced -->

Key findings...
```

### People — `context/ops/people.md`

Living doc; H2 per stakeholder.

```markdown
# People

## Jane Doe — CEO at Acme {#jane-doe-acme}
<!-- role:"CEO" company:"Acme Co" last_updated:2026-04-20 session:synced -->

Communication style, context, working preferences...
```

### Strategy — `context/product/strategy.md`

Living doc; sections updated by `/context-sync` from Notion or session memory.
No per-entry format constraint — structured as the PM sees fit, with H2
sections per strategic topic (Positioning, Core Bet, North Star, etc.).

### Roadmap — `context/product/roadmap.md`

Living doc; three H2 sections: `## Committed`, `## Next`, `## Later`.
Each item is a bullet. Updated during planning sessions.

### Experiments — `context/product/experiments.md`

Living doc; H2 per experiment. Append-only.

```markdown
## Free-trial → paid conversion at 14 days {#free-trial-14d-2026-04-10}
<!-- started:2026-04-10 status:Active hypothesis:"14-day trial will convert at 8%" metric:"trial-to-paid rate" session:synced -->

**Hypothesis:** ...
**Measurement:** ...
**Outcome:** _(updated when resolved)_
```

### Market Landscape — `context/market/landscape.md`

Maintained exclusively by `/market-scan`. Append-only `## Scan — YYYY-MM-DD`
H2 sections. Structure identical to the prior `data/knowledge/market-landscape/`
format:

```markdown
---
title: {Product} — Market Landscape
last_updated: 2026-04-20
---

# {Product} — Market Landscape

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
```

When a skill needs the latest scan, read only the most recent
`## Scan — {date}` H2 section, not the full file history.

### Lead board — `context/ops/leads.md`

Compact pipeline board; one row per active lead.

```markdown
# Leads

| Status | Company | Contact | Fit | Last Contact | Next Action | File |
|---|---|---|---|---|---|---|
| Demo | Acme Co | Jane Doe | High | 2026-04-18 | Demo 2026-04-22 | leads-detail/acme-co.md |
```

### Lead detail — `context/ops/leads-detail/{slug}.md`

Format identical to the prior `data/leads/{slug}.md`. Frontmatter +
`## Interactions` (append-only, newest first) + `## Notes`.

```markdown
---
title: Jane Doe — Acme Co
company: Acme Co
contact:
  name: Jane Doe
  role: Head of Product
  email: jane@acme.co
  linkedin: linkedin.com/in/janedoe
status: Contacted
source: cold-email
fit: High
persona: solo-pm
last_contact: 2026-04-18
next_action: "Send follow-up if no reply by 2026-04-25"
next_action_date: 2026-04-25
tags: [pm-tools, series-a]
---

## Interactions
<!-- Newest first. Append-only. One H3 per event. -->

### 2026-04-18 — Sent cold email
<!-- channel:email outcome:sent -->

Pitched PM OS for solo PMs. Referenced her tweet on context-switching pain.

## Notes

Free-form context: pain points, budget signals, objections raised.
```

## Tasks/ Conventions

### `tasks/active.md` and `tasks/done.md`

Format unchanged from the prior `data/tasks/` schema. Checkboxes with
HTML-comment metadata. Grouped by H2 in `active.md`.

```markdown
# Active Tasks

## Now

- [ ] Ship pricing page update <!-- priority:now due:2026-05-01 blocker:"" -->

## Next

- [ ] Draft Q3 OKRs <!-- priority:next due:2026-05-15 blocker:"" -->

## Later

- [ ] Migrate auth to Clerk <!-- priority:later due:"" blocker:"" -->
```

`done.md` is flat chronological with `done:` date:

```markdown
- [x] Interview 3 design agencies <!-- priority:now done:2026-04-18 -->
```

### `tasks/governance.md`

Written exclusively by `/context-sync`. Never edited by write skills. PM
reviews and resolves each item manually, or via `/weekly-review`.

```markdown
# Governance Tasks

_Written by /context-sync. Review and resolve each item._

## Semantic Conflicts

- [ ] Resolve conflict: Pro tier pricing <!-- conflict_type:semantic source_a:"context/product/decisions.md#price-pro-49-2026-04-20" source_b:"notion:page-abc123" detected:2026-05-11 -->
  **Source A says:** Pro tier at $49/mo (context/product/decisions.md, last synced 2026-04-20)
  **Source B says:** Pro tier at $39/mo (Notion page "Pricing v2", updated 2026-05-08)

## Staleness Alerts

- [ ] Refresh context/market/landscape.md <!-- staleness_type:age threshold_days:30 last_synced:2026-04-10 source:notion -->
```

## `.sync-state.json` Schema

Machine-written by `/context-sync`. Never edit manually. Tracks what was
last synced so incremental runs skip unchanged sources.

```json
{
  "last_sync": "2026-05-11T10:00:00Z",
  "sources": {
    "notion": {
      "context/product/decisions.md": {
        "last_synced": "2026-05-11T10:00:00Z",
        "page_ids": ["abc123", "def456"],
        "checksum": "sha256-of-last-compiled-content"
      },
      "context/market/signals.md": {
        "last_synced": "2026-05-11T10:00:00Z",
        "page_ids": ["ghi789"],
        "checksum": "sha256-..."
      }
    },
    "gmail": {
      "context/users/feedback.md": {
        "last_synced": "2026-05-11T10:00:00Z",
        "query": "label:pm-signals after:2026-05-01",
        "thread_count": 12
      },
      "context/market/signals.md": {
        "last_synced": "2026-05-11T10:00:00Z",
        "query": "subject:(competitor OR market) after:2026-05-01",
        "thread_count": 3
      }
    },
    "session_memory": {
      "context/product/decisions.md": {
        "last_appended": "2026-05-11T09:45:00Z"
      }
    }
  }
}
```

## `<!-- session: pending -->` Annotation

When a write skill (e.g., `/log-decision`, `/log-signal`) adds a new block
to a context file during a session, it appends `session:pending` in the
inline metadata comment on that block's header. This marks content that
has been captured locally but not yet reconciled with external sources.

```markdown
## Cut multiplayer from v1 {#cut-multiplayer-2026-05-11}
<!-- date:2026-05-11 type:Scope status:Active outcome:Pending agent:[] linked_signals:[] linked_decision:null session:pending -->
```

`/context-sync` step 3 processes these: verifies consistency, runs a
conflict check if the new block overlaps semantically with existing context,
then changes `session:pending` to `session:synced`. The block content stays;
only the marker changes.

**Rules:**
- Write skills always add `session:pending` when writing a new block.
- `/context-sync` is the only skill that writes `session:synced`.
- Never manually set `session:synced` — let `/context-sync` do it.

## Staleness Thresholds

| Context file | Source | Hard threshold | Soft warning |
|---|---|---|---|
| context/market/signals.md | Notion + Gmail | 14 days | 7 days |
| context/users/feedback.md | Notion + Gmail | 14 days | 7 days |
| context/market/landscape.md | Notion + web | 30 days | 21 days |
| context/product/decisions.md | Sessions | 30 days (no new decision) | — |
| context/users/personas.md | Notion + sessions | 90 days | 60 days |
| context/ops/people.md | Notion + sessions | 90 days | 60 days |
| context/users/research.md | Notion | 180 days | 120 days |
| context/product/strategy.md | Notion + sessions | 60 days | 30 days |
| context/product/experiments.md | Sessions | 30 days (no new entry) | — |

**Hard threshold:** `/context-sync` writes a staleness task to `tasks/governance.md`.
**Soft warning:** `/context-sync` notes it in the sync summary but does not create a task.

## Cross-References

Always relative paths from the file you're in.

- A decision citing signals:
  `linked_signals:[context/market/signals.md#wtp-feedback-2026-04-15]`
- A signal citing a decision:
  `linked_decision:"context/product/decisions.md#price-pro-49-2026-04-20"`
- A persona citing feedback signals:
  `evidence:[context/users/feedback.md#headline-slug-YYYY-MM-DD]`

Anchors are derived from the H2/H3 headline using GitHub-flavored markdown
rules: lowercase, spaces → hyphens, strip punctuation, append date suffix
(`-YYYY-MM-DD`) to ensure uniqueness across time. Don't invent a separate ID
system.

## Token-Efficiency Rules for Skills

1. **Read `context/INDEX.md` first when it exists.** It is the machine-facing
   router refreshed by `/context-sync` and lists the most recent anchors per
   file. Use it to scope which downstream files to open before grepping.
2. **Read the relevant H2 section, not the full file.** Most context files
   are multi-entry; use grep for the H2 heading, then read that section only.
3. **Filter by inline metadata before reading bodies.** Grep for
   `status:Active` or `date:202...` in the metadata comment before opening
   the full section.
4. **Never load archive files unless explicitly looking up history.**
   `context/market/archive/` is for historical reference only.
5. **Read the most recent `## Scan — {date}` in landscape.md, not the
   full file history.**
6. **Cache nothing across skill invocations.** Files are cheap; staleness
   is dangerous. Always read fresh.
7. **Don't read `.sync-state.json` in analysis skills.** That file is for
   `/context-sync` only. Analysis skills read context files, not sync metadata.
