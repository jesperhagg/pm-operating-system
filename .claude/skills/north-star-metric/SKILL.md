---
description: Pick a North Star Metric using 5 sharpness tests (user-value-aligned, leading, growth-correlated, durable, measurable). Force one NSM plus 3–5 input metrics plus an explicit kill-criterion. Writes the decision as an H2 block in context/product/strategy.md.
---

# North Star Metric

Most "north star" picks are vibes — revenue or DAU because that's what
got measured last quarter. This skill forces a deliberate pick: a single
metric, 3–5 inputs that drive it, and a kill-criterion stating when a
flat NSM means strategy is wrong (not just execution).

Use this when shipping the first version of a strategy, after a pivot,
or when a `/weekly-review` keeps surfacing "what are we actually
optimizing for?"

## Before Starting — Self-Hydration

1. Identify the current product (read host repo's CLAUDE.md, or ask).
2. Read:
   - `context/product/strategy.md` — read in full (it's the living
     strategy doc; the NSM may already exist or be implicit).
   - Grep `context/product/decisions.md` for `type:Positioning`,
     `type:Pricing`, and `type:Scope` (last 180 days) — to understand
     what the strategy is committed to.
   - `context/product/experiments.md` — last 60 days, to surface
     metrics already being measured.
   - If `context/learnings/north-star-metric.md` exists, read the top
     3–5 H3 entries. Apply silently to this run — do not narrate prior
     lessons back to the user.
3. Brief the user: *"Picking NSM for {product}. Current strategy named
   '{positioning headline}'. {N} metrics already tracked across recent
   experiments. Proceed?"*

If `context/product/strategy.md` is empty or has no positioning, halt:
*"No strategy on file — an NSM without a strategy is a metric in search
of a meaning. Anchor positioning first."*

## Framework — 5 Sharpness Tests

A candidate NSM must pass **all five**. If a candidate fails one, either
fix it or pick a different metric.

### Test 1 — User-Value-Aligned

Does the metric move when customers get more value, or only when *we*
extract more? Revenue moves when we charge more; usage doesn't.

**Pass:** "Weekly reviews completed per active user" (moves when the
product works for them).
**Fail:** "Paid subscriptions" as the only NSM for an early-stage
product (moves when we sell harder, regardless of whether they
get value).

### Test 2 — Leading, Not Lagging

Does the metric move weeks *before* revenue does, not weeks after?
Lagging metrics are confirmations, not steering wheels.

**Pass:** "% of new users completing first weekly review within 7 days"
(activation predicts retention predicts revenue).
**Fail:** "MRR" (this lags every cause by 30–90 days).

### Test 3 — Growth-Correlated

Would a 10% lift in this metric reliably correspond to a meaningful lift
in growth? If the metric can move without growth following, it's not
load-bearing.

**Pass:** Demonstrated or plausibly causal link between metric and growth.
**Fail:** "NPS score" — moves independently of growth in many cases.

### Test 4 — Durable Across Pivots

Would the metric still be the NSM if you changed pricing, persona, or
distribution channel tomorrow? Durable metrics survive iteration; brittle
ones get replaced after each pivot.

**Pass:** "Active weekly reviewers" (still the NSM whether sold as B2C
SaaS, B2B teams, or done-for-you service).
**Fail:** "Indie Hackers signups per week" (channel-specific; dies the
day you change channels).

### Test 5 — Measurable Without Instrumentation Hell

Can you read this number every week without building new pipelines? If
the answer is "we'd need a data team for that", the metric will go
unread.

**Pass:** Measurable from existing analytics, billing system, or a
weekly SQL query you can run yourself.
**Fail:** "User happiness index" composed from a survey + behavioral
panel + tagged events you don't yet track.

## Input Metrics (3–5)

Once the NSM passes all 5 tests, define the **input metrics** that drive
it — the levers you can pull weekly.

**Rules:**
- 3 minimum, 5 maximum. Fewer than 3 means you don't understand the NSM;
  more than 5 means you haven't picked the load-bearing ones.
- Each input must be: (a) measurable today, (b) movable by a specific
  team action within 4 weeks, (c) plausibly causal upstream of the NSM.
- Use the formula: **NSM = f(input₁, input₂, input₃, ...)**. State the
  function in plain words ("Active weekly reviewers = new activations ×
  retention rate − churn").

## Kill-Criterion (Mandatory)

The single condition that, if met, means the strategy is wrong — not
that the team needs to try harder.

**Template:**
> If NSM is flat or declining for {N consecutive weeks/months}, we treat
> this as evidence that the strategy is wrong and run
> `/evaluate-opportunity` (or `/sunset-product`) before adding more
> headcount, scope, or spend.

**Rules:**
- N must be a number, not "a while".
- "Flat" must have a number too — "<2% week-over-week growth" is flat;
  "no growth" is interpretation.
- The kill-criterion is a precommitment. Argue with it after data
  arrives and you've defeated the point.

## One NSM, Not Two

If two candidates pass all five tests, **pick one**. Holding two NSMs
splits focus and every disagreement about priorities re-litigates which
one matters more. The other becomes an input metric.

## Output

Append a new H2 block to `context/product/strategy.md` titled
`## North Star Metric`. If a prior `## North Star Metric` block exists,
**do not overwrite** — confirm with the user whether this supersedes (in
which case mark the prior block `superseded:YYYY-MM-DD` and add the new
one above) or whether the prior block was approximate and this is the
formal definition.

If `context/product/strategy.md` does not exist, create it with
`# Strategy` H1 (defensive; `/context-init` scaffolds it).

```markdown
## North Star Metric {#north-star-metric-YYYY-MM-DD}
<!-- date:YYYY-MM-DD type:Strategy status:Active session:pending -->

**NSM:** {metric}, measured weekly via {source}.

**Definition:** {one-sentence precise definition — what counts as "active"?
in what window?}

**Why this passes all 5 tests:**
- User-value-aligned: {…}
- Leading: {…}
- Growth-correlated: {…}
- Durable across pivots: {…}
- Measurable without instrumentation hell: {…}

**Input metrics:**
1. {input₁} — moved by {team action}
2. {input₂} — moved by {team action}
3. {input₃} — moved by {team action}

NSM = f({input₁}, {input₂}, {input₃}) — {plain-words function}.

**Kill-criterion:**
If NSM is flat (<{X}% WoW growth) for {N} consecutive weeks, run
`/evaluate-opportunity` before adding scope, headcount, or spend.

---
```

Return a short summary to the user:

```
## NSM Defined
**NSM:** {metric}
**Tests passed:** 5/5
**Input metrics:** {N}
**Kill-criterion horizon:** {N weeks of flat <X% growth}
**Appended to:** context/product/strategy.md (#north-star-metric-{date})
```

## Worked Example — One NSM

**Product:** Hosted weekly-review SaaS for solo multi-product PMs.

**NSM:** Weekly reviews completed per active user.

Passes all 5: completion = value received; moves before revenue; lifted
completion has correlated with retention in prior data; survives a pivot
to B2B teams (still the right metric); measurable from a single
`reviews_completed` event in existing analytics.

**Input metrics:**
1. New-user first-review completion rate within 7 days (activation).
2. Active users (any review event in last 7 days) (engagement breadth).
3. Reviews per active user per week (engagement depth).

NSM = Active users × Reviews per active user per week.

**Kill-criterion:** If reviews/active user is flat (<2% WoW growth) for
8 consecutive weeks, run `/evaluate-opportunity` before adding scope.

## Capture Learning

After defining the NSM, append one H3 entry to
`context/learnings/north-star-metric.md` (create with
`# Learnings — north-star-metric` H1 if missing). Newest first. Mark
`session:pending` — `/context-sync` will reconcile.

```markdown
### {one-line headline of what made this run distinctive} {#headline-slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD skill:north-star-metric session:pending -->

**Worked:** {one sentence — which test surfaced the cleanest pick}.
**Missed:** {one sentence — temptation toward a lagging or vanity metric}.
**Next time:** {one adjustment — test phrasing, kill-criterion horizon, input-metric count}.
```

Keep entries three lines, not three paragraphs.

## Follow-ups

Contextual to what was committed:

- NSM defined → `/log-decision` (Type: Strategy) to formally commit the
  pick as a decision tied to current strategy.
- An input metric is unmeasured today → `/design-experiment` for a
  lightweight instrumentation test.
- Weekly cadence needs reorienting → next `/weekly-review` will anchor
  Focus Score against the NSM trajectory.
- Kill-criterion is going to trigger soon (already flat) → run
  `/evaluate-opportunity` *now*, don't wait for the timer.

## Anti-Patterns

- **Revenue as NSM for pre-PMF product** — revenue lags every cause by
  90 days. Pick the leading metric that predicts revenue.
- **Two NSMs** — splits focus. Pick one; the other is an input.
- **No kill-criterion** — without one, "what is success?" never gets
  asked, and dying products live forever.
- **Lagging metric labeled as leading** — MRR is not leading even if the
  team calls it that. Use Test 2 honestly.
- **Vanity NSM** — page views, social followers, signups (without
  activation). These move with marketing spend, not with product value.
- **Composite "health score" NSM** — multi-input composites are
  unreadable and impossible to debug when they drop. Pick one number.
