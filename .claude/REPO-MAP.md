# PM OS — Repo Map
_Last generated: 2026-04-16 | 15 exported skills / 2 internal skills / 4 agents_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `skills/` | Exported skills (available in consumer repos via plugin) | 15 |
| `.claude/skills/` | Internal skills (this repo only) | 2 |
| `agents/` | Exported chat-persona agents (available in consumer repos) | 4 |
| `.claude/context/` | Lazy-loaded reference docs | 2 |
| `.claude-plugin/` | plugin.json (manifest), marketplace.json | 2 |

## Exported Skills — `skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|----------|
| /break-down | `skills/break-down/SKILL.md` | 88 | Break down a PRD or feature idea into kanban-ready work items. Fetches |
| /define-persona | `skills/define-persona/SKILL.md` | 185 | Define a customer persona grounded in real evidence — not demographi |
| /design-experiment | `skills/design-experiment/SKILL.md` | 167 | Structure a fast, falsifiable experiment to validate a hypothesis. For |
| /evaluate-opportunity | `skills/evaluate-opportunity/SKILL.md` | 139 | Evaluate a startup or product opportunity against strategic criteria.  |
| /fetch-context | `skills/fetch-context/SKILL.md` | 74 | Fetch live product context from Notion. Foundation skill used by other |
| /knowledge | `skills/knowledge/SKILL.md` | 245 | Fetch, store, and review structured knowledge in Notion. Manages three |
| /log-decision | `skills/log-decision/SKILL.md` | 81 | Log a product decision to Notion and local memory. Captures the decisi |
| /log-signal | `skills/log-signal/SKILL.md` | 137 | Log a time-stamped observation to the Notion Signals database. Capture |
| /market-scan | `skills/market-scan/SKILL.md` | 344 | Scan the competitive landscape for a product, discovering active compe |
| /memory-review | `skills/memory-review/SKILL.md` | 132 | Review memory across Notion (Decisions, Signals, Knowledge Base) and l |
| /pricing | `skills/pricing/SKILL.md` | 211 | Structure a pricing decision. Picks a value metric, sets an anchor pri |
| /sunset-product | `skills/sunset-product/SKILL.md` | 187 | Guided kill-or-park workflow for a product, feature, or bet that isn't |
| /tasks | `skills/tasks/SKILL.md` | 141 | Surface active tasks from the Notion backlog with sprint-style formatt |
| /weekly-review | `skills/weekly-review/SKILL.md` | 124 | Run a portfolio-level weekly review across all products. Reads memory, |
| /write-prd | `skills/write-prd/SKILL.md` | 142 | Write a Product Requirements Document using opinionated per-section te |

## Internal Skills — `.claude/skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|----------|
| /generate-repo-map | `.claude/skills/generate-repo-map/SKILL.md` | 114 | Regenerate .claude/REPO-MAP.md by scanning current skills, agents, and |
| /pm-digest | `.claude/skills/pm-digest/SKILL.md` | 154 | Search the web for the latest PM + AI news, discussions, and best prac |

## Agents — `agents/*/AGENT.md`

| Agent | Path | Lines | Domain |
|-------|------|-------|--------|
| growth-engineer | `agents/growth-engineer/AGENT.md` | 38 | Distribution-first growth specialist. Advisory by default, produces co |
| product-sculptor | `agents/product-sculptor/AGENT.md` | 36 | Minimalist PM who sculpts MVPs to their atomic core. Obsessed with Tim |
| startup-advisor | `agents/startup-advisor/AGENT.md` | 37 | Analytical startup advisor (YC + McKinsey lens). Pressure-tests GTM, m |
| systems-architect | `agents/systems-architect/AGENT.md` | 39 | Senior technical architect for product systems. Architecture only —  |

## Reference Docs — `.claude/context/`

| File | Lines | Load when |
|------|-------|----------|
| `dev-standards.md` | 185 | Authoring or reviewing skills, agents, plugin infrastructure |
| `notion-schemas.md` | 142 | Writing to Notion (Decisions, Signals, KB, Tasks) |

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify an exported skill | `skills/<name>/SKILL.md` |
| Modify an internal skill | `.claude/skills/<name>/SKILL.md` |
| Modify an agent | `agents/<name>/AGENT.md` |
| Update plugin version | `.claude-plugin/plugin.json` |
| Check Notion DB schemas + routing rubric | `.claude/context/notion-schemas.md` |
| Check skill design patterns + conventions | `.claude/context/dev-standards.md` |
| Add a new exported skill | New `skills/<name>/SKILL.md` (auto-discovered) |
| Add a new internal skill | New `.claude/skills/<name>/SKILL.md` |
| Add a new agent | New `agents/<name>/AGENT.md` (auto-discovered) |
| Update marketplace listing | `.claude-plugin/marketplace.json` (major releases only) |
