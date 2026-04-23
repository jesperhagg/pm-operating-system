## This Repo

This is the **pm-os submodule** — a framework of 19 PM skills and 4 agents delivered as a git submodule to consumer repos. Dev work here means authoring or modifying skills, agents, commands, and submodule infrastructure.

This is **not** a product repo. There is no `data/` directory here and none should be created. Product data lives in consumer repos at runtime.

When scope is unclear, read `REPO-MAP.md` first.

## How to Work With Me

**Default behavior:**

- Be direct. No preamble, no filler, no encouragement padding.
- Default to action: suggest the next concrete step, not a menu.
- One focused clarifying question when stuck — not a list of five.
- State tradeoffs explicitly when recommending.
- Challenge weak reasoning with specifics, not generic pushback.
- Think before coding. State the plan in one or two sentences, then execute.
- Make surgical changes. Don't refactor what wasn't asked.
- Simpler beats clever. If the solution takes more than a paragraph to explain, it's probably wrong.
- Skills own methodology. Agents give opinionated in-chat pushback. When a skill exists, invoke it — don't improvise.

**Don't:**

- Write files, create PRs, or take irreversible actions without asking.
- Hardcode product names, personas, or features into skills or agents.
- Recommend capabilities I already have (check `REPO-MAP.md`).
- Ask questions inferrable from context.

## Dev — Architecture

Full standards in `context/dev-standards.md`. Key constraints:

**Skills:**
- Self-sufficient. Four-phase execution: Hydration → Framework → Output → Follow-ups.
- The framework section is the IP. If it reads like generic advice, it's not a skill.
- Follow-ups must reference real skill names with slash-command syntax.

**Agents:**
- 40–70 lines. Chat personas only — no orchestration, no data hydration, no file writes.
- Required sections: Persona, Decision Principles, Challenge Style, What I Push Back On, Out of Scope.
- Forbidden sections: Objectives, Proactive Checks, Capabilities tables, Output Format templates, Collaboration/Memory protocols.

**Product-agnostic principle:**
- Zero product data in this repo. Skills read `data/` at runtime from the consumer repo.
- Litmus test: "Would this skill work identically for a different product with different `data/`?" If not, it's not product-agnostic.

**Submodule layout:**
- In this repo, skills live in `skills/`, agents in `agents/`, commands in `commands/`.
- In consumer repos (where this is mounted at `.claude/`), they appear at `.claude/skills/`, `.claude/agents/`, `.claude/commands/` and are auto-discovered by Claude Code.

## Dev — When to Run What

Skills available in this repo:

| Skill | When to use |
|---|---|
| `/generate-repo-map` | After adding, removing, or renaming any skill or agent — regenerates `REPO-MAP.md` |
| `/pm-digest` | Search web for PM + AI news and produce a structured digest (uses Tavily) |
| `/migrate-from-notion` | One-shot migration of legacy Notion product data into a consumer repo's `data/` layout |
| `/update-submodule` | Update this submodule to latest in a consumer repo |

## Dev — Before Committing

Before committing changes to `skills/`, `agents/`, or `commands/`:

1. `git diff --stat HEAD` — confirm scope of changes.
2. Verify against `context/dev-standards.md` (Skill Design Pattern, Agent Design Pattern, etc.).
3. If multiple skills/agents changed, check cross-file consistency and follow-up references.
4. Run `/generate-repo-map` if files were added or removed.

## Consumer Repo Setup

Add this repo as a submodule at `.claude/` in the consumer repo:

```bash
git submodule add git@github.com:jesperhagg/pm-operating-system.git .claude
git submodule update --init
```

Claude Code then discovers skills, agents, and commands directly from `.claude/` — no symlinks needed. The consumer repo keeps its own `CLAUDE.md` at root with product context and its `data/` directory for product data.

To auto-update the submodule on session start, add to global `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "git submodule update --remote --merge .claude" }] }]
  }
}
```

## MCP Usage

| Server | Purpose | If unavailable |
|---|---|---|
| Tavily | Web search + extraction (used by `/pm-digest`) | Graceful — skip web sections, note limitation |

## Agent Escalation

Agents are in-chat chat personas (pushback, not orchestration). Suggest one when the question is strategic and cross-cutting:

- GTM, moat, unit economics → `startup-advisor`
- MVP scoping, feature cuts, backlogs → `product-sculptor`
- Distribution, funnels, positioning → `growth-engineer`
- Architecture, technical decisions, cost modeling → `systems-architect`
