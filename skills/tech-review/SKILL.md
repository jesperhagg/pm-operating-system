---
description: Audit code and architecture across six lenses (simplify, cost, performance, scalability, maintenance, security) within a user-specified scope. Produces a prioritized findings report and offers to apply selected fixes surgically.
---

# Tech Review

Distinct from the built-in `/review` (PR-focused), `/simplify` (single-lens),
and `/security-review` (security only). Use this skill for holistic,
scope-targeted audits of arbitrary parts of a product.

## Modes

- **Audit (default)** — Parse scope, review, print prioritized report. Halts
  there.
- **Fix** — Triggered when the user replies to the report with a selection
  (e.g. `all critical`, `1, 3, 5`). Applies only the picked findings.

## Phase 1 — Hydration

### 1.1 Parse inputs

Slash-command form:

```
/tech-review                                    # whole repo, all lenses
/tech-review packages/api                       # path scope, all lenses
/tech-review packages/api security,performance  # path + lens filter
/tech-review . simplify                         # whole repo, single lens
```

- **Arg 1 — scope path** (optional). Default = repo root (`.`). Validate it
  exists; halt with `Scope {path} not found.` if not. A single file is a
  valid scope.
- **Arg 2 — lens filter** (optional). Comma-separated subset of: `simplify`,
  `cost`, `performance`, `scalability`, `maintenance`, `security`. Default =
  all six. Halt on unknown names with the valid list.

Echo the resolved scope and lenses back to the user before proceeding.

### 1.2 Apply exclusions

Always excluded, even if the user names them:

