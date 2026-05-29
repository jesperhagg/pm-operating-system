# PM OS — Repo Map
_Last generated: 2026-05-29 | 33 skills / 6 agents / 0 commands_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `.claude/skills/` | Skills (auto-discovered by Claude Code) | 33 |
| `.claude/agents/` | Chat-persona agents (auto-discovered) | 6 |
| `.claude/commands/` | Slash commands (auto-discovered) | 0 |
| `.claude/context/` | Lazy-loaded reference docs | 3 |
| `template/` | Constraint-layer scaffolding copied by `/dev-scaffold-constraint-layer` | — |
| `example/` | Working consumer-repo scaffold (output of `/ctx-context-init`) for local testing | — |

## Skills — `.claude/skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|----------|
| /ctx-context-init | `.claude/skills/ctx-context-init/SKILL.md` | 341 | Initialize the context/ and tasks/ directory tree in a consumer repo w |
| /ctx-context-sync | `.claude/skills/ctx-context-sync/SKILL.md` | 248 | Incremental sync of context/ files from Notion, Gmail, and session mem |
| /ctx-fetch-context | `.claude/skills/ctx-fetch-context/SKILL.md` | 111 | Fetch live product context from the consumer repo's context/ files. Fo |
| /ctx-generate-repo-map | `.claude/skills/ctx-generate-repo-map/SKILL.md` | 276 | Regenerate REPO-MAP.md as a routing map of the codebase. In the pm-os  |
| /ctx-knowledge | `.claude/skills/ctx-knowledge/SKILL.md` | 191 | Fetch, store, and review structured knowledge in context/. Manages peo |
| /dev-agent-playbook-update | `.claude/skills/dev-agent-playbook-update/SKILL.md` | 84 | Capture non-obvious knowledge the coding agent uncovered during a sess |
| /dev-encode-constraint | `.claude/skills/dev-encode-constraint/SKILL.md` | 104 | Convert a coding-agent mistake into a permanent constraint — regress |
| /dev-review-diff | `.claude/skills/dev-review-diff/SKILL.md` | 103 | Review a code diff (working tree, last commit, or PR number) against t |
| /dev-scaffold-constraint-layer | `.claude/skills/dev-scaffold-constraint-layer/SKILL.md` | 145 | One-shot setup of the constraint layer in a consumer product repo. Cop |
| /dev-tech-review | `.claude/skills/dev-tech-review/SKILL.md` | 282 | Audit code and architecture across six lenses (simplify, cost, perform |
| /disc-break-down | `.claude/skills/disc-break-down/SKILL.md` | 104 | Break down a PRD or feature idea into kanban-ready work items. Reads c |
| /disc-cohort-analysis | `.claude/skills/disc-cohort-analysis/SKILL.md` | 231 | Structure a cohort analysis — pick the cohort axis, the metric, the  |
| /disc-design-experiment | `.claude/skills/disc-design-experiment/SKILL.md` | 182 | Structure a fast, falsifiable experiment to validate a hypothesis. For |
| /gtm-log-interaction | `.claude/skills/gtm-log-interaction/SKILL.md` | 108 | Append a dated interaction (email, reply, call, demo, meeting) to an e |
| /gtm-log-lead | `.claude/skills/gtm-log-lead/SKILL.md` | 100 | Log a new prospect or customer to context/ops/leads-detail/ as a markd |
| /gtm-log-signal | `.claude/skills/gtm-log-signal/SKILL.md` | 134 | Log a time-stamped observation to context/market/signals.md or context |
| /gtm-market-scan | `.claude/skills/gtm-market-scan/SKILL.md` | 235 | Scan the competitive landscape for the product, discovering active com |
| /gtm-pipeline | `.claude/skills/gtm-pipeline/SKILL.md` | 159 | Read-only view of the sales pipeline from data/leads/. Groups leads by |
| /memory-review | `.claude/skills/memory-review/SKILL.md` | 17 | Deprecated. Use /ctx-context-sync instead. |
| /migrate-from-notion | `.claude/skills/migrate-from-notion/SKILL.md` | 15 | Deprecated. Use /ctx-context-init + /ctx-context-sync instead. |
| /ops-pm-digest | `.claude/skills/ops-pm-digest/SKILL.md` | 154 | Search the web for the latest PM + AI news, discussions, and best prac |
| /ops-sunset-product | `.claude/skills/ops-sunset-product/SKILL.md` | 175 | Guided kill-or-park workflow for a product or bet that isn't working.  |
| /ops-tasks | `.claude/skills/ops-tasks/SKILL.md` | 133 | Surface active tasks from tasks/active.md with sprint-style formatting |
| /ops-weekly-review | `.claude/skills/ops-weekly-review/SKILL.md` | 161 | Run a weekly review — single-product (default) or portfolio (across  |
| /pm-init | `.claude/skills/pm-init/SKILL.md` | 10 | Deprecated. Use /ctx-context-init instead. |
| /strat-define-persona | `.claude/skills/strat-define-persona/SKILL.md` | 164 | Define a customer persona grounded in real evidence — not demographi |
| /strat-evaluate-opportunity | `.claude/skills/strat-evaluate-opportunity/SKILL.md` | 219 | Evaluate a startup or product opportunity from a solo-founder / indie- |
| /strat-ideal-customer-profile | `.claude/skills/strat-ideal-customer-profile/SKILL.md` | 314 | Define an Ideal Customer Profile — the segment to sell to — across |
| /strat-lean-canvas | `.claude/skills/strat-lean-canvas/SKILL.md` | 287 | Produce a Lean Canvas — 9 boxes on one page covering Problem, Custom |
| /strat-log-decision | `.claude/skills/strat-log-decision/SKILL.md` | 99 | Log a product decision to context/product/decisions.md as an H2 block  |
| /strat-north-star-metric | `.claude/skills/strat-north-star-metric/SKILL.md` | 249 | Pick a North Star Metric using 5 sharpness tests (user-value-aligned,  |
| /strat-pricing | `.claude/skills/strat-pricing/SKILL.md` | 227 | Structure a pricing decision. Picks a value metric, sets an anchor pri |
| /strat-write-prd | `.claude/skills/strat-write-prd/SKILL.md` | 160 | Write a Product Requirements Document using opinionated per-section te |

## Agents — `.claude/agents/*/AGENT.md`

| Agent | Path | Lines | Domain |
|-------|------|-------|--------|
| constraint-architect | `.claude/agents/constraint-architect/AGENT.md` | 36 | Pushes back when work would be done without first encoding the constra |
| domain-expert | `.claude/agents/domain-expert/AGENT.md` | 38 | Veteran practitioner in whatever industry the consumer repo operates i |
| growth-engineer | `.claude/agents/growth-engineer/AGENT.md` | 38 | Distribution-first growth specialist. Advisory by default, produces co |
| product-sculptor | `.claude/agents/product-sculptor/AGENT.md` | 36 | Minimalist PM who sculpts MVPs to their atomic core. Obsessed with Tim |
| startup-advisor | `.claude/agents/startup-advisor/AGENT.md` | 37 | Analytical startup advisor (YC + McKinsey lens). Pressure-tests GTM, m |
| systems-architect | `.claude/agents/systems-architect/AGENT.md` | 42 | Senior technical architect for product systems. Architecture only —  |

## Commands — `.claude/commands/*.md`

| Command | Path | Purpose |
|---------|------|----------|

## Reference Docs — `.claude/context/`

| File | Lines | Load when |
|------|-------|----------|
| `context-schemas.md` | 551 | Reading/writing product context/ — file shapes, routing rubric, sync-state |
| `data-schemas.md` | 389 | Legacy — see context-schemas.md instead |
| `dev-standards.md` | 221 | Authoring or reviewing skills, agents, commands |

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify a skill | `.claude/skills/<name>/SKILL.md` |
| Modify an agent | `.claude/agents/<name>/AGENT.md` |
| Modify a command | `.claude/commands/<name>.md` |
| Check context schemas (file shapes, routing rubric) | `.claude/context/context-schemas.md` |
| Check skill/agent design patterns | `.claude/context/dev-standards.md` |
| Modify constraint-layer scaffolding | `template/constraint-layer/<file>` |
| Try a skill against seeded data | `cd example && claude` |
| Add a new skill | New `.claude/skills/<name>/SKILL.md` (auto-discovered) |
| Add a new agent | New `.claude/agents/<name>/AGENT.md` (auto-discovered) |
| Add a new command | New `.claude/commands/<name>.md` (auto-discovered) |
