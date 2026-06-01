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
│   ├── templates/        # constraint-layer scaffolding copied by /dev-scaffold-constraint-layer
│   │   └── constraint-layer/ #  docs/, CI workflows (ci.yml + per-stack), PR template, CLAUDE.md fragment
│   ├── settings.json
│   └── .mcp.json.example
├── .github/              # this repo's own Gate: workflows/ci.yml, workflows/review-agent.yml, PR template
├── docs/                 # coding-side guides: engineering, architecture, conventions, agent-playbook
├── example/              # working consumer scaffold — output of /ctx-context-init
│   ├── .claude → ../.claude
│   ├── context/          # product/, market/, users/, ops/, learnings/ (empty seed files)
│   └── tasks/            # active.md, done.md
├── AGENTS.md             # how to work with / when to invoke agents
├── CLAUDE.md             # purpose + routing index (entry point)
└── REPO-MAP.md           # generated index of skills/agents/commands/reference docs
```

## Architecture

The repo carries two systems in one tree, separated by audience, and a routing layer on top.

```
┌─────────────────────────────────────────────────────────────────────┐
│ ROUTER          CLAUDE.md · AGENTS.md · REPO-MAP.md                   │
│                 entry point + when-to-use-what index                  │
├──────────────────────────────────┬──────────────────────────────────┤
│ PM OPERATING SYSTEM              │ PRODUCT CODEBASE                   │
│ (.claude/)                       │ (docs/ + app code, when it lands)  │
│                                  │                                    │
│ skills/   methodology, run via   │ docs/engineering.md  principles    │
│           /<skill-name>          │ docs/architecture.md system map    │
│ agents/   in-chat pushback       │ docs/conventions.md  house style   │
│ hooks/    SessionStart, activity │ docs/agent-playbook.md  run + gotchas│
│ templates/ constraint-layer seed │ .github/  CI + review-agent + PR    │
│ context/  authoring standards    │                                    │
│           (dev-standards,        │ governed by the CONSTRAINT LAYER ──┐│
│            context-schemas)      │                                    ││
├──────────────────────────────────┴────────────────────────────────┐ ││
│ DATA (per product repo, written by skills — never hardcoded)        │ ││
│ context/  product· market· users· ops· learnings                    │ ││
│ tasks/    active· done                                              │ ││
└─────────────────────────────────────────────────────────────────────┘ │
                                                                          │
   The constraint layer (below) is what governs the product codebase ◄────┘
```

**Two modes of work.** *PM workflows* invoke a skill (strategy, discovery, GTM, cadence) that reads
and writes structured markdown in `context/` + `tasks/`. *Product development* follows `docs/` and is
policed by the constraint layer. Agents are chat personas for pushback — they don't orchestrate, hydrate,
or write files; skills own all methodology.

**Why `.claude/templates/` lives where it does.** pm-os installs into a product repo as `.claude/`
(submodule or copied directory). Anything a downstream repo needs at scaffold time must therefore sit
*inside* `.claude/` — so the constraint-layer seed files live at `.claude/templates/constraint-layer/`,
not at the repo root.

## How the constraint layer works

The constraint layer is what keeps app code high-quality when most of it is written by an agent. It is
three coupled mechanisms — **Playbook**, **Gate**, **Loop** — not a pile of docs.

**1. The Playbook (the rubric).** Three docs the coding agent reads *before* writing code:
`docs/agent-playbook.md` (how to run, where things live, credentials, quirks, hard rules),
`docs/conventions.md` (enforceable house style — the review agent's rubric), and `docs/architecture.md`
(system shape, hot paths, hard constraints).

**2. The Gate (mechanical rejection).** Runs on every PR:
- `.github/workflows/ci.yml` — stack-detecting lint + test. A Python repo runs the python job, a Node
  repo the node job, a polyglot repo both, an empty repo passes as a no-op until code lands. Red CI =
  blocked merge.
- `.github/workflows/review-agent.yml` — runs `/dev-review-diff` against the three docs and comments
  file-anchored findings. Needs a `CLAUDE_CODE_OAUTH_TOKEN` repo secret.
- `.github/pull_request_template.md` — forces every PR to answer **"What test or constraint prevents
  this regression?"** If the answer is "none," the work isn't done.

**3. The Loop (self-improvement).** When the agent makes a mistake you don't patch the code first — you
encode the constraint first via `/dev-encode-constraint`, which walks a first-match-wins rubric and
writes the strongest artifact that catches the *class* of mistake:

| The mistake is… | Artifact | Where |
|---|---|---|
| detectable in test output | regression test | `tests/` |
| a static pattern (banned call, naming) | lint rule | `ruff.toml` / `.eslintrc.json` |
| explicit house style, hard to lint | convention entry | `docs/conventions.md` |
| missing knowledge the agent should have had | playbook note | `docs/agent-playbook.md` |
| a judgment call only a reviewer makes | review-agent prompt | `docs/conventions.md` (review rubric) |

Strength order: **test > lint > convention > playbook > review-prompt.** Then you re-run the original
task — the next attempt is blocked by the constraint, not a human. `/dev-agent-playbook-update` is the
softer cousin for *missing knowledge* rather than coding mistakes. The slogan: **the repo teaches the
agent — the agent doesn't memorize the repo.**

**A typical dev task** therefore flows: hydrate (read the three docs) → implement surgically → self-review
with `/dev-review-diff` → push → Gate re-checks on PR (CI + review-agent) → if anything slips through,
`/dev-encode-constraint` ratchets the bar up so it can't recur.

**Identifying a constraint-layer gap.** A gap is a class of mistake the layer *should* have caught but
didn't — the rubric never encoded the rule. The tells: `/dev-review-diff` comes back clean yet something
is still wrong on read; the same class of mistake recurs across diffs; a bug reaches `main` with green CI;
or a reviewer flags something no test, lint, or convention names. The fix is never a one-off patch — it's
`/dev-encode-constraint` to add the missing test/lint/convention, then re-run `/dev-review-diff` so the
next diff of that class is caught mechanically. (See the "Constraint Layer" section in `CLAUDE.md`.)

> **This repo is dual-purpose.** Because it *hosts* pm-os, `/dev-scaffold-constraint-layer` deliberately
> halts here rather than scaffolding over itself. Its Gate (`.github/`) was therefore installed by hand;
> the Playbook docs in `docs/` are still placeholders to be filled when app code lands.

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
/dev-scaffold-constraint-layer       # scaffolds docs/, CI, PR template from .claude/templates/constraint-layer/
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
