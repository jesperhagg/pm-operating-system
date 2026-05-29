# PM Operating System

An AI-native product-management OS for Claude Code: a set of PM skills (PRDs, opportunity scoring, market scans, decision logging, weekly reviews) and chat-persona agents (startup-advisor, product-sculptor, growth-engineer, systems-architect) that read and write structured markdown in your product repo. One product per repo — the repo IS the product.

This repo is both the canonical source of pm-os *and* a working example consumer repo, so you can try every skill end-to-end without leaving it.

## Repo layout

```
pm-operating-system/
├── .claude/              # the pm-os payload (skills, agents, hooks, scripts, reference docs)
│   ├── skills/           # 33 skills, prefix-packaged (ctx-/strat-/disc-/gtm-/ops-/dev-); see skills/README.md
│   ├── agents/           # 6 chat-persona agents
│   ├── context/          # reference docs (context-schemas, dev-standards)
│   ├── hooks/            # SessionStart hook
│   ├── scripts/          # generate-repo-map.sh and friends
│   ├── settings.json
│   └── .mcp.json.example
├── docs/                 # coding-side guides: engineering, architecture, conventions, agent-playbook
├── template/             # constraint-layer scaffolding copied by /dev-scaffold-constraint-layer
│   └── constraint-layer/ #   docs/, CI workflows, PR template
├── example/              # working consumer scaffold — output of /ctx-context-init
│   ├── .claude → ../.claude
│   ├── context/          # product/, market/, users/, ops/, learnings/ (empty seed files)
│   └── tasks/            # active.md, done.md
├── AGENTS.md             # how to work with / when to invoke agents
├── CLAUDE.md             # purpose + routing index (entry point)
└── REPO-MAP.md           # generated index of skills/agents/commands/reference docs
```

## Install in your own product repo

Two options — pick one.

**As a git submodule** (recommended; updates with `git submodule update --remote`):

```bash
git submodule add git@github.com:jesperhagg/pm-operating-system.git .claude
git submodule update --init
```

**As a copied directory** (no submodule overhead, but you have to pull updates manually):

```bash
cp -R /path/to/pm-operating-system/.claude /path/to/your-product/.claude
```

Then, from your product repo root:

```bash
/ctx-context-init                    # scaffolds context/ and tasks/
/dev-scaffold-constraint-layer       # scaffolds docs/, CI, PR template from template/constraint-layer/
```

## Try it without leaving this repo

The `example/` directory is a pre-seeded consumer-repo scaffold. Skills can be exercised against it:

```bash
cd example
claude
```

Inside that session, try:

- `/strat-log-decision` — writes an H2 block to `example/context/product/decisions.md`
- `/gtm-log-signal` — appends to `example/context/market/signals.md` or `example/context/users/feedback.md`
- `/ops-tasks add "Spec the onboarding flow"` — appends to `example/tasks/active.md`
- `/gtm-market-scan <topic>` — requires Tavily; writes to `example/context/market/landscape.md`

`example/` ships with empty seed files only (the exact output of `/ctx-context-init`). If a test run writes data you don't want to keep, `git checkout -- example/` resets it.

## Skills (selected)

| Skill | What it does |
|-------|-------------|
| `/ctx-context-init` | Scaffolds `context/` and `tasks/` in a fresh product repo |
| `/ctx-context-sync` | Incremental sync of `context/` from Notion, Gmail, and session memory |
| `/dev-scaffold-constraint-layer` | Sets up `docs/agent-playbook.md`, conventions, architecture, CI, PR template |
| `/ctx-fetch-context` | Hydrates other skills with decisions, personas, recent signals, landscape |
| `/strat-write-prd` | PRD using opinionated per-section templates with falsifiable hypotheses |
| `/strat-evaluate-opportunity` | Scores Market / Competition / Founder Fit / Feasibility from a solo-founder lens |
| `/gtm-market-scan <market>` | Parallel web search → dual-write to `landscape.md` + `signals.md` |
| `/disc-break-down` | Decomposes a PRD into kanban-ready JTBD work items |
| `/strat-log-decision` | H2 block per decision to `context/product/decisions.md` |
| `/gtm-log-signal` | H3 dated observation to signals.md or feedback.md |
| `/gtm-log-lead` / `/gtm-log-interaction` / `/gtm-pipeline` | Outbound pipeline in `context/ops/` |
| `/ops-tasks` | Active backlog (`tasks/active.md`) — Now / Next / Later |
| `/ops-weekly-review` | One-page focus plan from decisions + signals + tasks |
| `/dev-encode-constraint` | Convert a coding-agent mistake into a permanent test/lint/playbook entry |
| `/dev-review-diff` | Mechanical diff review against the constraint layer |
| `/ops-pm-digest` | Daily PM + AI news digest (Tavily) |
| `/ctx-generate-repo-map` | Regenerate `REPO-MAP.md` |

Full list (with line counts and one-line descriptions) lives in `REPO-MAP.md`.

## Agents

In-chat chat personas for strategic pushback — not orchestrators, not file writers.

| Agent | When to invoke |
|-------|------|
| `startup-advisor` | GTM, moat, unit economics |
| `product-sculptor` | MVP scoping, feature cuts, backlogs |
| `growth-engineer` | Distribution, funnels, positioning |
| `systems-architect` | Architecture, technical decisions, cost modeling |
| `constraint-architect` | About to patch AI-generated code without encoding the upstream constraint |
| `domain-expert` | Surfaced when the question is deep in a specific domain |

## MCP servers

Optional but unlock specific skills:

| Server | Used by | Without it |
|---|---|---|
| Tavily | `/gtm-market-scan`, `/ops-pm-digest` | Skills skip web sections and note the limitation |
| Notion | `/ctx-context-sync`, `/ctx-context-init` (Notion migration path) | Notion source is skipped |
| Gmail | `/ctx-context-sync` | Gmail source is skipped |

To configure: copy `.claude/.mcp.json.example` to `.mcp.json` in your product repo, fill in API keys, restart Claude Code.

## Context layout (in your product repo)

After `/ctx-context-init`, your product repo has:

```
context/
├── product/      decisions.md, strategy.md, roadmap.md, experiments.md
├── market/       landscape.md, signals.md, archive/
├── users/        personas.md, feedback.md, research.md, icp.md
├── ops/          people.md, leads.md, leads-detail/{slug}.md
└── learnings/    <skill>.md (per-skill accumulated lessons)
tasks/
├── active.md     Now / Next / Later
└── done.md
```

Full file shapes and routing rubric: `.claude/context/context-schemas.md`.
