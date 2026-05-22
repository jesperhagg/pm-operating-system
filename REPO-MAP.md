# PM OS — Repo Map
_Last generated: 2026-05-08 | 23 skills / 5 agents / 1 commands_
_Last generated: 2026-05-21 | 29 skills / 4 agents / 1 commands_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `agents/` | Chat-persona agents (available in consumer repos) | 5 |
| `skills/` | Skills (available in consumer repos via submodule) | 29 |
| `commands/` | Slash commands (available in consumer repos) | 1 |
| `context/` | Lazy-loaded reference docs | 3 |

## Skills — `skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|---------|
| /break-down | `skills/break-down/SKILL.md` | 104 | Break down a PRD or feature idea into kanban-ready work items. |
| /cohort-analysis | `skills/cohort-analysis/SKILL.md` | 231 | Structure a cohort analysis with pre-set thresholds; surfaces curves and divergence without averaging away signal. |
| /context-init | `skills/context-init/SKILL.md` | 341 | Initialize the context/ and tasks/ directory tree in a consumer repo with scaffold files, INDEX.md router, and Notion routing config. |
| /context-sync | `skills/context-sync/SKILL.md` | 248 | Incremental sync of context/ files from Notion, Gmail, and session memory; refreshes INDEX.md anchors. |
| /define-persona | `skills/define-persona/SKILL.md` | 164 | Define a customer persona grounded in real evidence — not demographics. |
| /design-experiment | `skills/design-experiment/SKILL.md` | 182 | Structure a fast, falsifiable experiment to validate a hypothesis. |
| /evaluate-opportunity | `skills/evaluate-opportunity/SKILL.md` | 219 | Evaluate a startup or product opportunity from a solo-founder lens. |
| /fetch-context | `skills/fetch-context/SKILL.md` | 111 | Fetch live product context from the consumer repo's context/ files, routed via INDEX.md. |
| /generate-repo-map | `skills/generate-repo-map/SKILL.md` | 276 | Regenerate REPO-MAP.md as a routing map of the codebase. |
| /ideal-customer-profile | `skills/ideal-customer-profile/SKILL.md` | 314 | Define an Ideal Customer Profile across 7 dimensions with required disqualifiers and a fit-score rubric. |
| /knowledge | `skills/knowledge/SKILL.md` | 191 | Fetch, store, and review structured knowledge in context/. |
| /lean-canvas | `skills/lean-canvas/SKILL.md` | 287 | Produce a Lean Canvas — 9 boxes with evidence required for each. |
| /log-decision | `skills/log-decision/SKILL.md` | 99 | Log a product decision to context/product/decisions.md as an H2 block. |
| /log-interaction | `skills/log-interaction/SKILL.md` | 108 | Append a dated interaction to an existing lead in context/ops/leads-detail/. |
| /log-lead | `skills/log-lead/SKILL.md` | 100 | Log a new prospect to context/ops/leads-detail/ and update context/ops/leads.md. |
| /log-signal | `skills/log-signal/SKILL.md` | 134 | Log a time-stamped observation to context/market/signals.md or context/users/feedback.md. |
| /market-scan | `skills/market-scan/SKILL.md` | 235 | Scan the competitive landscape and dual-write to context/market/landscape.md and context/market/signals.md. |
| /memory-review | `skills/memory-review/SKILL.md` | 17 | Deprecated — use /context-sync instead. |
| /migrate-from-notion | `skills/migrate-from-notion/SKILL.md` | 15 | Deprecated — use /context-init + /context-sync instead. |
| /north-star-metric | `skills/north-star-metric/SKILL.md` | 249 | Pick a North Star Metric using 5 sharpness tests; commit it with input metrics and a kill-criterion. |
| /pipeline | `skills/pipeline/SKILL.md` | 159 | Read-only view of the sales pipeline from context/ops/leads.md. |
| /pm-digest | `skills/pm-digest/SKILL.md` | 154 | Search the web for the latest PM + AI news, discussions, and best practices. |
| /pm-init | `skills/pm-init/SKILL.md` | 10 | Deprecated — use /context-init instead. |
| /pricing | `skills/pricing/SKILL.md` | 227 | Structure a pricing decision. Picks a value metric, sets an anchor price, designs tiers. |
| /sunset-product | `skills/sunset-product/SKILL.md` | 175 | Guided kill-or-park workflow for a product or bet that isn't working. |
| /tasks | `skills/tasks/SKILL.md` | 133 | Surface active tasks from tasks/active.md with sprint-style formatting. |
| /tech-review | `skills/tech-review/SKILL.md` | 282 | Audit code and architecture across six lenses. |
| /weekly-review | `skills/weekly-review/SKILL.md` | 161 | Run a weekly review — single-product or portfolio. |
| /write-prd | `skills/write-prd/SKILL.md` | 160 | Write a Product Requirements Document using opinionated per-section templates. |

## Agents — `agents/*/AGENT.md`

| Agent | Path | Lines | Domain |
|-------|------|-------|--------|
| domain-expert | `agents/domain-expert/AGENT.md` | 38 | Veteran practitioner in whatever industry the consumer repo operates in. Adapts from data/domain.md. |
| growth-engineer | `agents/growth-engineer/AGENT.md` | 38 | Distribution-first growth specialist. Advisory by default, produces co |
| product-sculptor | `agents/product-sculptor/AGENT.md` | 36 | Minimalist PM who sculpts MVPs to their atomic core. Obsessed with Tim |
| startup-advisor | `agents/startup-advisor/AGENT.md` | 37 | Analytical startup advisor (YC + McKinsey lens). Pressure-tests GTM, m |
| systems-architect | `agents/systems-architect/AGENT.md` | 42 | Senior technical architect for product systems. Architecture only —  |

## Commands — `commands/*.md`

| Command | Path | Purpose |
|---------|------|---------|
| /update-submodule | `commands/update-submodule.md` | Pull the latest pm-os submodule commits from the remote. |

## Reference Docs — `context/`

| File | Lines | Load when |
|------|-------|-----------|
| `context-schemas.md` | 551 | Writing to context/ or tasks/ (routing rubric, file shapes, sync-state, learnings/ICP/NSM destinations) |
| `data-schemas.md` | 389 | Legacy — deprecated. Migrating from old data/ layout only. |
| `dev-standards.md` | 193 | Authoring or reviewing skills, agents, submodule infrastructure |

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify a skill | `skills/<name>/SKILL.md` |
| Modify an agent | `agents/<name>/AGENT.md` |
| Modify a command | `commands/<name>.md` |
| Check context layer schemas (file shapes, routing rubric, sync-state, learnings/ICP/NSM destinations) | `context/context-schemas.md` |
| Check skill design patterns + conventions | `context/dev-standards.md` |
| Add a new skill | New `skills/<name>/SKILL.md` (auto-discovered) |
| Add a new agent | New `agents/<name>/AGENT.md` (auto-discovered) |
| Add a new command | New `commands/<name>.md` (auto-discovered) |
| Initialize context layer in a consumer repo | `/context-init` |
| Sync context from Notion / Gmail (and refresh INDEX.md) | `/context-sync` |
