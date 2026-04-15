---
description: Log a time-stamped observation to the Notion Signals database. Captures user feedback, competitive moves, market signals, technical constraints, or internal learnings with structured metadata and an optional Action Required flag.
---

# Log Signal

This skill writes a single observation to the Notion Signals database.
Use it when something **happened** that a PM should notice but isn't
(yet) a commitment. Unlike `/log-decision` (which records what *we*
chose), `/log-signal` records what *the world did* or what we observed.

**When to use vs. the alternatives:**
- Use `/log-signal` for dated observations: a competitor launched X, a
  user said Y, an experiment showed Z.
- Use `/log-decision` for commitments: we chose to do X, we killed Y.
- Use `/knowledge add research` for synthesized, durable learnings:
  "what we know about persona X."

See the **DB Routing Rubric** in `.claude/context/notion-schemas.md` for the full distinction.

## Before Starting — Self-Hydration

1. Identify the current product (read the host repo's CLAUDE.md for
   Repo Identity, or ask the user).
2. If the signal was just discussed in this conversation, extract it
   from context.
3. If not, ask the user:
   - What did you observe? (one-sentence headline)
   - When did it happen? (date of the source event, not today)
   - Where did you see it? (source)
4. Use Notion MCP to fetch recent Signals for this product (last 30 days)
   to check for duplicates.

## Signal Structure

This skill writes to the shared Signals database (see `.claude/context/notion-schemas.md`
for full property definitions). Capture the signal
with these fields:

### Required Fields
- **Signal** — one-sentence headline of the observation.
- **Date** — when the observation occurred (the source event's date, NOT
  today's date).
- **Type** — one of:
  - `User Feedback` — recurring user complaint, praise, or behavior pattern
    (3+ source mentions, not a one-off)
  - `Technical Constraint` — a build-time discovery (API limit, latency
    surprise, cost ceiling, platform restriction)
  - `Market Signal` — funding round, market movement, regulatory change,
    macro shift
  - `Competitive Move` — competitor launched, priced, pivoted, or acquired
  - `Internal Learning` — a validated or invalidated assumption from our
    own experiments, builds, or analysis
- **Source** — where this signal came from (URL, interview reference,
  analytics dashboard, competitor site, etc.). Must be concrete.
- **Product** — which product(s) this applies to (multi-select).

### Context Fields
- **Implication** — what this means for the product or strategy
  (1–2 sentences). Be concrete about what changes or what we need to
  watch.
- **Linked Decision** — if this signal connects to a prior decision
  (supports it, contradicts it, or should trigger a new one), reference
  the decision title or date.
- **Action Required** — checkbox. Set to `true` if this signal demands
  an explicit PM response (a decision, an experiment, a scope change).
  If it's just observational context for later, leave `false`.

## The "Action Required" Test

Before setting `Action Required = true`, the signal must pass this test:
*"If I ignore this signal for 2 weeks, something meaningful goes wrong."*
If the answer is no, leave it `false`. Action Required signals surface in
`/weekly-review` and are meant to be triaged — overusing the flag defeats
the purpose.

## Writing to Notion

Use Notion MCP to create a new page in the Signals database:
- Set `Signal` (title) to the one-sentence headline
- Set `Date` to the source event's date
- Set `Type`, `Source`, `Implication`, `Action Required`
- Set `Product` multi-select to the identified product
- Set `Linked Decision` if one was identified

If Notion MCP is not available or the write fails:
- Log the signal to `.claude/memory/shared.md` under a
  `Signals (Notion fallback)` section.
- Format: `- [{date}] **{product}** — **{type}**: {signal} — Source: {source} — Implication: {implication} — Action: {yes/no}`
- At next session start, `/tasks` will prompt to sync these to Notion.

## Output

Confirm what was logged:

```
## Signal Logged

**Product:** {product}
**Type:** {type}
**Signal:** {headline}
**Date:** {source date}
**Source:** {source}
**Implication:** {implication}
**Action Required:** {yes/no}
**Written to:** Notion Signals database [or local memory fallback]
```

## Follow-ups

Suggest 1–3 contextual next steps based on the signal just logged:

- If `Action Required = true`:
  → "This signal demands a response. Want to run `/log-decision` now to
  commit to a direction, or `/weekly-review` to see it alongside other
  action-required signals?"
- If `Type = Competitive Move` or `Market Signal`:
  → "Want me to run `/market-scan` to pull fresh context on this market?"
- If `Type = User Feedback` and it's the 3rd+ similar signal in 30 days:
  → "This is a recurring pattern. Want to run `/evaluate-opportunity` on
  the underlying user job?"
- If `Type = Internal Learning` and it invalidates a prior decision:
  → "Want me to update the Outcome on the linked decision to
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
