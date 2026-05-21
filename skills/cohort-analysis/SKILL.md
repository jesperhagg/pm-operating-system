---
description: Structure a cohort analysis — pick the cohort axis, the metric, the comparison window, and (before reading data) the actionable threshold that triggers a decision. Surfaces curves and divergence; rejects vanity averages and undersized samples. Conversation-first; persists only when an experiment-worthy signal appears.
---

# Cohort Analysis

Most "we looked at the data" sessions end in vibes. This skill forces the
4 decisions that make a cohort analysis decision-grade — including the
kill / act threshold, set *before* opening the data so the result can't be
rationalized after the fact.

The skill is the **analytic framework**, not the data layer. Hand it data
in the conversation, or point it at a query / dashboard you've already run.

## When to Use

- Retention has been ambiguous; "is it stable or decaying?" needs a real
  read.
- A pricing or onboarding change shipped 4+ weeks ago and you need to
  confirm impact on new cohorts.
- Multiple acquisition channels are running and you can't tell which one
  produces the durable users.

## Before Starting — Self-Hydration

1. Identify the current product (read host repo's CLAUDE.md, or ask).
2. Read:
   - Grep `context/product/decisions.md` for `status:Active` and
     `type:Pricing` or `type:Go-to-Market` (last 90 days) — to know what
     changes could plausibly explain cohort divergence.
   - Grep `context/product/experiments.md` for entries from the last 90
     days — to avoid re-running an experiment that already concluded.
   - Grep `context/users/feedback.md` for the last 30 days — behavioral
     context for any divergence you find.
   - If `context/learnings/cohort-analysis.md` exists, read the top 3–5
     H3 entries. Apply silently to this run — do not narrate prior
     lessons back to the user.
3. Confirm with the user: *"Cohort analysis for {product}. Recent changes
   on file: {1–2 decisions}. What's the question we're answering?"*

The skill does **not** fetch data automatically. Ask the user where the
data lives (CSV path, query, dashboard, paste-in) before proceeding.

## Framework — 4 Decisions, In Order

Each decision is committed before the next. **Decision 4 is set before you
look at any numbers** — that's the whole point.

### 1. Cohort Axis

Pick exactly one. Mixing axes produces confounded results.

| Axis | When it fits |
|---|---|
| **Signup date** (weekly or monthly buckets) | Baseline retention; default for "is the product getting stickier?" |
| **First-action date** | Activation-stickiness analysis; when signup ≠ first real use. |
| **Acquisition channel** | "Which channel produces durable users?" |
| **Plan tier** | Differentiated retention by price point. |
| **Onboarding variant** | A/B test impact on retention. |

**Rule:** Pick one. If you need two, run two analyses — don't crosshatch
in a single chart.

### 2. Metric

Pick exactly one. Multi-metric cohort charts are noise.

| Metric | Definition | When it fits |
|---|---|---|
| **Retention** | % of cohort active in week N | Long-term stickiness |
| **Engagement** | Actions per active user per week | Depth of use, not just presence |
| **Revenue** | Cumulative ARPU by week N | LTV trajectory, plan-tier comparison |

**Rule:** "Active" must have a one-line definition (e.g., "≥1 review
generated in the week"). Don't use a vendor-default that you can't explain.

### 3. Window + Comparison Cohorts

Define the analysis window and the cohorts to compare.

**Rules:**
- **Window length** must be ≥4 weeks for retention, ≥8 weeks for revenue.
  Shorter windows can't separate signal from week-to-week noise.
- **At least 3 cohorts** to compare. Two cohorts can always be told a
  story; three reveals trend.
- **Apples-to-apples:** cohorts must have had the same opportunity to
  reach the metric (don't compare a 12-week-old cohort to a 2-week-old
  cohort on "week-8 retention" — the young cohort hasn't gotten there).
- **Minimum cohort size:** 30 users per cohort for retention; 100 for
  engagement; 50 for revenue. If smaller, name it as exploratory and do
  not commit a decision off the result.

### 4. Actionable Threshold (set BEFORE looking)

The threshold that triggers a decision. Write it out before opening the
data.

**Template:**
> If {cohort comparison} shows {specific gap or curve} at {week N}, we
> {specific action}. If it shows {opposite}, we {opposite action}.
> Otherwise, we monitor for {N more weeks} before acting.

**Rules:**
- "Act" must be concrete: ship X, kill Y, double down on channel Z.
- "Monitor" is a valid outcome only with a defined re-look date.
- If you can't write the threshold before looking, the analysis isn't
  ready — go back to Decision 1 and sharpen the question.

## Reading the Data

After Decisions 1–4 are locked, look at the cohorts. Surface:

1. **Curves.** Plot or describe each cohort's metric over the window.
2. **Divergence.** Where do cohorts separate, and by how much?
3. **Named cohorts.** Give each cohort a memorable label (e.g.,
   "Post-pricing-change cohort", "Indie Hackers channel cohort") — abstract
   labels like "Cohort 3" cost more than they're worth.
4. **Sample-size caveats.** Flag any cohort below the minimum from
   Decision 3.

Do **not** average across cohorts in the headline. Averages hide the
divergence the analysis exists to find.

## Output

```
# Cohort Analysis — {question} — {date}

## Setup
- Axis: {…}
- Metric: {definition}
- Window: {N weeks}, cohorts {list}
- Pre-set threshold: {…}

## Results

| Cohort | n | Week 1 | Week 2 | … | Week N |
|---|---|---|---|---|---|
| {Cohort A} | {…} | {…} | … | | |
| {Cohort B} | … | | | | |

## Divergence
- {specific observation, e.g., "Cohort B retention plateaus at 35% by
  week 4; Cohort A continues to decline to 18%"}
- {…}

## Threshold Check
- Threshold met? {YES / NO / EXPLORATORY (sample too small)}
- Triggered action: {specific action}

## Caveats
- {Sample-size, instrumentation, or definitional caveats}
```

If the threshold check came back NO and the user asks to "look closer",
that's the sign the threshold was wrong. Name it and decline to fish for
a secondary read — re-run the framework with a new question instead.

## Persistence

The skill is conversation-first. Persist **only** when the analysis
surfaces an experiment-worthy signal worth carrying forward:

- Divergence large enough to act on AND the action is non-trivial →
  append H2 block to `context/product/experiments.md` with
  `session:pending`, hypothesis: the cohort divergence's likely cause.
- Otherwise: do not write to `context/`. Cohort analyses are repeated
  artifacts; cluttering `experiments.md` with every read degrades it.

Ask the user before writing.

## Worked Example — Threshold Excerpt

**Question:** Did the v2 onboarding (shipped 6 weeks ago) improve week-4
retention?

**Pre-set threshold:** *"If the post-onboarding-v2 cohort shows week-4
retention ≥5 percentage points above the pre-change cohort, we
keep v2 as default and run `/log-decision` (Type: Scope) to make it
permanent. If it's ≤2pp above or below, we revert. Between 2 and 5: we
monitor 2 more weeks before deciding."*

This is a real threshold — it commits the action in advance and leaves
no room to argue with the data after the fact.

## Capture Learning

After delivering the analysis, append one H3 entry to
`context/learnings/cohort-analysis.md` (create with
`# Learnings — cohort-analysis` H1 if missing). Newest first. Mark
`session:pending` — `/context-sync` will reconcile.

```markdown
### {one-line headline of what made this analysis distinctive} {#headline-slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD skill:cohort-analysis session:pending -->

**Worked:** {one sentence — which axis / metric / threshold choice surfaced the real signal}.
**Missed:** {one sentence — false signal, undersized cohort, threshold mis-set}.
**Next time:** {one adjustment — sample-size rule, axis choice heuristic, threshold phrasing}.
```

Keep entries three lines, not three paragraphs.

## Follow-ups

Contextual to what the analysis surfaced:

- Divergence found, cause unknown → `/design-experiment` to test the
  hypothesis behind it.
- Behavior shift is the headline → `/log-signal` (Type: Internal
  Learning) with the cohort data inline.
- Divergence implies a decision → `/log-decision` (Type: Scope or
  Go-to-Market) committing the action triggered by the threshold.
- Sample sizes too small across the board → not a cohort-analysis
  problem; user needs more volume before retrying. Note and stop.

## Anti-Patterns

- **Averaging across cohorts in the headline.** Averages hide divergence
  — exactly what the analysis exists to find.
- **Vanity metrics.** "Total signups by cohort" tells you nothing about
  stickiness; pick a real metric.
- **Sample sizes too small.** Calling a result off 12 users is gambling
  with a chart. Name the sample-size threshold and respect it.
- **No threshold set before looking.** Without it, every result becomes
  "interesting" and nothing changes.
- **Moving the threshold after results come in.** That's motivated
  reasoning. If the threshold was wrong, that's a learning for the next
  analysis — not a license to rerun this one.
- **Crosshatching axes.** Don't split a single chart by both signup
  cohort AND channel AND plan tier; pick one axis per analysis.
