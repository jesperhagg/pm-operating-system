# Engineering Principles

How to approach **product coding tasks** in this repo. The companion docs are
`docs/architecture.md` (system shape), `docs/conventions.md` (enforceable house style,
checked by `/dev-review-diff`), and `docs/agent-playbook.md` (non-obvious repo knowledge).

## 1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

## 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.
- Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

Define success criteria. Loop until verified.

- Transform tasks into verifiable goals.
- For multi-step tasks, state a brief plan with verify steps.
- Strong success criteria let you loop independently. Weak criteria require clarification — ask for it.

## Task Delegation

Spawn subagents and pick the cheapest model that can handle the job:

- **Haiku** — bulk mechanical tasks, no judgment needed.
- **Sonnet** — scoped research, code exploration, synthesis.
- **Opus** — only when real planning or tradeoffs are involved.

Caps:

- Haiku never spawns further subagents (if it needs to, the task was wrong-sized).
- Max spawn depth is 2 (parent → subagent → one more tier).
- If a subagent realizes it needs a smarter model, it returns to the parent instead of escalating on its own.
