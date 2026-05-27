---
description: Review a code diff (working tree, last commit, or PR number) against the constraint layer — docs/conventions.md, docs/agent-playbook.md, docs/architecture.md. Outputs accept-or-reject with file/line-anchored findings citing the specific rule violated. Runs locally before commit and as the review-agent CI workflow on PR.
---

# Review Diff

The mechanical review of an AI-generated (or human-generated) diff against the embedded constraint layer. Reads `docs/conventions.md`, `docs/agent-playbook.md`, and `docs/architecture.md` as the rubric and rejects anything that violates a rule. Cites the exact rule and the exact line.

**When to run:**
- Before committing an AI-generated diff locally — confirm it passes the rubric.
- As the `.github/workflows/review-agent.yml` CI step on every PR.
- Spot-check an existing PR before merging.

**When NOT to run:**
- For style choices that aren't in the rubric — this skill only enforces what's encoded. If you want to push back on something not in the docs, run `/encode-constraint` first, then re-run this.
- On the constraint layer docs themselves (`docs/conventions.md` etc.) — those are reviewed by humans, not by this skill.

## Step 1 — Hydrate

1. Confirm cwd is a consumer product repo. Halt if missing any of `docs/conventions.md`, `docs/agent-playbook.md`, `docs/architecture.md` with: *"The constraint layer isn't scaffolded. Run `/scaffold-constraint-layer` first."*
2. Determine the diff to review:
   - **Default:** `git diff HEAD` (working tree vs last commit).
   - If the user passed a PR number → fetch via `gh pr diff <num>` (graceful fallback to `mcp__github__pull_request_read` if `gh` unavailable).
   - If the user passed a commit range → `git diff <range>`.
   - If the user pasted a diff directly → use that.
3. Read in full:
   - `docs/conventions.md` — primary rubric.
   - `docs/agent-playbook.md` — secondary; mostly for "What the Agent Must Not Do" hard rules.
   - `docs/architecture.md` — tertiary; flag diffs that violate stated constraints (e.g., cross-tenant queries when arch.md says single-tenant).

## Step 2 — Apply the Rubric

For each hunk in the diff, walk the three rubric docs in order and check for violations. For each violation, record:

- **File:line** in the diff.
- **Severity:** `block` (rule explicit, violation clear) | `warn` (rule fuzzy or judgment call).
- **Rule violated:** the exact path and line from the rubric doc (e.g., `docs/conventions.md:23 — "No bare except clauses"`).
- **Why this is a violation:** one sentence linking the diff line to the rule.
- **Suggested fix:** one line. Concrete.

**Hard rules — always block:**

- Anything in `docs/agent-playbook.md` under `## What the Agent Must Not Do`.
- Any explicit "Reject any..." entry in `docs/conventions.md` under `## Review-Agent Rubric`.
- Architectural constraints in `docs/architecture.md` under `## Constraints`.

**Soft rules — warn, don't block:**

- Style preferences in `docs/conventions.md` that don't use enforcement language ("we prefer...", "ideally..."). If frequent, surface to the user that the rule should be tightened or moved.

**Out of scope — don't comment:**

- Lint-level issues — the lint job will catch them. Don't duplicate.
- Test failures — the test job will catch them.
- Anything not anchored to a specific line in a rubric doc.

## Step 3 — Output

If running locally, print the structured report below. If running as the CI workflow, post each finding as a PR comment anchored at the file:line. One approval comment if clean.

```
## review-diff — Result

**Diff source:** {working tree | commit X..Y | PR #N}
**Files changed:** {count}
**Verdict:** {APPROVED | BLOCKED (N findings) | NEEDS REVIEW (N warnings)}

### Findings

{For each finding:}

#### [{severity}] {file}:{line}

- **Rule:** `{rubric-doc}:{line}` — "{exact rule text}"
- **Violation:** {one sentence}
- **Suggested fix:** {one line}

### Summary

{If APPROVED:} Clean against the current rubric. If a class of issue should have been caught but wasn't, run /encode-constraint to add the missing rule.

{If BLOCKED:} N hard-rule violations. The diff cannot ship until each is resolved.

{If NEEDS REVIEW:} N soft warnings. Decide per-finding whether to fix the code or tighten the rubric via /encode-constraint.
```

## Step 4 — When the Review Finds Nothing But Something Feels Wrong

If a reviewer (human or agent) catches an issue this skill missed, **that's a constraint-layer gap, not a review-skill bug**. The rubric didn't encode the rule. Run `/encode-constraint` to add it, then re-run `/review-diff` — the next diff with the same class of issue will be caught mechanically.

## Follow-ups

- A finding revealed a class of mistake worth encoding permanently → `/encode-constraint`
- The review caught missing knowledge (not a coding rule) → `/agent-playbook-update`
- Multiple BLOCKED findings on a single diff → strong signal the coding agent's context was wrong; check whether `docs/architecture.md` or the playbook needs a clarifying section.

## Anti-Patterns

- **Don't flag style preferences not in the rubric.** This skill's authority comes from citing the exact line. Inventing rules undermines it — encode them first.
- **Don't duplicate lint/test output.** Those have their own job. This skill reviews what mechanical tools can't.
- **Don't approve a diff that violates `## What the Agent Must Not Do`.** Those are hard rules. Block, even if the user pushes back — they should re-encode the rule if they disagree.
- **Don't write findings without file:line anchors.** Findings without anchors are vibes; findings with anchors are actionable.
- **Don't run on the constraint-layer docs themselves.** Changes to `docs/conventions.md` are reviewed by humans — this skill would just check the rubric against itself.
