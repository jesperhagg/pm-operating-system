---
description: One-shot setup of the constraint layer in a consumer product repo. Copies starter docs (agent-playbook, conventions, architecture) into docs/, drops a stack-appropriate CI workflow + PR template, and injects a Constraint Layer section into the product repo's CLAUDE.md. Run once per product repo, after /ctx-context-init. Idempotent — skips files that already exist.
---

# Scaffold Constraint Layer

Sets up the **constraint layer** in a consumer product repo: the docs the coding agent reads first, the CI gate that mechanically rejects bad diffs, and the PR template that forces every change to answer the regression question.

**When to run:**
- New product repo, after `/ctx-context-init` and before any feature work.
- Existing product repo that doesn't yet have `docs/agent-playbook.md` / `docs/conventions.md` / `docs/architecture.md`.

**When NOT to run:**
- The template repo itself (pm-os) — there's no `docs/` to scaffold here.
- A product repo that already has a constraint layer — extend the existing files with `/dev-encode-constraint` and `/dev-agent-playbook-update`.

## Step 1 — Preconditions

1. Confirm cwd is the consumer product repo root (must contain a `CLAUDE.md`). If not, halt: *"Run `/dev-scaffold-constraint-layer` from the product repo root."*
2. Confirm this is not the pm-os template repo. Halt if `CLAUDE.md` line 1 contains "pm-os template" — that's the template, not a product repo.
3. Glob for `docs/agent-playbook.md`. If it exists, ask: *"The constraint layer looks already scaffolded. I'll only fill missing files — nothing existing will be touched. Proceed? (y/n)"*

## Step 2 — Detect the Stack

Ask the user — short, one prompt, multiple-choice:

```
What's the primary stack for this repo?
1. Python (pytest + ruff)
2. Node / TypeScript (jest|vitest + eslint)
3. Both (monorepo or mixed)
4. Other — I'll skip the CI workflow and you can author it manually
```

Record the answer as `stack`. Used in Step 4.

## Step 3 — Copy the Playbook Docs

Source files live at `.claude/templates/constraint-layer/` — both in this
template repo and in any product repo where pm-os is installed as `.claude/`
(submodule or copied directory). The path is the same in both.

For each source → destination pair, **read** the source, **check** if the
destination exists. If it exists, skip and log. Else write verbatim.

| Source (in `.claude/templates/constraint-layer/`) | Destination (product repo root) |
|---|---|
| `agent-playbook.md` | `docs/agent-playbook.md` |
| `conventions.md` | `docs/conventions.md` |
| `architecture.md` | `docs/architecture.md` |
| `pull_request_template.md` | `.github/pull_request_template.md` |

Create `docs/` and `.github/` if they don't exist.

## Step 4 — Drop the CI Workflow

Based on the `stack` answer from Step 2:

| Stack answer | Workflow files to write |
|---|---|
| Python | `.github/workflows/ci.yml` ← `ci-python.yml` |
| Node | `.github/workflows/ci.yml` ← `ci-node.yml` |
| Both | `.github/workflows/ci.yml` ← `ci.yml` (stack-detecting; runs python + node jobs as manifests appear) |
| Other | Skip. Note in summary: *"Author your own `.github/workflows/ci.yml` running tests + lints on PR."* |

If the user is unsure or wants one workflow that travels across repos, write the
stack-detecting `ci.yml` for any stack — it no-ops where a manifest is absent.

For every stack except "Other," also write `.github/workflows/review-agent.yml` from the template — but ask first: *"Wire up the review-agent CI workflow? (requires a CLAUDE_CODE_OAUTH_TOKEN secret in the repo) (y/n)"*. Skip if no.

If a workflow file already exists at the destination, **do not overwrite**. Log it and tell the user where to find the template content so they can merge manually.

## Step 5 — Inject the CLAUDE.md Section

Read `.claude/templates/constraint-layer/CLAUDE.md.fragment`.

Read the product repo's `CLAUDE.md`.

If `CLAUDE.md` already contains the literal heading `## Constraint Layer`, skip — log it. Else append the full fragment to the end of `CLAUDE.md`, preceded by a blank line.

## Step 6 — Bootstrap Lint Config (Stack-Dependent)

Only if the user picked Python or Node (or both) in Step 2, and only if a lint config doesn't already exist:

**Python** — if no `ruff.toml`, `pyproject.toml` (with `[tool.ruff]`), or `.ruff.toml` exists, write `ruff.toml`:

```toml
# Minimal ruff config. Tighten as conventions accumulate.
line-length = 100
target-version = "py312"

[lint]
select = ["E", "F", "I", "B", "UP", "SIM"]
```

**Node** — if no `.eslintrc*` or `eslint.config.*` exists, write `.eslintrc.json`:

```json
{
  "extends": ["eslint:recommended"],
  "env": { "node": true, "es2022": true },
  "parserOptions": { "ecmaVersion": 2022, "sourceType": "module" }
}
```

If config exists, skip. The user's existing setup wins.

## Step 7 — Summary

Print a table of what was written, what was skipped, and the next step.

```
## scaffold-constraint-layer — Summary

Stack: {stack}

| File | Result |
|---|---|
| docs/agent-playbook.md | {created|skipped} |
| docs/conventions.md | {created|skipped} |
| docs/architecture.md | {created|skipped} |
| .github/pull_request_template.md | {created|skipped} |
| .github/workflows/ci.yml | {created|skipped|skipped-other-stack} |
| .github/workflows/review-agent.yml | {created|skipped|declined} |
| {ruff.toml | .eslintrc.json} | {created|skipped|n/a} |
| CLAUDE.md (## Constraint Layer section) | {appended|skipped} |

The constraint layer is now in place. The gate (CI) blocks bad diffs on PR.
The playbook (docs/) teaches the agent before it writes a line. The loop
(/dev-encode-constraint) turns every new mistake into a permanent constraint.

Next: fill in the placeholders in docs/agent-playbook.md, docs/conventions.md,
and docs/architecture.md. Don't ship the template comments — replace them
with real content for this repo.
```

## Follow-ups

- Fill in the playbook → `/dev-agent-playbook-update` after the next session uncovers anything non-obvious.
- First mistake the coding agent makes → `/dev-encode-constraint` to convert it into a permanent test/lint/doc.
- Review an AI-generated diff before merging → `/dev-review-diff`.

## Anti-Patterns

- **Don't overwrite existing files.** The user's prior work always wins. Skip and log.
- **Don't run in the pm-os template repo.** This skill scaffolds a product repo; running it here would create stray `docs/` directories that don't belong.
- **Don't fill in the placeholders for the user.** The playbook and conventions docs must reflect the actual repo — guessing produces lies the agent will then follow.
- **Don't enable the review-agent workflow without the secret in place.** A workflow that fails on every PR teaches the team to ignore CI.
