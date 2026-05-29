## This Repo

This repo serves two roles:

1. **Canonical source of pm-os** — a framework of PM skills, agents, and reference docs that lives under `.claude/`. To install in your own product repo, copy or git-submodule this repo's `.claude/` directory into your repo's `.claude/`. Claude Code auto-discovers everything from there.
2. **Working example consumer repo** — `example/` is a seeded product directory (the exact output of `/context-init`) so you can `cd example && claude` and exercise the skills end-to-end against realistic file shapes without leaving the repo. `example/.claude` is a symlink to `../.claude` so the skills are auto-discovered there too.

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

Full standards in `.claude/context/dev-standards.md`. Key constraints:

**Skills:**
- Self-sufficient. Four-phase execution: Hydration → Framework → Output → Follow-ups.
- The framework section is the IP. If it reads like generic advice, it's not a skill.
- Follow-ups must reference real skill names with slash-command syntax.

**Agents:**
- 40–70 lines. Chat personas only — no orchestration, no data hydration, no file writes.
- Required sections: Persona, Decision Principles, Challenge Style, What I Push Back On, Out of Scope.
- Forbidden sections: Objectives, Proactive Checks, Capabilities tables, Output Format templates, Collaboration/Memory protocols.

**Product-agnostic principle:**
- Skills must work for any product. The seed data under `example/` is empty scaffolding only — no invented decisions, signals, or personas. Skills read `context/` and `tasks/` at runtime from the cwd (which is `example/` when testing, or the consumer repo root in production).
- Litmus test: "Would this skill work identically for a different product with different `context/` content?" If not, it's not product-agnostic.

**Layout:**
- Skills live in `.claude/skills/`, agents in `.claude/agents/`, commands in `.claude/commands/` (none yet).
- Reference docs in `.claude/context/`. Constraint-layer scaffolding (copied into product repos by `/scaffold-constraint-layer`) lives in `template/constraint-layer/`.
- `example/` is the consumer-repo scaffold. Don't put product data there — only the empty file shapes `/context-init` produces.

## Dev — When to Run What

Skills available in this repo:

| Skill | When to use |
|---|---|
| `/generate-repo-map` | After adding, removing, or renaming any skill or agent — regenerates `REPO-MAP.md` |
| `/pm-digest` | Search web for PM + AI news and produce a structured digest (uses Tavily) |
| `/context-init` | Initialize `context/` + `tasks/` in a new product repo (replaces `/pm-init`) |
| `/context-sync` | Incremental sync of `context/` from Notion, Gmail, and session memory |
| `/migrate-from-notion` | Legacy — one-shot migration into old `data/` layout; use `/context-init` + `/context-sync` for new repos |
| `/scaffold-constraint-layer` | One-shot setup of `docs/agent-playbook.md`, `docs/conventions.md`, `docs/architecture.md`, CI gate, and PR template in a product repo. Run once, after `/context-init`. |
| `/encode-constraint` | The central loop. Convert a coding-agent mistake into a permanent test, lint, conventions entry, playbook note, or review-agent prompt. Run on every recurring mistake. |
| `/agent-playbook-update` | Capture non-obvious repo knowledge the agent uncovered (where creds live, a quirk) into `docs/agent-playbook.md` so the next session inherits it. |
| `/review-diff` | Mechanically review a diff against the constraint layer (conventions/playbook/architecture). Runs locally before commit and as the review-agent CI workflow on PR. |

Recommended order in a new product repo: `/context-init` → `/scaffold-constraint-layer` → product work. During work: `/encode-constraint` on every mistake, `/review-diff` on every diff, `/agent-playbook-update` when a session uncovers something non-obvious.

## Dev — Local Testing Loop

Because this repo is also a working consumer scaffold, you can exercise skills here without setting up a separate product repo:

```bash
cd example
claude                       # opens Claude Code with .claude/ resolved via symlink
```

Then try `/log-decision`, `/log-signal`, `/tasks add "..."`, `/market-scan`, etc. Writes land in `example/context/...` and `example/tasks/...`, not at the repo root. Before committing template changes, reset the seed files in `example/` if any test runs wrote into them (e.g. `git checkout -- example/`).

## Dev — Before Committing

Before committing changes to `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`:

1. `git diff --stat HEAD` — confirm scope of changes.
2. Verify against `.claude/context/dev-standards.md` (Skill Design Pattern, Agent Design Pattern, etc.).
3. If multiple skills/agents changed, check cross-file consistency and follow-up references.
4. Run `/generate-repo-map` if files were added or removed.
5. If you used `example/` to test, run `git status example/` and revert any writes that shouldn't ship as part of the empty scaffold.

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
- About to patch AI-generated code without encoding the upstream constraint → `constraint-architect`