| Excluded | Why |
|---|---|
| `.claude/**` | Skills, agents, commands, hooks — Claude/agent instructions, not product code |
| `data/**` | PM Operating System data store, not product code |
| `node_modules/**`, `dist/**`, `build/**`, `coverage/**`, `.git/**`, `.next/**`, `target/**`, `__pycache__/**`, `.venv/**` | Generated, vendored, or VCS internals |
| `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `uv.lock`, `Gemfile.lock` | Lockfiles — not human-reviewed |
| Top-level `CLAUDE.md` | Agent instruction file |

In-scope: source files (any common extension — `.ts`, `.tsx`, `.js`, `.jsx`,
`.mjs`, `.cjs`, `.py`, `.go`, `.rs`, `.rb`, `.java`, `.kt`, `.swift`, `.cs`,
`.php`, `.json`/`.yaml`/`.toml` configs), plus regular Markdown like
`README.md` and `docs/*.md` (reviewed under the maintenance lens for clarity
/ accuracy).

If the result is empty after exclusions, say
`Nothing to review at {scope} after exclusions.`, list what was excluded, and
halt.

### 1.3 Read context

- **Consumer `CLAUDE.md`** — stack, architecture, domain terms, repo-specific
  invariants. Adapt heuristics below to the actual stack rather than assuming
  Node/TS.
- **Root manifest** + scoped-package manifest (`package.json`,
  `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) — dependencies, scripts,
  workspace layout.
- **Glob the scope** to map what you're about to review. Count source files.
- **Sample siblings.** For path-scoped reviews, skim 1–2 sibling files (e.g.
  the package's `index.*`, an adjacent adapter) so findings reference real
  callers and patterns rather than guesses.

### 1.4 Scale check

If > ~50 source files in scope, stop and propose chunking by package or
directory before continuing. Large reviews lose precision. If the user
insists, switch to **architecture-level observations + a sampled deep dive
on ~10 representative files** rather than silently flattening into shallow
line findings.

## Phase 2 — Framework

For each enabled lens, look for the items below. Quote concrete `file:line`
references in every finding — no hand-wavy claims. Lens content adapts to
the stack identified in hydration; the categories are stack-agnostic.

### Simplify

- Duplication across files; copy-pasted logic that wants extraction (or vice
  versa: an abstraction that exists for one caller).
- Dead code: unused exports, unreachable branches, commented-out blocks.
- Over-abstraction: single-use helpers, premature interfaces, configurability
  with no consumer.
- Convoluted control flow: deep nesting, unnecessary async, redundant guards.

### Cost

- Redundant external API calls (same endpoint hit multiple times per
  request).
- Missing caching for stable data — focus on outbound integrations, adapters,
  or any module that hits a paid upstream.
- Expensive ops on hot paths (sorts, JSON parsing, big regex) where
  avoidable.
- Oversized request/response payloads.
- Idle paid resources (unused service tiers, always-on scheduled jobs).

### Performance

- N+1 fetches; missing batching or parallelization.
- Synchronous I/O on request paths; event-loop / thread blockers.
- Unnecessary serialization round-trips.
- Algorithmic hot spots (quadratic loops over user-controlled data).

### Scalability

- In-process state that should be external (memory caches, counters, locks)
  when the system might run multiple instances.
- Bounded resources without backpressure (connection pools, file handles,
  queues).
- Single-instance assumptions in handlers (timers, leader logic).
- Non-idempotent handlers exposed to retries.
- Missing pagination on list endpoints.

### Maintenance

- Naming clarity; types (flag loose unions, missing return types, untyped
  any-equivalents in the host language).
- Error-handling consistency: where do errors surface? are they typed at
  module boundaries?
- Dependency hygiene: deprecated, unused, duplicated, or unpinned deps.
- Test coverage gaps relevant to the scope (note them; do not write tests).
- Doc accuracy: does in-scope `README.md` / `docs/*.md` still describe
  reality?

### Security

- **Auth surface.** If the scope includes route handlers / endpoints,
  confirm tokens or sessions are *validated*, not just present. Flag any
  handler that accepts a credential without verification, and any
  placeholder/dev-only auth that has not been replaced.
- Input validation and sanitization on every external boundary.
- Secret handling: env var leaks, secrets in logs, secrets committed to
  repo.
- SSRF / injection vectors (especially in adapters that call upstream APIs
  with user-supplied identifiers).
- OWASP Top-10 sweep against the scope.
- **Dependency CVEs:** do not run `npm audit` / `pip-audit` / equivalents
  automatically — call out that the user should run them, and flag any
  obviously outdated security-sensitive deps.

### Severity rubric

| Level | Definition |
|---|---|
| Critical | Security holes, correctness bugs, production breakage risk, data loss potential. Fix before merge. |
| Important | Real tech debt, meaningful perf/cost wins, scaling cliffs that will bite within the next 10× growth. |
| Nice-to-have | Readability, style, minor refactors. |

If a finding's severity is unclear, lean lower and explain the uncertainty —
better to under-flag than cry wolf.

If a finding spans 3+ files or is structural, lift it to **Architecture
observations** instead of a line-anchored finding.

### Effort labels

- **S** — under ~30 minutes, single file.
- **M** — half day, a handful of files.
- **L** — more than a day, or needs a spike before committing to a fix.

## Phase 3 — Output

Print to chat using this template. Do not write to disk unless the user
asks.

```
# Tech Review — {scope} — {today's date}

## Summary
- Files reviewed: {N} (lines: {M})
- Lenses: {comma-separated list}
- Findings: {X} critical, {Y} important, {Z} nice-to-have

## Critical

### [{LENS}] {Short title}
- **Where:** `{path}:L{start}-L{end}`
- **Issue:** {what's wrong, in 1–2 sentences}
- **Recommendation:** {concrete change — alternative API, refactor sketch,
  or "needs spike" if uncertain}
- **Effort:** S / M / L

### ...

## Important

### ...

## Nice-to-have

### ...

## Architecture observations
{Cross-cutting notes that span files: missing layer, leaky abstraction,
drift from a documented adapter pattern, etc. Skip if none.}

## Suggested action plan
{Numbered list of the top 5–7 items, ordered by leverage (impact / effort).}
```

If a lens produced zero findings, omit its findings section but mention it
under Summary so the user knows it was checked.

After the report, prompt:

> Which findings should I fix? (e.g. `all critical`, `1, 3, 5`, `skip`)

### Fix mode

On confirmation, apply only the selected items. Strict rules:

- **Surgical changes only.** Don't refactor adjacent code or improve
  unrelated style. Every changed line must trace to a selected finding.
- **No new abstractions** unless the finding explicitly recommended one and
  the user picked it.
- **No tests** unless the user asks for them.
- **Pause on big blast radius.** If a fix would touch more than ~3 files or
  change a public API, stop and confirm that specific change before
  proceeding.
- **Skip uncertain fixes.** If the recommendation said "needs spike", do not
  guess — leave it for follow-up and note that it was skipped.

After applying, summarize: file count, lines touched, items skipped, and
confirm with the user.

## Phase 4 — Follow-ups

Suggest 1–3 of these, only when contextually relevant:

- Critical security findings → run `/security-review` for a deeper second
  pass over the changed files.
- Architecture-level findings (drift from adapter pattern, missing layer,
  recurring lens hits across runs) → run `/log-decision` to record the
  chosen direction so it's not re-discovered next review.
- Test-coverage gaps surfaced under maintenance → call out explicitly that
  writing tests is out of scope unless requested separately.
- Strategic / cross-cutting architectural questions → consult the
  **systems-architect** agent.

## Anti-patterns

- Don't write the report to disk unless the user asks. Skill prints to
  chat; persistence is a separate ask.
- Don't run `npm audit`, ESLint, type-checkers, or test suites without
  being asked. Point to them in findings instead.
- Don't review excluded paths "just for completeness". Exclusions exist
  because those files aren't product code.
- Don't expand scope mid-review. If something interesting surfaces outside
  the requested scope, mention it under Architecture observations and
  stop.
- Don't hardcode product names, file paths, or stack assumptions. Read
  them from the consumer `CLAUDE.md` during hydration.
