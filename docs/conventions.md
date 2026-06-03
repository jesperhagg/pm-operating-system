# Conventions

> **Placeholder.** The product codebase is not yet present in this repo. Fill these sections in as real code lands.

_House style the coding agent must match. Used by `/review-diff` and the review-agent CI workflow as the rubric for accept/reject decisions._

_Every entry is enforceable — if you can't point at a specific pattern in a diff and say "this violates section X," the entry is too vague. Either tighten it or move it to `agent-playbook.md`._

## Naming

- _(example) Functions: `snake_case` in Python, `camelCase` in TypeScript._
- _(example) Test files mirror source paths: `src/foo/bar.py` → `tests/foo/test_bar.py`._
- _(example) No abbreviations except a fixed allowlist (`db`, `id`, `url`)._

## Code Structure

- _(example) One public function per file unless tightly coupled (helpers next to their caller)._
- _(example) No module exceeds 300 lines — split before you scroll._
- _(example) Public functions need type hints / type annotations._

## Error Handling

- _(example) Never swallow exceptions with bare `except:` or empty `catch {}`._
- _(example) User-facing errors return structured error objects, not raw strings._
- _(example) Don't catch what you can't handle — let it propagate to the request layer._

## Tests

- _(example) Every new public function has at least one test._
- _(example) Bug fixes ship with a regression test that fails before the fix and passes after._
- _(example) No test depends on network, real time, or filesystem state outside `tmp_path`._

## Comments

- _(example) Default to no comments. Only document the WHY, never the WHAT._
- _(example) No comments referencing the current PR, ticket, or author._
- _(example) Docstrings on public APIs only — internal helpers should be readable from the name._

## Dependencies

- _(example) New runtime dependency requires an architecture.md update and a justification in the PR description._
- _(example) Pin versions in lockfiles. No `latest` tags._
- _(example) Prefer the standard library over a new dependency for one-off needs._

## Logging and Observability

- _(example) Log structured (JSON) at request boundaries, free-form inside hot paths._
- _(example) No `print` statements in committed code._
- _(example) Errors logged with full context (request id, tenant id, input shape)._

## What Counts as a Convention Violation

The review-agent rejects a diff when:
- It violates any explicit rule above.
- It introduces a pattern that contradicts an example pattern elsewhere in the codebase.
- It would require a future convention entry to clean up.

The review-agent does not reject:
- Style choices not covered here (subjective).
- Things the linter already catches (lint will fail separately).
