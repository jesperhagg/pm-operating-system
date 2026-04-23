# PM OS — Repo Map
_Last generated: 2026-04-23 | 22 skills / 4 agents / 1 commands_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `.claude/skills/` | Skills (available in consumer repos via submodule) | 22 |
| `.claude/agents/` | Chat-persona agents (available in consumer repos) | 4 |
| `.claude/commands/` | Slash commands (available in consumer repos) | 1 |
| `.claude/context/` | Lazy-loaded reference docs | 2 |

## Skills — `.claude/skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|----------|
| /break-down | `.claude/skills/break-down/SKILL.md` | 88 | Break down a PRD or feature idea into kanban-ready work items. Reads c |
| /define-persona | `.claude/skills/define-persona/SKILL.md` | 200 | Define a customer persona grounded in real evidence — not demographi |
| /design-experiment | `.claude/skills/design-experiment/SKILL.md` | 166 | Structure a fast, falsifiable experiment to validate a hypothesis. For |
| /evaluate-opportunity | `.claude/skills/evaluate-opportunity/SKILL.md` | 203 | Evaluate a startup or product opportunity from a solo-founder / indie- |
| /fetch-context | `.claude/skills/fetch-context/SKILL.md` | 98 | Fetch live product context from the consumer repo's data/ files. Found |
| /generate-repo-map | `.claude/skills/generate-repo-map/SKILL.md` | 112 | Regenerate .claude/REPO-MAP.md by scanning current skills, agents, and |
| /knowledge | `.claude/skills/knowledge/SKILL.md` | 259 | Fetch, store, and review structured knowledge in data/knowledge/. Mana |
| /log-decision | `.claude/skills/log-decision/SKILL.md` | 88 | Log a product decision to data/decisions/ as a markdown file with stru |
| /log-interaction | `.claude/skills/log-interaction/SKILL.md` | 142 | Append a dated interaction (email, reply, call, demo, meeting) to an e |
| /log-lead | `.claude/skills/log-lead/SKILL.md` | 137 | Log a new prospect or customer to data/leads/ as a markdown file with  |
| /log-signal | `.claude/skills/log-signal/SKILL.md` | 135 | Log a time-stamped observation to data/signals/active.md as an H3 sect |
| /market-scan | `.claude/skills/market-scan/SKILL.md` | 338 | Scan the competitive landscape for the product, discovering active com |
| /memory-review | `.claude/skills/memory-review/SKILL.md` | 173 | Review memory across data/ (Decisions, Signals, Knowledge, Personas, L |
| /migrate-from-notion | `.claude/skills/migrate-from-notion/SKILL.md` | 191 | One-shot migration of legacy Notion product data (Decisions, Signals,  |
| /pipeline | `.claude/skills/pipeline/SKILL.md` | 159 | Read-only view of the sales pipeline from data/leads/. Groups leads by |
| /pm-digest | `.claude/skills/pm-digest/SKILL.md` | 154 | Search the web for the latest PM + AI news, discussions, and best prac |
| /pm-init | `.claude/skills/pm-init/SKILL.md` | 174 | Initialize the data/ directory tree in a consumer repo with all subfol |
| /pricing | `.claude/skills/pricing/SKILL.md` | 211 | Structure a pricing decision. Picks a value metric, sets an anchor pri |
| /sunset-product | `.claude/skills/sunset-product/SKILL.md` | 204 | Guided kill-or-park workflow for a product or bet that isn't working.  |
| /tasks | `.claude/skills/tasks/SKILL.md` | 139 | Surface active tasks from data/tasks/active.md with sprint-style forma |
| /weekly-review | `.claude/skills/weekly-review/SKILL.md` | 134 | Run a weekly review — single-product (default) or portfolio (across  |
| /write-prd | `.claude/skills/write-prd/SKILL.md` | 143 | Write a Product Requirements Document using opinionated per-section te |

## Agents — `.claude/agents/*/AGENT.md`

| Agent | Path | Lines | Domain |
|-------|------|-------|--------|
| growth-engineer | `.claude/agents/growth-engineer/AGENT.md` | 38 | Distribution-first growth specialist. Advisory by default, produces co |
| product-sculptor | `.claude/agents/product-sculptor/AGENT.md` | 36 | Minimalist PM who sculpts MVPs to their atomic core. Obsessed with Tim |
| startup-advisor | `.claude/agents/startup-advisor/AGENT.md` | 37 | Analytical startup advisor (YC + McKinsey lens). Pressure-tests GTM, m |
| systems-architect | `.claude/agents/systems-architect/AGENT.md` | 39 | Senior technical architect for product systems. Architecture only —  |

## Commands — `.claude/commands/*.md`

| Command | Path | Purpose |
|---------|------|----------|
| /update-submodule | `.claude/commands/update-submodule.md` | Pull the latest pm-os submodule commits from the remote. |

## Reference Docs — `.claude/context/`

| File | Lines | Load when |
|------|-------|----------|
| `data-schemas.md` | 383 | Writing to data/ (Decisions, Signals, Knowledge, Personas, Tasks) |
| `dev-standards.md` | 173 | Authoring or reviewing skills, agents, plugin infrastructure |

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify a skill | `.claude/skills/<name>/SKILL.md` |
| Modify an agent | `.claude/agents/<name>/AGENT.md` |
| Modify a command | `.claude/commands/<name>.md` |
| Check data layer schemas (frontmatter, file shapes, routing rubric) | `.claude/context/data-schemas.md` |
| Check skill design patterns + conventions | `.claude/context/dev-standards.md` |
| Add a new skill | New `.claude/skills/<name>/SKILL.md` (auto-discovered) |
| Add a new agent | New `.claude/agents/<name>/AGENT.md` (auto-discovered) |
| Add a new command | New `.claude/commands/<name>.md` (auto-discovered) |
