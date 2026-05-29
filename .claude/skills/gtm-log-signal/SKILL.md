---
description: Log a time-stamped observation to context/market/signals.md or context/users/feedback.md as an H3 section with structured metadata. Captures user feedback, competitive moves, market signals, technical constraints, or internal learnings with an optional Action Required flag.
---

# Log Signal

This skill appends a single observation to the appropriate context file.
Use it when something **happened** that a PM should notice but isn't (yet)
a commitment. Unlike `/strat-log-decision` (which records what *we* chose),
`/gtm-log-signal` records what *the world did* or what we observed.

**Signal routing by type:**

| Signal type | File |
|---|---|
| User Feedback | `context/users/feedback.md` |
| Market Signal, Competitive Move | `context/market/signals.md` |
| Internal Learning | `context/product/experiments.md` (H2 entry) |
| Technical Constraint | `context/market/signals.md` (unless it triggers a decision → `/strat-log-decision`) |

**When to use vs. the alternatives:**
- Use `/gtm-log-signal` for dated observations: a competitor launched X, a
  user said Y, an experiment showed Z.
- Use `/strat-log-decision` for commitments: we chose to do X, we killed Y.
- Use `/ctx-knowledge add research` for synthesized, durable learnings:
  "what we know about persona X."

See the **Context Routing Rubric** in `.claude/context/context-schemas.md`.

## Before Starting — Self-Hydration

1. Identify the current product (read the host repo's CLAUDE.md for
   Repo Identity, or ask the user).
2. If the signal was just discussed in this conversation, extract it
   from context.
3. If not, ask the user:
   - What did you observe? (one-sentence headline)
   - When did it happen? (date of the source event, not today)
   - Where did you see it? (source)
4. Determine the signal type from the description. Confirm the target
   file with the user if ambiguous.
5. Grep the target file for similar headlines from the last 30 days to
   check for duplicates.

## Signal Structure

### Required Fields (in the metadata comment)
- **date** — when the observation occurred (source event date, not today).
- **type** — one of:
  - `User Feedback` — recurring user complaint, praise, or behavior
    pattern (3+ source mentions, not a one-off)
  - `Technical Constraint` — a build-time discovery (API limit, latency
    surprise, cost ceiling, platform restriction)
  - `Market Signal` — funding round, market movement, regulatory
    change, macro shift
  - `Competitive Move` — competitor launched, priced, pivoted, or acquired
  - `Internal Learning` — a validated or invalidated assumption from our
    own experiments, builds, or analysis
- **source** — where this signal came from. Must be concrete.
- **session** — always `pending` when written by this skill.

### Body
- **Implication** — what this means for the product or strategy (1–2 sentences).

### Optional Fields
- **action_required** — `true` if this signal demands an explicit PM
  response. Default `false`. See the Action Required test below.
- **linked_decision** — anchor to a decision this signal connects to.

## The "Action Required" Test

Before setting `action_required:true`:
*"If I ignore this signal for 2 weeks, something meaningful goes wrong."*
If the answer is no, leave it `false`.

## Writing the Signal

1. Determine the target file from the routing table above.
2. Compute the anchor slug: kebab-case of headline, append `-YYYY-MM-DD`.
3. Open the target file (create it with an H1 header if missing).
4. Insert the new H3 block at the top (newest-first), after the H1 header:

```markdown
### {Headline one-liner} {#slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD type:"{Type}" source:"{source}" action_required:{true|false} linked_decision:"{anchor or null}" session:pending -->

**Implication:** {1–2 sentences}.
```

The `session:pending` annotation marks this as session-written, awaiting
reconciliation by `/ctx-context-sync`.

## Output

Confirm what was logged:

```
## Signal Logged

**Type:** {type}
**Signal:** {headline}
**Date:** {source date}
**Source:** {source}
**Implication:** {implication}
**Action Required:** {yes/no}
**Written to:** {target file} (top of file)
```

## Follow-ups

- If `action_required:true`:
  → "This signal demands a response. Want to run `/strat-log-decision` now to
  commit to a direction, or `/ops-weekly-review` to see it alongside other
  action-required signals?"
- If `type = Competitive Move` or `Market Signal`:
  → "Want me to run `/gtm-market-scan` to pull fresh context on this market?"
- If `type = User Feedback` and it's the 3rd+ similar signal in 30 days:
  → "This is a recurring pattern. Want to run `/strat-evaluate-opportunity` on
  the underlying user job?"
- If `type = Internal Learning` and it invalidates a prior decision:
  → "Want me to update the outcome on the linked decision to
  `Invalidated` via `/strat-log-decision`?"

## Anti-Patterns

Reject or redirect these inputs rather than logging them:

- **Synthesized trend without a source** — "AI is getting cheaper."
  Redirect to `/ctx-knowledge add research`.
- **A commitment phrased as an observation** — "We should pivot to X."
  Redirect to `/strat-log-decision`.
- **A one-off comment with no pattern** — A single Reddit thread.
  Ask for more source examples before logging User Feedback.
- **A vague dateless claim** — Ask for the specific dated event.
