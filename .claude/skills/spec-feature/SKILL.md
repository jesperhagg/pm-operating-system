---
description: Build a feature test-first — convert user-facing acceptance criteria into failing tests, then write the minimum code to pass them. The proactive twin of /encode-constraint; acceptance tests graduate into permanent regression guards in the constraint layer.
---

# Spec Feature

Build a feature **test-first**. Define the user-facing test criteria as the objective up front, turn
them into failing tests, then write the minimum code that makes them pass. The acceptance tests you
write here don't disappear after the feature ships — the moment they go green and are committed they
**graduate into permanent regression guards** in the constraint layer's test suite.

This is the **proactive intake path** into the constraint layer. `/encode-constraint` is its reactive
twin: it turns a *mistake* into a regression test after the fact. `/spec-feature` turns *acceptance
criteria* into tests *before* the code exists. Same `tests/` tree, same CI Gate, same answer to the PR
template's "What test or constraint prevents this regression?" — a feature built this way arrives at
the Gate already holding its ticket.

**When to run:**
- Starting implementation of a feature or a `/break-down` task with a `Done when:` criterion.
- You can state the feature's success as observable, user-facing behavior.

**When NOT to run:**
- The repo has no test harness or constraint layer yet → run `/scaffold-constraint-layer` first.
- You're fixing a mistake the agent already shipped → that's the reactive path, use `/encode-constraint`.
- The work is exploratory spike code with no definable acceptance criteria → spike first, spec after.

## Step 1 — Hydrate

1. Confirm cwd is a scaffolded consumer product repo: `docs/agent-playbook.md`, `docs/conventions.md`,
   `docs/architecture.md` exist and a test runner is present (`pytest`, `vitest`, `jest`, etc.). If
   not, halt: *"Run `/scaffold-constraint-layer` first — there's no suite for acceptance tests to land in."*
2. Locate the feature objective. In priority order:
   - A `/break-down` task's `Done when:` criteria (read it from `tasks/active.md` or the conversation).
   - A `/write-prd` success section generated this session.
   - A fresh objective the user states now.
3. Read the constraint-layer rubric so generated tests and code conform on the first attempt:
   `docs/agent-playbook.md` (how to run, where things live), `docs/conventions.md` (house style —
   especially the Tests section), `docs/architecture.md` (where this feature fits, hot paths).
4. If `context/learnings/spec-feature.md` exists, read the top 3–5 H3 entries and apply silently.
5. Briefly summarize the objective and the test-path convention before proceeding.

## Step 2 — Specify the Acceptance Criteria (the objective)

Convert the feature into a **numbered list of observable, falsifiable acceptance criteria**. This is
the heart of the skill — the criteria *are* the objective the code must meet.

Each criterion must be:
- **User-facing** — phrased as behavior ("When the user submits an empty form, the API returns 422
  with a structured error"), not implementation ("the validator function is called").
- **Observable** — checkable from outside the unit: a return value, a status code, a rendered output,
  a persisted record.
- **Executable** — you can write a test that asserts it. If you can't, it's a goal, not a criterion —
  sharpen it or drop it.
- **Falsifiable** — there's a clear input that makes it fail. A criterion that can't fail tests nothing.

Keep business KPIs out — "D7 retention ≥ 40%" is a `/write-prd` success metric, not an acceptance
criterion. Acceptance criteria are about *correct behavior*, not *market outcomes*.

**Confirm the numbered list with the user before writing a single test.** Locking the criteria first
is the discipline that makes the rest mechanical — the same way `/design-experiment` fixes the
decision rule before the experiment runs.

## Step 3 — Red: write the failing tests first

Translate each acceptance criterion into a test. One criterion maps to one (or a small cluster of)
test cases.

- **Destination:** `tests/<mirror-of-source-path>/test_<thing>.py` (Python) or
  `tests/<...>.test.ts` (TS) — the same convention `/encode-constraint` uses, so proactive and
  reactive tests sit side by side.
- **Run them and confirm they FAIL** against the current (absent) implementation. A test that passes
  before any code is written tests nothing — fix it until it fails for the right reason.
- Follow the Tests section of `docs/conventions.md` (no network/filesystem/time dependencies unless
  the convention allows; one behavior per test; clear names tied to the criterion).

State explicitly, per test, which acceptance-criterion number it covers, so coverage is auditable.

## Step 4 — Green: minimum code to pass

Write the **least** code that makes the red tests green. Follow `docs/engineering.md`: simplicity
first, surgical changes, nothing speculative. Delegate the implementation to the cheapest capable
model per the repo's delegation rules.

Loop: run the tests, fix, re-run, until **every** acceptance test passes. Do not add behavior the
criteria don't demand — if you find yourself wanting to, that's a new criterion (back to Step 2) or a
new task (back to `/break-down`), not a silent expansion.

## Step 5 — Refactor and hand to the Gate

1. Refactor the now-passing code under `docs/conventions.md` — keep the tests green throughout.
2. Run `/review-diff` to check the diff against the full constraint layer before commit.
3. The acceptance tests now **answer the PR template's "What test or constraint prevents this
   regression?" by construction** — list their paths and names there. This is the graduation point:
   spec tests become regression guards with no extra ceremony.

## Step 6 — Output

```
## spec-feature — Result

**Feature:** {one-line objective}
**Acceptance criteria:** {N}, all green
**Tests added:** {paths}
**Source changed:** {paths}

### Coverage map
1. {criterion} → {test name} ✅
2. ...

### Gate status
- /review-diff: {APPROVED | findings to address}
- PR regression answer: {test paths/names that prevent this regression}
```

## Capture Learning

Append one H3 entry to `context/learnings/spec-feature.md` (create with `# Learnings — spec-feature`
H1 if missing). Newest first. Mark `session:pending` — `/context-sync` reconciles.

```markdown
### {one-line headline of what made this run distinctive} {#headline-slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD skill:spec-feature session:pending -->

**Worked:** {one sentence — which criterion framing or test produced the cleanest red→green loop}.
**Missed:** {one sentence — a criterion that was vague, untestable, or hid scope}.
**Next time:** {one adjustment — criteria sharpness, test-path choice, scope guard}.
```

Keep entries three lines, not three paragraphs.

## Follow-ups

- Diff is green and ready → `/review-diff` to gate it, then commit.
- An **unanticipated** mistake surfaced that the acceptance tests didn't foresee → `/encode-constraint`
  (the reactive twin) to lock that class out forever.
- The feature committed to a scope or design choice worth recording → `/log-decision`.
- Scope grew past the original criteria mid-loop → `/break-down` to re-decompose.

## Anti-Patterns

- **Don't write code before the tests are red.** If there's no failing test, there's no objective to
  meet — you're coding on vibes, not criteria.
- **Don't write tests that pass on empty code.** A green test before implementation constrains nothing;
  it's the same dead asset as `/encode-constraint`'s "test that passes on the buggy code."
- **Don't smuggle business KPIs in as acceptance criteria.** Retention, activation, and revenue are
  `/write-prd` metrics. Acceptance criteria assert *correct behavior*, full stop.
- **Don't expand scope inside the green loop.** New behavior the criteria didn't name is a new
  criterion or a new task — never a quiet addition that ships untested.
- **Don't skip the user confirmation in Step 2.** Locking criteria before testing is the whole point;
  inventing them as you go reintroduces the ambiguity the workflow exists to remove.
