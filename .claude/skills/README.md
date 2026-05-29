# Skills

PM and dev skills, auto-discovered by Claude Code from `.claude/skills/<name>/SKILL.md`.
Skills are grouped into **packages by name prefix** (Claude Code only discovers skills one
level deep, so packaging is done via the directory-name prefix, not nested folders).

Authoring standards: `.claude/context/dev-standards.md` (Skill Design Pattern). Every skill is
self-sufficient and four-phase: **Hydration → Framework → Output → Follow-ups**. The framework
section is the IP — if it reads like generic advice, it's not a skill.

## Packages

### `ctx-` — Context & repo infra
| Skill | Purpose |
|---|---|
| `/ctx-context-init` | Initialize `context/` + `tasks/` tree in a repo (replaces `/pm-init`) |
| `/ctx-context-sync` | Incremental sync of `context/` from Notion, Gmail, session memory |
| `/ctx-fetch-context` | Foundation: hydrate live product context for other skills |
| `/ctx-knowledge` | Fetch/store/review structured knowledge (people, research, strategy) |
| `/ctx-generate-repo-map` | Regenerate `REPO-MAP.md` after adding/removing/renaming skills or agents |

### `strat-` — Strategy & definition
| Skill | Purpose |
|---|---|
| `/strat-write-prd` | Write a PRD with falsifiable hypotheses and measurable metrics |
| `/strat-lean-canvas` | 9-box Lean Canvas, each box evidence-cited or marked untested |
| `/strat-north-star-metric` | Pick an NSM via 5 sharpness tests + input metrics + kill-criterion |
| `/strat-define-persona` | Evidence-grounded persona (JTBD, pain, workaround, trigger) |
| `/strat-ideal-customer-profile` | ICP across 7 dimensions with disqualifiers + fit rubric |
| `/strat-pricing` | Value metric, anchor price, tiers, WTP validation test |
| `/strat-evaluate-opportunity` | Score an opportunity (market/competition/fit/feasibility) + GTM options |
| `/strat-log-decision` | Log a product decision as an H2 block in `decisions.md` |

### `disc-` — Discovery & experiments
| Skill | Purpose |
|---|---|
| `/disc-design-experiment` | Falsifiable experiment with a decision rule set before it runs |
| `/disc-cohort-analysis` | Cohort axis, metric, window, actionable threshold |
| `/disc-break-down` | Decompose a PRD/feature into kanban-ready work items (JTBD) |

### `gtm-` — Market & pipeline
| Skill | Purpose |
|---|---|
| `/gtm-market-scan` | Scan competitive landscape; dual-write to `landscape.md` + `signals.md` |
| `/gtm-log-signal` | Log a time-stamped observation to `signals.md` or `feedback.md` |
| `/gtm-log-lead` | Log a new prospect to the outbound pipeline |
| `/gtm-log-interaction` | Append a dated interaction to an existing lead |
| `/gtm-pipeline` | Read-only pipeline view; flags overdue follow-ups and stale contacts |

### `ops-` — Cadence & portfolio
| Skill | Purpose |
|---|---|
| `/ops-weekly-review` | Weekly review (single-product or portfolio) → one-page focus plan |
| `/ops-sunset-product` | Guided kill-or-park workflow; capture lesson, log, archive |
| `/ops-pm-digest` | Web search → structured PM + AI digest (uses Tavily) |
| `/ops-tasks` | Surface/update/add active tasks from `tasks/active.md` |

### `dev-` — Dev & constraint layer
| Skill | Purpose |
|---|---|
| `/dev-scaffold-constraint-layer` | One-shot constraint-layer setup (docs, CI gate, PR template) |
| `/dev-encode-constraint` | Convert a coding-agent mistake into a permanent constraint |
| `/dev-agent-playbook-update` | Capture non-obvious repo knowledge into `docs/agent-playbook.md` |
| `/dev-review-diff` | Review a diff against the constraint layer (accept/reject) |
| `/dev-tech-review` | Audit code/architecture across six lenses, apply fixes surgically |

**Deprecated stubs** (kept at their old names, they print a redirect): `/pm-init` → `/ctx-context-init`,
`/migrate-from-notion` → `/ctx-context-init` + `/ctx-context-sync`, `/memory-review` → `/ctx-context-sync`.

## When to run what

New product repo, recommended order: `/ctx-context-init` → `/dev-scaffold-constraint-layer` → product work.
During work: `/dev-encode-constraint` on every recurring mistake, `/dev-review-diff` on every diff,
`/dev-agent-playbook-update` when a session uncovers something non-obvious. After adding/removing/renaming
any skill or agent: `/ctx-generate-repo-map`.

## Local testing loop

This repo doubles as a working consumer scaffold (`example/`, with `.claude` symlinked to `../.claude`):

```bash
cd example
claude    # opens Claude Code with .claude/ resolved via the symlink
```

Try `/strat-log-decision`, `/gtm-log-signal`, `/ops-tasks add "..."`, `/gtm-market-scan`. Writes land in
`example/context/...` and `example/tasks/...`, not at the repo root. Revert seed writes before committing
template changes: `git checkout -- example/`.
