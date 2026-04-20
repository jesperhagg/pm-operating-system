# PM OS — Repo Map
_Last generated: 2026-04-20 | 19 exported skills / 3 internal skills / 4 agents_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `skills/` | Exported skills (available in consumer repos via plugin) | 19 |
| `.claude/skills/` | Internal skills (this repo only) | 3 |
| `agents/` | Exported chat-persona agents (available in consumer repos) | 4 |
| `.claude/context/` | Lazy-loaded reference docs | 2 |
| `.claude-plugin/` | plugin.json (manifest), marketplace.json | 2 |

## Exported Skills — `skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|----------|
| /break-down | `skills/break-down/SKILL.md` | 88 | Break down a PRD or feature idea into kanban-ready work items. Reads c |
| /define-persona | `skills/define-persona/SKILL.md` | 200 | Define a customer persona grounded in real evidence — not demographi |
| /design-experiment | `skills/design-experiment/SKILL.md` | 166 | Structure a fast, falsifiable experiment to validate a hypothesis. For |
| /evaluate-opportunity | `skills/evaluate-opportunity/SKILL.md` | 203 | Evaluate a startup or product opportunity from a solo-founder / indie- |
| /fetch-context | `skills/fetch-context/SKILL.md` | 98 | Fetch live product context from the consumer repo's data/ files. Found |
| /knowledge | `skills/knowledge/SKILL.md` | 259 | Fetch, store, and review structured knowledge in data/knowledge/. Mana |
| /log-decision | `skills/log-decision/SKILL.md` | 88 | Log a product decision to data/decisions/ as a markdown file with stru |
| /log-interaction | `skills/log-interaction/SKILL.md` | 142 | Append a dated interaction (email, reply, call, demo, meeting) to an e |
| /log-lead | `skills/log-lead/SKILL.md` | 137 | Log a new prospect or customer to data/leads/ as a markdown file with  |
| /log-signal | `skills/log-signal/SKILL.md` | 135 | Log a time-stamped observation to data/signals/active.md as an H3 sect |
| /market-scan | `skills/market-scan/SKILL.md` | 338 | Scan the competitive landscape for the product, discovering active com |
| /memory-review | `skills/memory-review/SKILL.md` | 173 | Review memory across data/ (Decisions, Signals, Knowledge, Personas, L |
| /pipeline | `skills/pipeline/SKILL.md` | 159 | Read-only view of the sales pipeline from data/leads/. Groups leads by |
| /pm-init | `skills/pm-init/SKILL.md` | 174 | Initialize the data/ directory tree in a consumer repo with all subfol |
| /pricing | `skills/pricing/SKILL.md` | 211 | Structure a pricing decision. Picks a value metric, sets an anchor pri |
| /sunset-product | `skills/sunset-product/SKILL.md` | 204 | Guided kill-or-park workflow for a product or bet that isn't working.  |
| /tasks | `skills/tasks/SKILL.md` | 139 | Surface active tasks from data/tasks/active.md with sprint-style forma |
| /weekly-review | `skills/weekly-review/SKILL.md` | 134 | Run a weekly review — single-product (default) or portfolio (across  |
| /write-prd | `skills/write-prd/SKILL.md` | 143 | Write a Product Requirements Document using opinionated per-section te |

## Internal Skills — `.claude/skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|----------|
| /generate-repo-map | `.claude/skills/generate-repo-map/SKILL.md` | 114 | Regenerate .claude/REPO-MAP.md by scanning current skills, agents, and |
| /migrate-from-notion | `.claude/skills/migrate-from-notion/SKILL.md` | 191 | One-shot migration of legacy Notion product data (Decisions, Signals,  |
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
| `data-schemas.md` | 383 | Writing to data/ (Decisions, Signals, Knowledge, Personas, Tasks) |
| `dev-standards.md` | 180 | Authoring or reviewing skills, agents, plugin infrastructure |

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify an exported skill | `skills/<name>/SKILL.md` |
| Modify an internal skill | `.claude/skills/<name>/SKILL.md` |
| Modify an agent | `agents/<name>/AGENT.md` |
| Update plugin version | `.claude-plugin/plugin.json` |
| Check data layer schemas (frontmatter, file shapes, routing rubric) | `.claude/context/data-schemas.md` |
| Check skill design patterns + conventions | `.claude/context/dev-standards.md` |
| Add a new exported skill | New `skills/<name>/SKILL.md` (auto-discovered) |
| Add a new internal skill | New `.claude/skills/<name>/SKILL.md` |
| Add a new agent | New `agents/<name>/AGENT.md` (auto-discovered) |
| Update marketplace listing | `.claude-plugin/marketplace.json` (major releases only) |
