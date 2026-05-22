## This Repo

This is the **pm-os template** — a framework of PM skills and agents you copy into each new product repo as the `.claude/` directory. Dev work here means authoring or modifying skills, agents, and commands.

This is **not** a product repo. There is no `data/` or `context/` directory here and none should be created. Product context lives in `context/` and `tasks/` directories created by `/context-init` after the template is copied.

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
- Zero product data in this repo. Skills read `context/` and `tasks/` at runtime from the product repo.
- Litmus test: "Would this skill work identically for a different product with different `context/` content?" If not, it's not product-agnostic.

**Layout:**
- Skills live in `skills/`, agents in `agents/`, commands in `commands/`.
- When copied to a product repo as `.claude/`, they appear at `.claude/skills/`, `.claude/agents/`, `.claude/commands/` and are auto-discovered by Claude Code.

## Dev — When to Run What

Skills available in this repo:

| Skill | When to use |
|---|---|
| `/generate-repo-map` | After adding, removing, or renaming any skill or agent — regenerates `REPO-MAP.md` |
| `/pm-digest` | Search web for PM + AI news and produce a structured digest (uses Tavily) |
| `/context-init` | Initialize `context/` + `tasks/` in a new product repo (replaces `/pm-init`) |
| `/context-sync` | Incremental sync of `context/` from Notion, Gmail, and session memory |
| `/migrate-from-notion` | Legacy — one-shot migration into old `data/` layout; use `/context-init` + `/context-sync` for new repos |

## Dev — Before Committing

Before committing changes to `skills/`, `agents/`, or `commands/`:

1. `git diff --stat HEAD` — confirm scope of changes.
2. Verify against `context/dev-standards.md` (Skill Design Pattern, Agent Design Pattern, etc.).
3. If multiple skills/agents changed, check cross-file consistency and follow-up references.
4. Run `/generate-repo-map` if files were added or removed.

## New Product Repo Setup

Copy this template as the `.claude/` directory in a new product repo:

```bash
cp -r pm-operating-system/ my-product/.claude/
```

Claude Code then discovers skills, agents, and commands directly from `.claude/` — no symlinks needed. The product repo keeps its own `CLAUDE.md` at root with product context, `context/` for the knowledge wiki, and `tasks/` for operational artifacts. Run `/context-init` to scaffold the `context/` and `tasks/` directories.

## MCP Usage

| Server | Purpose | If unavailable |
|---|---|---|
| Tavily | Web search + extraction (used by `/pm-digest`, `/market-scan`) | Graceful — skip web sections, note limitation |
| Notion | Context sync from Notion DBs (used by `/context-sync`, `/context-init`) | Graceful — skip Notion source, note limitation |
| Gmail | Context sync from email threads (used by `/context-sync`) | Graceful — skip Gmail source, note limitation |

## Agent Escalation

Agents are in-chat chat personas (pushback, not orchestration). Suggest one when the question is strategic and cross-cutting:

- GTM, moat, unit economics → `startup-advisor`
- MVP scoping, feature cuts, backlogs → `product-sculptor`
- Distribution, funnels, positioning → `growth-engineer`
- Architecture, technical decisions, cost modeling → `systems-architect`
