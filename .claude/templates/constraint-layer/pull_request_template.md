<!--
Constraint-layer PR template. Borrowed from the OpenAI team practice:
every PR answers the regression question. If the answer is "none," the
work isn't done.
-->

## What

_(One paragraph. What this PR changes, from the user's perspective. Not the implementation — the behavior change.)_

## Why

_(One paragraph. The reason this change exists. Link the ticket, decision, or signal that drove it.)_

## What test or constraint prevents this regression?

_(Required. Pick one or more — and be specific:)_

- [ ] **Regression test** — file path and test name: `___`
- [ ] **Lint rule** — config file and rule: `___`
- [ ] **Convention entry** — section in `docs/conventions.md`: `___`
- [ ] **Playbook note** — section in `docs/agent-playbook.md`: `___`
- [ ] **Review-agent prompt** — added to review rubric: `___`
- [ ] **Not applicable** — explain why this class of mistake can't recur: `___`

## How was this verified?

- [ ] Tests pass locally (`make test` or equivalent)
- [ ] Lints pass locally (`make lint` or equivalent)
- [ ] `/dev-review-diff` ran clean
- [ ] Manually exercised the change in dev

## Docs updated?

- [ ] `docs/architecture.md` — if structure changed
- [ ] `docs/conventions.md` — if a new pattern was introduced
- [ ] `docs/agent-playbook.md` — if there's new non-obvious knowledge
- [ ] None needed — explain: `___`
