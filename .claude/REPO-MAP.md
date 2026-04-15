# PM OS — Repo Map
_Last generated: 2026-04-15 | 11 exported skills / 3 internal skills / 5 agents_

## Structure

| Path | Contains | Count |
|------|----------|-------|
| `skills/` | Exported skills (available in consumer repos via plugin) | 11 |
| `.claude/skills/` | Internal skills (this repo only) | 3 |
| `.claude/agents/` | Agents | 5 |
| `.claude/context/` | Lazy-loaded reference docs | 2 |
| `.claude-plugin/` | plugin.json (manifest), marketplace.json | 2 |

## Exported Skills — `skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|---------|
| /fetch-context | `skills/fetch-context/SKILL.md` | 74 | Foundation skill — hydrates product context from Notion |
| /write-prd | `skills/write-prd/SKILL.md` | 62 | 6-section PRD template |
| /evaluate-opportunity | `skills/evaluate-opportunity/SKILL.md` | 55 | Scores on 5 dimensions → Explore/Park/Kill |
| /market-scan | `skills/market-scan/SKILL.md` | 344 | Competitive scan, dual-writes KB + Signals |
| /break-down | `skills/break-down/SKILL.md` | 88 | Decomposes PRD → kanban tasks via JTBD |
| /weekly-review | `skills/weekly-review/SKILL.md` | 124 | Portfolio operating rhythm, surfaces action-required signals |
| /log-decision | `skills/log-decision/SKILL.md` | 81 | Writes commitment to Notion Decisions DB |
| /log-signal | `skills/log-signal/SKILL.md` | 137 | Writes observation to Notion Signals DB |
| /knowledge | `skills/knowledge/SKILL.md` | 245 | Fetch/Store/Review structured knowledge in Notion KB |
| /tasks | `skills/tasks/SKILL.md` | 141 | Session-start backlog view; sprint-style formatting |
| /memory-review | `skills/memory-review/SKILL.md` | 77 | Curates `.claude/memory/shared.md` for staleness |

## Internal Skills — `.claude/skills/*/SKILL.md`

| Skill | Path | Lines | Purpose |
|-------|------|-------|---------|
| /pm-digest | `.claude/skills/pm-digest/SKILL.md` | 154 | Daily PM + AI news digest via Tavily |
| /design-review | `.claude/skills/design-review/SKILL.md` | 123 | Pre-commit review gate via pm-os-creator |
| /skill-eval | `.claude/skills/skill-eval/SKILL.md` | 224 | Audits skill/agent against design standards |
| /generate-repo-map | `.claude/skills/generate-repo-map/SKILL.md` | — | Regenerates this file |

## Agents — `.claude/agents/*/AGENT.md`

| Agent | Path | Lines | Domain |
|-------|------|-------|--------|
| startup-advisor | `.claude/agents/startup-advisor/AGENT.md` | 313 | GTM, moat, unit economics, prioritization |
| product-sculptor | `.claude/agents/product-sculptor/AGENT.md` | 297 | MVP scoping, feature cuts, backlogs |
| growth-engineer | `.claude/agents/growth-engineer/AGENT.md` | 312 | Distribution, funnels, landing page positioning |
| systems-architect | `.claude/agents/systems-architect/AGENT.md` | 338 | System design, APIs, infrastructure, AI/LLM |
| pm-os-creator | `.claude/agents/pm-os-creator/AGENT.md` | 189 | Meta-architect for this repo |

## Reference Docs — `.claude/context/`

| File | Lines | Load when |
|------|-------|-----------|
| `notion-schemas.md` | 152 | Writing to Notion (Decisions, Signals, KB, Tasks) |
| `dev-standards.md` | 162 | Authoring or reviewing skills, agents, plugin infrastructure |

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
