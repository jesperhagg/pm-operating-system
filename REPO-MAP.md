# PM OS — Repo Map
_Last generated: 2026-06-03 | 34 skills / 6 agents / 0 commands_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `.claude/skills/` | Skills (auto-discovered by Claude Code) | 34 |
| `.claude/agents/` | Chat-persona agents (auto-discovered) | 6 |
| `.claude/commands/` | Slash commands (auto-discovered) | 0 |
| `.claude/context/` | Lazy-loaded reference docs | 3 |
| `.claude/hooks/` | SessionStart + PostToolUse hooks (staleness check, activity log) | 2 |
| `.claude/templates/` | Constraint-layer scaffolding copied by `/scaffold-constraint-layer` | — |
| `example/` | Working consumer-repo scaffold (output of `/context-init`) for local testing | — |

## Skills — `.claude/skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|----------|
| /context-init | `.claude/skills/context-init/SKILL.md` | 382 | Initialize the context/ and tasks/ directory tree in a consumer repo w |
| /context-sync | `.claude/skills/context-sync/SKILL.md` | 248 | Incremental sync of context/ files from Notion, Gmail, and session mem |
| /fetch-context | `.claude/skills/fetch-context/SKILL.md` | 111 | Fetch live product context from the consumer repo's context/ files. Fo |
| /generate-repo-map | `.claude/skills/generate-repo-map/SKILL.md` | 276 | Regenerate REPO-MAP.md as a routing map of the codebase. In the pm-os  |
| /knowledge | `.claude/skills/knowledge/SKILL.md` | 191 | Fetch, store, and review structured knowledge in context/. Manages peo |
| /agent-playbook-update | `.claude/skills/agent-playbook-update/SKILL.md` | 84 | Capture non-obvious knowledge the coding agent uncovered during a sess |
| /encode-constraint | `.claude/skills/encode-constraint/SKILL.md` | 104 | Convert a coding-agent mistake into a permanent constraint — regress |
| /spec-feature | `.claude/skills/spec-feature/SKILL.md` | 150 | Build a feature test-first — convert user-facing acceptance criteria |
| /review-diff | `.claude/skills/review-diff/SKILL.md` | 103 | Review a code diff (working tree, last commit, or PR number) against t |
| /scaffold-constraint-layer | `.claude/skills/scaffold-constraint-layer/SKILL.md` | 145 | One-shot setup of the constraint layer in a consumer product repo. Cop |
| /tech-review | `.claude/skills/tech-review/SKILL.md` | 282 | Audit code and architecture across six lenses (simplify, cost, perform |
| /break-down | `.claude/skills/break-down/SKILL.md` | 104 | Break down a PRD or feature idea into kanban-ready work items. Reads c |
| /cohort-analysis | `.claude/skills/cohort-analysis/SKILL.md` | 231 | Structure a cohort analysis — pick the cohort axis, the metric, the  |
| /design-experiment | `.claude/skills/design-experiment/SKILL.md` | 182 | Structure a fast, falsifiable experiment to validate a hypothesis. For |
| /log-interaction | `.claude/skills/log-interaction/SKILL.md` | 108 | Append a dated interaction (email, reply, call, demo, meeting) to an e |
| /log-lead | `.claude/skills/log-lead/SKILL.md` | 100 | Log a new prospect or customer to context/ops/leads-detail/ as a markd |
| /log-signal | `.claude/skills/log-signal/SKILL.md` | 134 | Log a time-stamped observation to context/market/signals.md or context |
| /market-scan | `.claude/skills/market-scan/SKILL.md` | 235 | Scan the competitive landscape for the product, discovering active com |
| /pipeline | `.claude/skills/pipeline/SKILL.md` | 159 | Read-only view of the sales pipeline from data/leads/. Groups leads by |
| /memory-review | `.claude/skills/memory-review/SKILL.md` | 17 | Deprecated. Use /context-sync instead. |
| /migrate-from-notion | `.claude/skills/migrate-from-notion/SKILL.md` | 15 | Deprecated. Use /context-init + /context-sync instead. |
| /pm-digest | `.claude/skills/pm-digest/SKILL.md` | 154 | Search the web for the latest PM + AI news, discussions, and best prac |
| /sunset-product | `.claude/skills/sunset-product/SKILL.md` | 175 | Guided kill-or-park workflow for a product or bet that isn't working.  |
| /tasks | `.claude/skills/tasks/SKILL.md` | 133 | Surface active tasks from tasks/active.md with sprint-style formatting |
| /weekly-review | `.claude/skills/weekly-review/SKILL.md` | 161 | Run a weekly review — single-product (default) or portfolio (across  |
| /pm-init | `.claude/skills/pm-init/SKILL.md` | 10 | Deprecated. Use /context-init instead. |
| /define-persona | `.claude/skills/define-persona/SKILL.md` | 164 | Define a customer persona grounded in real evidence — not demographi |
| /evaluate-opportunity | `.claude/skills/evaluate-opportunity/SKILL.md` | 219 | Evaluate a startup or product opportunity from a solo-founder / indie- |
| /ideal-customer-profile | `.claude/skills/ideal-customer-profile/SKILL.md` | 314 | Define an Ideal Customer Profile — the segment to sell to — across |
| /lean-canvas | `.claude/skills/lean-canvas/SKILL.md` | 287 | Produce a Lean Canvas — 9 boxes on one page covering Problem, Custom |
| /log-decision | `.claude/skills/log-decision/SKILL.md` | 99 | Log a product decision to context/product/decisions.md as an H2 block  |
| /north-star-metric | `.claude/skills/north-star-metric/SKILL.md` | 249 | Pick a North Star Metric using 5 sharpness tests (user-value-aligned,  |
| /pricing | `.claude/skills/pricing/SKILL.md` | 227 | Structure a pricing decision. Picks a value metric, sets an anchor pri |
| /write-prd | `.claude/skills/write-prd/SKILL.md` | 160 | Write a Product Requirements Document using opinionated per-section te |

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
| `dev-standards.md` | 268 | Authoring or reviewing skills, agents, commands |

## Hooks — `.claude/hooks/*`

| Hook | Path | Event | Purpose |
|------|------|-------|---------|
| session-start | `.claude/hooks/session-start.sh` | SessionStart | Bash-only context staleness check + recent-activity count |
| activity-log | `.claude/hooks/activity-log.sh` | PostToolUse | Append one JSONL event per skill/agent/file action (audit trail) |

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify a skill | `.claude/skills/<name>/SKILL.md` |
| Modify an agent | `.claude/agents/<name>/AGENT.md` |
| Modify a command | `.claude/commands/<name>.md` |
| Check context schemas (file shapes, routing rubric) | `.claude/context/context-schemas.md` |
| Check skill/agent design patterns | `.claude/context/dev-standards.md` |
| Understand / change the activity log (audit trail) | `.claude/hooks/activity-log.sh` + `.claude/context/dev-standards.md` (§ Observability Layer) |
| Read what skills/agents did | `context/audit/activity-*.jsonl` (consumer repos) or `.claude/logs/` (dev) |
| Modify constraint-layer scaffolding | `.claude/templates/constraint-layer/<file>` |
| Try a skill against seeded data | `cd example && claude` |
| Add a new skill | New `.claude/skills/<name>/SKILL.md` (auto-discovered) |
| Add a new agent | New `.claude/agents/<name>/AGENT.md` (auto-discovered) |
| Add a new command | New `.claude/commands/<name>.md` (auto-discovered) |
