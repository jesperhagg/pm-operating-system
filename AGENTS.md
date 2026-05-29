# Working With Agents

Agents are **in-chat chat personas** — they give opinionated pushback, not orchestration.
They do not hydrate data, write files, or run workflows. When a task needs methodology, reach
for a **skill** (see `.claude/skills/README.md`); when a strategic question needs a sparring
partner, reach for an **agent**.

> _Note: this is a routed reference. Claude Code auto-reads `CLAUDE.md`, not this file — `CLAUDE.md`
> points here._

## When to invoke which agent

Suggest one when the question is strategic and cross-cutting:

| Trigger | Agent |
|---|---|
| GTM, moat, unit economics, prioritization | `startup-advisor` |
| MVP scoping, feature cuts, backlogs | `product-sculptor` |
| Distribution, funnels, positioning | `growth-engineer` |
| Architecture, technical decisions, cost modeling | `systems-architect` |
| About to patch AI-generated code without encoding the upstream constraint | `constraint-architect` |
| Vertical-specific market dynamics, user psychology, regulation | `domain-expert` |

## Skills vs. agents

- **Skill** = methodology with a defined output (a PRD, a logged decision, a cohort analysis).
  Self-sufficient, four-phase, writes to `context/` or `docs/`.
- **Agent** = a persona you argue with. No output artifact, no file writes.

When a skill exists for the job, invoke the skill — don't improvise the methodology inside an agent.

## Authoring agents

Standards live in `.claude/context/dev-standards.md` (Agent Design Pattern). Hard rules:

- 40–70 lines. Chat persona only — no orchestration, no data hydration, no file writes.
- Required sections: Persona, Decision Principles, Challenge Style, What I Push Back On, Out of Scope.
- Forbidden: Objectives, Proactive Checks, Capabilities tables, Output Format templates,
  Collaboration/Memory protocols.
