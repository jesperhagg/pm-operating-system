# PM OS — Repo Map
_Last generated: 2026-04-15 | 11 exported skills / 4 internal skills / 5 agents_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `skills/` | Exported skills (available in consumer repos via plugin) | 11 |
| `.claude/skills/` | Internal skills (this repo only) | 4 |
| `.claude/agents/` | Agents | 5 |
| `.claude/context/` | Lazy-loaded reference docs | 2 |
| `.claude-plugin/` | plugin.json (manifest), marketplace.json | 2 |

## Exported Skills — `skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|----------|
| /break-down | `skills/break-down/SKILL.md` | 88 | Break down a PRD or feature idea into kanban-ready work items. Fetches |
| /evaluate-opportunity | `skills/evaluate-opportunity/SKILL.md` | 55 | Evaluate a startup or product opportunity against strategic criteria.  |
| /fetch-context | `skills/fetch-context/SKILL.md` | 74 | Fetch live product context from Notion. Foundation skill used by other |
| /knowledge | `skills/knowledge/SKILL.md` | 245 | Fetch, store, and review structured knowledge in Notion. Manages three |
| /log-decision | `skills/log-decision/SKILL.md` | 81 | Log a product decision to Notion and local memory. Captures the decisi |
| /log-signal | `skills/log-signal/SKILL.md` | 137 | Log a time-stamped observation to the Notion Signals database. Capture |
| /market-scan | `skills/market-scan/SKILL.md` | 344 | Scan the competitive landscape for a product, discovering active compe |
| /memory-review | `skills/memory-review/SKILL.md` | 77 | Review memory files across all products and shared memory, identify st |
| /tasks | `skills/tasks/SKILL.md` | 141 | Surface active tasks from the Notion backlog with sprint-style formatt |
| /weekly-review | `skills/weekly-review/SKILL.md` | 124 | Run a portfolio-level weekly review across all products. Reads memory, |
| /write-prd | `skills/write-prd/SKILL.md` | 62 | Write a Product Requirements Document using proven PM frameworks. Auto |

## Internal Skills — `.claude/skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|----------|
| /design-review | `.claude/skills/design-review/SKILL.md` | 123 | Pre-ship review gate that runs pm-os-creator analysis on pending chang |
| /generate-repo-map | `.claude/skills/generate-repo-map/SKILL.md` | 114 | Regenerate .claude/REPO-MAP.md by scanning current skills, agents, and |
| /pm-digest | `.claude/skills/pm-digest/SKILL.md` | 154 | Search the web for the latest PM + AI news, discussions, and best prac |
| /skill-eval | `.claude/skills/skill-eval/SKILL.md` | 224 | Evaluate a skill or agent against PM OS design standards. Grades on pa |

## Agents — `.claude/agents/*/AGENT.md`

| Agent | Path | Lines | Domain |
|-------|------|-------|--------|
| growth-engineer | `.claude/agents/growth-engineer/AGENT.md` | 312 | Distribution-first growth specialist. Advisory by default, produces co |
| pm-os-creator | `.claude/agents/pm-os-creator/AGENT.md` | 189 | Meta-agent for developing the PM Operating System repo. Expert on Clau |
| product-sculptor | `.claude/agents/product-sculptor/AGENT.md` | 297 | Minimalist PM who sculpts MVPs to their atomic core. Obsessed with Tim |
| startup-advisor | `.claude/agents/startup-advisor/AGENT.md` | 313 | Analytical startup advisor (YC + McKinsey lens). Challenges assumption |
| systems-architect | `.claude/agents/systems-architect/AGENT.md` | 338 | Senior technical architect for product systems. Architecture only —  |

## Reference Docs — `.claude/context/`

| File | Lines | Load when |
|------|-------|----------|
| `dev-standards.md` | 180 | Authoring or reviewing skills, agents, plugin infrastructure |
| `notion-schemas.md` | 142 | Writing to Notion (Decisions, Signals, KB, Tasks) |

## When You Need To...

| Task | File to read/edit |
|------|-------------------|
| Modify an exported skill | `skills/<name>/SKILL.md` |
| Modify an internal skill | `.claude/skills/<name>/SKILL.md` |
| Modify an agent | `.claude/agents/<name>/AGENT.md` |
| Update plugin export list | `.claude-plugin/plugin.json` |
| Check Notion DB schemas + routing rubric | `.claude/context/notion-schemas.md` |
| Check skill design patterns + conventions | `.claude/context/dev-standards.md` |
| Add a new exported skill | New `skills/<name>/SKILL.md` + add entry to `plugin.json` |
| Add a new internal skill | New `.claude/skills/<name>/SKILL.md` (no plugin.json update) |
| Add a new agent | New `.claude/agents/<name>/AGENT.md` (no plugin.json update) |
| Update marketplace listing | `.claude-plugin/marketplace.json` (major releases only) |
