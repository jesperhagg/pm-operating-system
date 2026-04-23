# PM Operating System

My personal AI-native product management operating system, delivered as a
git submodule. It encodes the PM frameworks I actually use into reusable
slash commands and specialized agents — grounded in live product data from
the consumer repo's `data/` directory, not templates or hypotheticals.

## Why this exists

I manage multiple products as a solo founder. Repeatable PM work — PRDs,
opportunity scoring, market scans, decision logging, weekly reviews —
follows the same frameworks every time, but needs fresh product context
each time. This plugin solves that: the frameworks are codified here, the
context is read from markdown files in the product repo itself.

I also use this repo to develop the operating system itself — with a
meta-agent for architectural guidance and an eval skill for quality
auditing.

## How I use it

I add this as a git submodule at `.claude/` in each product repo. Claude
Code auto-discovers the skills, agents, and commands from there, reading
that product's `data/` files automatically. One product per repo — the
repo IS the product.

```bash
git submodule add git@github.com:jesperhagg/pm-operating-system.git .claude
git submodule update --init
```

## Skills

| Skill | What it does |
|-------|-------------|
| `/fetch-context` | Reads product context from `data/` (decisions, personas, backlog, recent Signals, Market Landscape) |
| `/write-prd` | Writes a PRD using a 6-section framework, hydrated from `data/` |
| `/evaluate-opportunity` | Scores an opportunity on 4 dimensions — Pursue, Pursue narrow, Park, or Kill |
| `/market-scan <market>` | Scans competitive landscape with parallel web search and appends findings to `data/knowledge/market-landscape/` and `data/signals/active.md` |
| `/break-down` | Decomposes a PRD into kanban-ready work items using JTBD framing |
| `/weekly-review` | Weekly review: what shipped, what's blocked, Action Required signals, what's next. Portfolio mode supports multi-repo rollup. |
| `/log-decision` | Writes a structured decision file to `data/decisions/` |
| `/log-signal` | Appends a time-stamped observation (user feedback, competitive move, market signal, technical constraint, internal learning) to `data/signals/active.md` |
| `/knowledge` | Manages stakeholder profiles, reference docs, research, and Market Landscape entries in `data/knowledge/` |
| `/tasks` | Surfaces active tasks from `data/tasks/active.md` (runs at session start) |
| `/define-persona` | Writes a persona file grounded in evidence to `data/personas/` |
| `/design-experiment` | Structures a falsifiable experiment with pre-committed thresholds |
| `/pricing` | Structures a pricing decision: value metric, anchor, tiers, WTP validation plan |
| `/sunset-product` | Guided kill/park/graduate workflow with retro + archival |
| `/memory-review` | Reviews and prunes `data/` entries for staleness |
| `/pm-digest` | Daily PM + AI news digest (internal, not exported) |

## Agents

| Agent | Role |
|-------|------|
| `startup-advisor` | Pressure-tests GTM, moat, unit economics (YC + McKinsey lens) |
| `product-sculptor` | Sculpts MVPs to atomic core, defines JTBD backlogs |
| `growth-engineer` | Distribution-first growth strategy, pre-launch funnels, copy |
| `systems-architect` | System design, APIs, infrastructure, security, AI/LLM systems |

## Setup

One MCP server is required:

- **Tavily** — web search and content extraction (for `/market-scan` and `/pm-digest`)

Steps:

1. Copy `.mcp.json.example` to `.mcp.json`
2. Replace API key placeholders with your keys
3. Restart your Claude Code session

## Data layout (in the consumer repo)

Product data lives in markdown under `data/`:

```
data/
├── signals/active.md              # H3 per signal, newest first, inline metadata
├── decisions/
│   ├── index.md                   # One-line-per-decision manifest
│   └── YYYY-MM-DD-slug.md         # One file per decision
├── knowledge/
│   ├── people/
│   ├── reference/
│   ├── research/
│   └── market-landscape/          # Living docs, `## Scan —` append-only
├── personas/
│   ├── index.md
│   └── {slug}.md                  # One file per persona
└── tasks/
    ├── active.md                  # Now / Next / Later checkboxes
    └── done.md                    # Completed tasks
```

See `context/data-schemas.md` in this repo for full frontmatter and file
conventions.

### Migrating from Notion

If you previously ran this against Notion databases, run
`/migrate-from-notion` once to export pages into the `data/` layout.
It's idempotent — safe to re-run.
