# Skills

PM and dev skills, auto-discovered by Claude Code from `.claude/skills/<name>/SKILL.md`.
Skills are grouped into categories below.

Authoring standards: `.claude/context/dev-standards.md` (Skill Design Pattern). Every skill is
self-sufficient and four-phase: **Hydration → Framework → Output → Follow-ups**. The framework
section is the IP — if it reads like generic advice, it's not a skill.

## Packages

### Context & repo infra
| Skill | Purpose |
|---|---|
| `/context-init` | Initialize `context/` + `tasks/` tree in a repo (replaces `/pm-init`) |
| `/context-sync` | Incremental sync of `context/` from Notion, Gmail, session memory |
| `/fetch-context` | Foundation: hydrate live product context for other skills |
| `/knowledge` | Fetch/store/review structured knowledge (people, research, strategy) |
| `/generate-repo-map` | Regenerate `REPO-MAP.md` after adding/removing/renaming skills or agents |

### Strategy & definition
| Skill | Purpose |
|---|---|
| `/write-prd` | Write a PRD with falsifiable hypotheses and measurable metrics |
| `/lean-canvas` | 9-box Lean Canvas, each box evidence-cited or marked untested |
| `/north-star-metric` | Pick an NSM via 5 sharpness tests + input metrics + kill-criterion |
| `/define-persona` | Evidence-grounded persona (JTBD, pain, workaround, trigger) |
| `/ideal-customer-profile` | ICP across 7 dimensions with disqualifiers + fit rubric |
| `/pricing` | Value metric, anchor price, tiers, WTP validation test |
| `/evaluate-opportunity` | Score an opportunity (market/competition/fit/feasibility) + GTM options |
| `/log-decision` | Log a product decision as an H2 block in `decisions.md` |

### Discovery & experiments
| Skill | Purpose |
|---|---|
| `/design-experiment` | Falsifiable experiment with a decision rule set before it runs |
| `/cohort-analysis` | Cohort axis, metric, window, actionable threshold |
| `/break-down` | Decompose a PRD/feature into kanban-ready work items (JTBD) |

### Market & pipeline
| Skill | Purpose |
|---|---|
| `/market-scan` | Scan competitive landscape; dual-write to `landscape.md` + `signals.md` |
| `/log-signal` | Log a time-stamped observation to `signals.md` or `feedback.md` |
| `/log-lead` | Log a new prospect to the outbound pipeline |
| `/log-interaction` | Append a dated interaction to an existing lead |
| `/pipeline` | Read-only pipeline view; flags overdue follow-ups and stale contacts |

### Cadence & portfolio
| Skill | Purpose |
|---|---|
| `/weekly-review` | Weekly review (single-product or portfolio) → one-page focus plan |
| `/sunset-product` | Guided kill-or-park workflow; capture lesson, log, archive |
| `/pm-digest` | Web search → structured PM + AI digest (uses Tavily) |
| `/tasks` | Surface/update/add active tasks from `tasks/active.md` |

### Dev & constraint layer
| Skill | Purpose |
|---|---|
| `/scaffold-constraint-layer` | One-shot constraint-layer setup (docs, CI gate, PR template) |
| `/encode-constraint` | Convert a coding-agent mistake into a permanent constraint |
| `/agent-playbook-update` | Capture non-obvious repo knowledge into `docs/agent-playbook.md` |
| `/review-diff` | Review a diff against the constraint layer (accept/reject) |
| `/tech-review` | Audit code/architecture across six lenses, apply fixes surgically |

**Deprecated stubs** (kept at their old names, they print a redirect): `/pm-init` → `/context-init`,
`/migrate-from-notion` → `/context-init` + `/context-sync`, `/memory-review` → `/context-sync`.

## When to run what

New product repo, recommended order: `/context-init` → `/scaffold-constraint-layer` → product work.
During work: `/encode-constraint` on every recurring mistake, `/review-diff` on every diff,
`/agent-playbook-update` when a session uncovers something non-obvious. After adding/removing/renaming
any skill or agent: `/generate-repo-map`.

## Local testing loop

This repo doubles as a working consumer scaffold (`example/`, with `.claude` symlinked to `../.claude`):

```bash
cd example
claude    # opens Claude Code with .claude/ resolved via the symlink
```

Try `/log-decision`, `/log-signal`, `/tasks add "..."`, `/market-scan`. Writes land in
`example/context/...` and `example/tasks/...`, not at the repo root. Revert seed writes before committing
template changes: `git checkout -- example/`.
