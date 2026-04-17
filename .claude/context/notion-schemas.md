# Notion Database Schema

> **Database IDs:** Store your workspace's Notion database IDs in
> `.claude/context/notion-routing.md` (copy from `notion-routing.example.md`).
> Skills resolve IDs from there at runtime — see `fetch-context/SKILL.md`.

All products share a single instance of each database. Skills and agents
filter by the **Product** property using the product name from the host
repo's `CLAUDE.md`. When no product identity is available, query across
all products and group results by product.

## DB Routing Rubric

The three context databases (Decisions + Signals + Knowledge Base) are
distinguished by **three orthogonal axes**. Every skill and agent must
follow this rubric when writing to Notion.

| Axis | Decisions | Signals | Knowledge Base |
|---|---|---|---|
| **What is it?** | A commitment we make | An observation of the world | A synthesized understanding we maintain |
| **Time shape** | Point in time, immutable | Time-stamped stream | Living document, updated over time |
| **Agency** | We chose this | The world did this (or we noticed it) | We compiled this |
| **Read pattern** | "What did we decide about X?" | "What changed recently?" | "What do I know about X?" |
| **Lifecycle** | Active → Superseded/Archived | Implication extracted → fades | Continually refreshed |

**Decision tree — which DB does this information go to?**

```
Is this a commitment WE are making (scope, positioning, pricing, kill/park)?
├── YES → Decisions
└── NO → Is this a time-stamped observation of something that happened
         (competitor moved, user said X, we discovered constraint Y)?
    ├── YES → Signals
    │         └── Does it also change our durable understanding of a topic?
    │             └── YES → Also update the relevant Knowledge Base entry
    └── NO  → Is this durable, re-usable knowledge (who a person is, what
              the competitive landscape for X looks like, what research has
              taught us about persona Y)?
        ├── YES → Knowledge Base
        └── NO  → Probably doesn't need to be logged. Discard.
```

**Concrete routing examples:**

| Information | DB | Why |
|---|---|---|
| Competitor launched feature yesterday | **Signals** (`Competitive Move`) + update KB Market Landscape entry | Time-stamped event, also changes our view of the landscape |
| Recurring user complaint across 5 interviews | **Signals** (`User Feedback`, Action Required = true) | Observation that demands a decision |
| Funding round announced | **Signals** (`Market Signal`) + update KB entry | Event with implication |
| "State of the market for category X" synthesis | **Knowledge Base** (`Market Landscape`) | Durable synthesis, not an event |
| Stakeholder's comms preferences | **Knowledge Base** (`People`) | Durable, not time-stamped |
| Decision to kill a feature | **Decisions** (`Kill/Park`) | A commitment |
| Technical constraint discovered during build | **Signals** (`Technical Constraint`) → if it forces a scope change, **also** log a Decision | Observation first, commitment second |
| "We validated that users will pay $X" | **Signals** (`Internal Learning`) → if we then decide to price at $X, log a Decision | Observation → commitment |
| Market scan output | **Knowledge Base** (Market Landscape entry, append dated section) + **Signals** (individual findings that meet criteria) | Dual-write; see `/market-scan` |

## Knowledge Base

| Property | Type | Values |
|----------|------|--------|
| Title | text | Entry name |
| Category | select | `People`, `Reference`, `Research`, `Market Landscape` |
| Product | multi-select | Which product(s) this applies to |
| Tags | multi-select | Freeform tags for filtering |
| Last Updated | last_edited_time | Auto — used for staleness detection |

Used by: `/knowledge`, `/market-scan`

**Category guide:**
- `People` — stakeholder profiles, communication styles, working preferences
- `Reference` — company info, product overviews, team structure, OKR history
- `Research` — domain research, literature reviews, one-shot insights
- `Market Landscape` — living documents of the competitive landscape for a
  product's market, written exclusively by `/market-scan` as append-only
  dated sections

## Task Management

| Property | Type | Values |
|----------|------|--------|
| Title | text | Task name |
| Status | select | `In Progress`, `Not Started`, `Done` |
| Priority | select | `Now`, `Next`, `Later` |
| Product | select or relation | Which product this task belongs to |
| Blocker | text or relation | What's blocking this task |
| Due Date | date | Target completion date |

Used by: `/tasks`, `/fetch-context`, `/break-down`

## Decisions

| Property | Type | Values |
|----------|------|--------|
| Title | text | Decision summary |
| Product | multi-select | Which product(s) this applies to |
| Type | select | `Architecture`, `Scope`, `Positioning`, `Pricing`, `Go-to-Market`, `Technical`, `Design`, `Partnership`, `Kill/Park` |
| Status | select | `Active`, `Superseded`, `Experimental`, `Archived` |
| Date | date | When decided |
| Context | text | Why the decision was made |
| Impact | text | What changes going forward |
| Outcome | select | `Pending`, `Validated`, `Invalidated`, `Inconclusive` |
| Outcome Notes | text | What actually happened after this decision |
| Outcome Date | date | When the outcome was assessed |
| Agent | multi-select | Which agent(s) contributed to this decision |

Used by: `/log-decision`, `/fetch-context`, `/weekly-review`, all agents.
Note: `Type: Insight` has been retired — insights are now logged as **Signals**
(see below). If legacy `Type: Insight` rows exist, they should be migrated
into the Signals database with an appropriate `Type`.
Note: The `Outcome` property enables a closed feedback loop — decisions
are logged with `Outcome: Pending`, then assessed over time via
`/weekly-review`.

## Signals

| Property | Type | Values |
|----------|------|--------|
| Signal | text (title) | One-sentence headline of the observation |
| Date | date | When the observation occurred (not today's date — the source date) |
| Type | select | `User Feedback`, `Technical Constraint`, `Market Signal`, `Competitive Move`, `Internal Learning` |
| Source | text | Where this signal came from — user interview, analytics, competitor site, build experience, etc. |
| Implication | text | What this means for the product or strategy |
| Linked Decision | text | Reference to a decision this signal triggered or should trigger |
| Action Required | checkbox | Whether this signal demands PM action |
| Product | multi-select | Which product(s) this applies to |

Used by: `/log-signal`, `/market-scan`, `/fetch-context`, `/weekly-review`,
all agents.

**When to write to Signals:**
- A concrete, time-stamped event (launch, funding, release, incident).
- A recurring user feedback pattern (3+ source mentions, not a one-off).
- A technical or regulatory constraint discovered during build.
- A validated or invalidated internal assumption (learning).
- A competitive move that pressures current positioning.

**When NOT to write to Signals:**
- Synthesized "trends" with no specific source — those belong in Knowledge
  Base (`Market Landscape` or `Research`).
- Commitments *we* are making — those belong in Decisions.
- One-off forum comments with no corroborating sources.

The feedback loop: Signals → triaged via `/weekly-review` (Action Required
filter) → either discarded, converted into a Decision via `/log-decision`,
or summarized into a Knowledge Base entry via `/knowledge add` or the next
`/market-scan` run.
