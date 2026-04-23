---
description: Log a time-stamped observation to data/signals/active.md as an H3 section with structured metadata. Captures user feedback, competitive moves, market signals, technical constraints, or internal learnings with an optional Action Required flag.
---

# Log Signal

This skill appends a single observation to `data/signals/active.md`.
Use it when something **happened** that a PM should notice but isn't
(yet) a commitment. Unlike `/log-decision` (which records what *we*
chose), `/log-signal` records what *the world did* or what we observed.

**When to use vs. the alternatives:**
- Use `/log-signal` for dated observations: a competitor launched X, a
  user said Y, an experiment showed Z.
- Use `/log-decision` for commitments: we chose to do X, we killed Y.
- Use `/knowledge add research` for synthesized, durable learnings:
  "what we know about persona X."

See the **DB Routing Rubric** in `.claude/context/data-schemas.md` for
the full distinction.

## Before Starting — Self-Hydration

1. Identify the current product (read the host repo's CLAUDE.md for
   Repo Identity, or ask the user).
2. If the signal was just discussed in this conversation, extract it
   from context.
3. If not, ask the user:
   - What did you observe? (one-sentence headline)
   - When did it happen? (date of the source event, not today)
   - Where did you see it? (source)
4. Grep `data/signals/active.md` for similar headlines from the last
   30 days to check for duplicates.

## Signal Structure

This skill writes an H3 section to `data/signals/active.md`. See
`.claude/context/data-schemas.md` for the full format.

### Required Fields (in the metadata comment)
- **date** — when the observation occurred (the source event's date,
  NOT today's date).
- **type** — one of:
  - `User Feedback` — recurring user complaint, praise, or behavior
    pattern (3+ source mentions, not a one-off)
  - `Technical Constraint` — a build-time discovery (API limit, latency
    surprise, cost ceiling, platform restriction)
  - `Market Signal` — funding round, market movement, regulatory
    change, macro shift
  - `Competitive Move` — competitor launched, priced, pivoted, or
    acquired
  - `Internal Learning` — a validated or invalidated assumption from
    our own experiments, builds, or analysis
- **source** — where this signal came from (URL, interview reference,
  analytics dashboard, competitor site, etc.). Must be concrete.

### Body
- **Implication** — what this means for the product or strategy
  (1–2 sentences). Be concrete about what changes or what we need to
  watch.

### Optional Fields (in metadata comment)
- **action_required** — `true` if this signal demands an explicit PM
  response (a decision, an experiment, a scope change). Default `false`.
- **linked_decision** — relative path to a decision this signal connects
  to (supports, contradicts, or should trigger).

## The "Action Required" Test

Before setting `action_required:true`, the signal must pass this test:
*"If I ignore this signal for 2 weeks, something meaningful goes wrong."*
If the answer is no, leave it `false`. Action Required signals surface in
`/weekly-review` and are meant to be triaged — overusing the flag defeats
the purpose.

## Writing the Signal

1. Read the current `data/signals/active.md` (or create it with a `# Active Signals` H1 header if missing).
2. Construct the H3 block:

   ```markdown
   ### {Headline one-liner}
   <!-- date:YYYY-MM-DD type:"{Type}" source:"{source}" action_required:{true|false}{ linked_decision:"../decisions/...md" if set} -->

   **Implication:** {1–2 sentences}.
   ```

3. Insert the new block at the top of the file (immediately after the H1
   header, before any existing H3 sections). Newest-first ordering.

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
**Written to:** data/signals/active.md (top of file)
```

## Follow-ups

Suggest 1–3 contextual next steps based on the signal just logged:

- If `action_required:true`:
  → "This signal demands a response. Want to run `/log-decision` now to
  commit to a direction, or `/weekly-review` to see it alongside other
  action-required signals?"
- If `type = Competitive Move` or `Market Signal`:
  → "Want me to run `/market-scan` to pull fresh context on this market?"
- If `type = User Feedback` and it's the 3rd+ similar signal in 30 days:
  → "This is a recurring pattern. Want to run `/evaluate-opportunity` on
  the underlying user job?"
- If `type = Internal Learning` and it invalidates a prior decision:
  → "Want me to update the outcome on the linked decision to
  `Invalidated` via `/log-decision`?"

## Anti-Patterns

Reject or redirect these inputs rather than logging them:

- **Synthesized trend without a source** — "AI is getting cheaper." That's
  a Research entry, not a Signal. Redirect to `/knowledge add research`.
- **A commitment phrased as an observation** — "We should pivot to X."
  That's a decision, not a signal. Redirect to `/log-decision`.
- **A one-off comment with no pattern** — A single Reddit thread with no
  corroboration. Ask for more source examples before logging.
- **A vague dateless claim** — "The market is shifting." Ask for the
  specific dated event that triggered the observation.
