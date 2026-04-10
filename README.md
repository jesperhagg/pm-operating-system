# PM Operating System

My personal AI-native product management operating system, built as a
Claude Code plugin. It encodes the PM frameworks I actually use into
reusable slash commands and specialized agents — grounded in live product
data from Notion, not templates or hypotheticals.

## Why this exists

I manage multiple products as a solo founder. Repeatable PM work — PRDs,
opportunity scoring, market scans, decision logging, weekly reviews —
follows the same frameworks every time, but needs fresh product context
each time. This plugin solves that: the frameworks are codified here, the
context is pulled live from Notion at runtime.

I also use this repo to develop the operating system itself — with a
meta-agent for architectural guidance and an eval skill for quality
auditing.

## How I use it

I install this as a Claude Code plugin in each of my product repos. The
skills and agents become available as slash commands in any repo, pulling
that product's context from Notion automatically. No product data lives
here — every skill is product-agnostic by design.

```
claude plugin marketplace add <path-or-github-url>
```

## Skills

| Skill | What it does |
|-------|-------------|
| `/fetch-context` | Pulls live product context from Notion (decisions, personas, backlog, recent Signals, Market Landscape) |
| `/write-prd` | Writes a PRD using a 6-section framework, hydrated with Notion context |
| `/evaluate-opportunity` | Scores an opportunity on 5 dimensions — Explore, Park, or Kill |
| `/market-scan <product>` | Scans competitive landscape with parallel web search and dual-writes findings to Knowledge Base (Market Landscape) and Signals |
| `/break-down` | Decomposes a PRD into kanban-ready work items using JTBD framing |
| `/weekly-review` | Portfolio-level weekly review: what shipped, what's blocked, Action Required signals, what's next |
| `/log-decision` | Logs a product decision to Notion with structured metadata |
| `/log-signal` | Logs a time-stamped observation (user feedback, competitive move, market signal, technical constraint, internal learning) to the Signals database |
| `/knowledge` | Manages stakeholder profiles, reference docs, research, and Market Landscape entries in Notion |
| `/tasks` | Surfaces active tasks from Notion backlog (runs at session start) |
| `/memory-review` | Reviews and prunes memory files and Notion entries for staleness |
| `/pm-digest` | Daily PM + AI news digest (internal, not exported) |

## Agents

| Agent | Role |
|-------|------|
| `startup-advisor` | Pressure-tests GTM, moat, unit economics (YC + McKinsey lens) |
| `product-sculptor` | Sculpts MVPs to atomic core, defines JTBD backlogs |
| `growth-engineer` | Distribution-first growth strategy, pre-launch funnels, copy |
| `systems-architect` | System design, APIs, infrastructure, security, AI/LLM systems |
| `pm-os-creator` | Meta-agent for developing this repo itself (internal) |

Agents collaborate via a one-hop protocol — any agent can consult one
other agent for cross-domain input, using a shared scratchpad for handoff.

## Internal development tools

These are only available when working in this repo directly:

- `/skill-eval` — Evaluates any skill or agent against the repo's design
  standards. Scores on 6 dimensions (pattern compliance, completeness,
  specificity, actionability, context grounding, composability). Supports
  batch evaluation across the full plugin.
- `/pm-digest` — Daily digest of PM + AI news and trends.
- `pm-os-creator` agent — Architectural guidance for designing new skills,
  auditing consistency, and keeping the plugin at the frontier of PM AI
  tooling.

## Setup

Two MCP servers are required:

1. **Notion** — live product context (decisions, personas, backlog,
   signals, market landscape)
2. **Tavily** — web search and content extraction (for `/market-scan`,
   `/pm-digest`)

Steps:

1. Copy `.mcp.json.example` to `.mcp.json`
2. Replace API key placeholders with your keys
3. Restart your Claude Code session

Four Notion databases are expected (see the full schema and the **DB
Routing Rubric** in `CLAUDE.md`):

**Knowledge Base** — durable synthesized knowledge. Categories: `People`,
`Reference`, `Research`, `Market Landscape`. Used by `/knowledge` and
`/market-scan`.

**Task Management** — shared backlog. Status, Priority, Product, Blocker,
Due Date. Used by `/tasks` and `/fetch-context`.

**Decisions** — commitments the PM has made. Type, Status, Context,
Impact, Outcome, Agent. Used by `/log-decision`, `/weekly-review`, and
all agents.

**Signals** — time-stamped observations (user feedback, competitive
moves, market signals, technical constraints, internal learnings) with an
Action Required flag. Used by `/log-signal`, `/market-scan`,
`/fetch-context`, `/weekly-review`, and all agents.

## Structure

```
skills/                    # Exported skills (available in consumer repos)
.claude/
  skills/                  # Internal skills (this repo only)
    pm-digest/
    skill-eval/
  agents/                  # Agent definitions (not exported)
    startup-advisor/
    product-sculptor/
    growth-engineer/
    systems-architect/
    pm-os-creator/
.claude-plugin/
  plugin.json              # Plugin manifest
  marketplace.json         # Marketplace listing
```
