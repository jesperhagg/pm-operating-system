---
description: Convert a coding-agent mistake into a permanent constraint — regression test, lint rule, conventions paragraph, playbook note, or review-agent prompt. Runs the decision rubric, names the exact file path, and produces the exact text/code to add. Then re-runs the original task. The core loop of the constraint layer.
---

# Encode Constraint

The central loop of the constraint layer: when the coding agent (or a human) made a mistake, **do not patch the code directly**. Encode a constraint that prevents the class of mistake forever, then re-run the original task. The next attempt is blocked by the constraint, not by a human.

**When to run:**
- The coding agent shipped a diff with a bug, style violation, or unsafe pattern.
- Code review caught something that should have been caught mechanically.
- A class of mistake keeps recurring — encode it once, end it forever.

**When NOT to run:**
- A genuine one-off — no class to encode (rare; default to encoding anyway).
- The mistake is fuzzy judgment with no clear pattern — use `/agent-playbook-update` to write the paragraph instead.

## Step 1 — Hydrate the Mistake

1. Confirm cwd is a consumer product repo with `docs/agent-playbook.md` and `docs/conventions.md` (the constraint layer is scaffolded). If not, halt: *"Run `/scaffold-constraint-layer` first."*
2. Ask the user (or extract from conversation context) the answers to:
   - **What happened?** One sentence — the mistake the agent made.
   - **What's the class?** What would a similar mistake look like in a different file? Push the user past the specific instance.
   - **What was the original task?** So we can re-run it after the constraint lands.
3. Look at the actual diff if available (run `git diff HEAD~1 HEAD` or ask for the relevant file path). Skipping this step produces constraints that don't match the real mistake.

## Step 2 — Apply the Decision Rubric

Pick exactly one artifact type by walking the rubric in order. The first match wins.

| Question | If yes → artifact | Why |
|---|---|---|
| Is the mistake **deterministically detectable in test output** (wrong return value, missing field, broken endpoint)? | **Regression test** | Tests are the strongest constraint — they run on every commit and fail loudly. |
| Is the mistake a **style or static pattern** (banned function, naming, structure, hard-coded value)? | **Lint rule** | Linters scale: catches every occurrence forever, costs nothing per run. |
| Is the mistake an **explicit house-style violation** that's hard to express as a lint (e.g., "user-facing errors must return structured objects")? | **Convention entry in `docs/conventions.md`** | Read by `/review-diff` and the review-agent CI workflow as the rubric. |
| Is the mistake **missing knowledge** the agent would have had if it had read the playbook (where creds live, how to run X, a quirk)? | **Playbook entry in `docs/agent-playbook.md`** | Knowledge belongs where the agent looks for it first. |
| Is the mistake a **judgment call** the linter can't decide but a reviewer can ("this should have been split into two functions")? | **Review-agent prompt** (added to `docs/conventions.md` under the "Review-agent rubric" section) | The review-agent reads conventions.md and applies them. |

If two seem to apply, prefer the higher row (tests beat lints beat conventions beat playbook beat review prompts). Stronger constraint wins.

## Step 3 — Produce the Exact Artifact

Output the **complete, ready-to-paste artifact** plus the exact destination path. No placeholders. No "TODO: fill in." If the skill can't produce a complete artifact, ask one focused clarifying question and try again — do not ship a partial constraint.

### For a regression test

- Destination: `tests/<mirror-of-source-path>/test_<thing>.py` (Python) or `tests/<...>.test.ts` (TS).
- Body: a test that **fails on the current buggy code** and **passes after the fix**. Both assertions must be made explicit in the output. If the test doesn't fail on current code, it doesn't constrain anything — fix the test.

### For a lint rule

- Destination: the project's lint config (`ruff.toml`, `.eslintrc.json`, `pyproject.toml [tool.ruff]`, etc.).
- Body: the exact config snippet to merge in. If the rule needs a custom plugin or codemod, name it. Prefer rules already shipped with the linter.

### For a conventions entry

- Destination: `docs/conventions.md` under the most relevant H2 section (Naming / Code Structure / Error Handling / Tests / Comments / Dependencies / Logging). Add a new H2 if no existing section fits.
- Body: one bullet, ten to twenty words, **enforceable** ("if you see X in a diff, reject it"). If it reads like advice ("we prefer..."), tighten or move to the playbook.

### For a playbook entry

- Destination: `docs/agent-playbook.md` under the most relevant H2 section (How to Run / Where Things Live / Credentials / Quirks / What the Agent Must Not Do / Glossary).
- Body: one to three bullets. Concrete. Tells the agent what to do or where to look.

### For a review-agent prompt

- Destination: append to `docs/conventions.md` under a `## Review-Agent Rubric` H2 section (create it if missing).
- Body: a short imperative the review-agent runs against every diff. *"Reject any new public function without a corresponding test in `tests/`."*

## Step 4 — Output

```
## encode-constraint — Result

**Mistake class:** {one-sentence summary}
**Artifact type:** {test | lint | convention | playbook | review-prompt}
**Destination:** {exact path}
**Strength:** {blocks at CI | blocks at lint | reviewed by /review-diff | absorbed by next session}

### Artifact to apply

{the complete ready-to-paste artifact}

### Next steps

1. Apply the artifact above to {destination}.
2. Verify it catches the mistake: {specific verification command}.
3. Re-run the original task: "{the original task from Step 1}".
4. If the agent now ships a clean attempt blocked-then-passing through the constraint, the loop closed. If not, the constraint is too weak — re-run /encode-constraint with the new failure.
```

## Follow-ups

- Mistake was about missing knowledge, not a coding error → `/agent-playbook-update` (this skill's softer cousin)
- Want to verify the constraint actually catches the class on the next diff → `/review-diff`
- Multiple constraints encoded in one session → consider whether a single architectural change would obviate them; flag for the next architecture review.

## Anti-Patterns

- **Don't patch the code first and encode later.** The code patch is the WRONG asset. The constraint is the right one. Encode, apply, then let the constraint guide the re-run.
- **Don't pick "convention" when you could pick "lint."** Conventions are read by humans and the review-agent; lints are read by the compiler. Stronger constraint wins.
- **Don't produce a test that already passes on the buggy code.** That test constrains nothing. If you can't write a failing test for the class of mistake, the artifact type is wrong — move down the rubric.
- **Don't encode every mistake as a new conventions entry.** Conventions bloat is the same anti-pattern as a settings page with too many toggles — it stops being read. Lints scale, conventions don't.
- **Don't write the constraint for the specific bug — write it for the class.** "Don't return None from `get_user`" is a one-instance lint. "Public getters must return the documented type or raise" is a class.
