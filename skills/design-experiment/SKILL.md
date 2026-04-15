---
description: Structure a fast, falsifiable experiment to validate a hypothesis. Forces a decision rule before the experiment runs. Fits the test-before-spec working style.
---

# Design Experiment

Turn a hunch into a testable experiment. Every experiment ships with a falsifiable prediction, a success threshold, a duration, and a decision rule — so when it finishes, you act, you don't re-debate.

Use this before building anything non-trivial. Faster, cheaper, and more honest than a PRD.

## Before Starting — Self-Hydration

1. Identify the current product (read host repo's CLAUDE.md, or ask).
2. Use Notion MCP to fetch:
   - Recent Signals (last 30 days) — especially Internal Learning and User Feedback
   - Active Decisions — to anchor what's already committed
   - Prior experiments (Decisions with Type: Go-to-Market or Scope + Outcome: Pending/Validated/Invalidated)
3. Brief the user on any prior experiment that touched this hypothesis — don't re-run what's already been tested.

If Notion MCP is unavailable, proceed but flag: *"No prior-experiment context available — risk of duplication."*

## Framework

Every experiment has these 7 fields. Fill each one concretely before running.

### 1. Hypothesis

**Template:**
> **We believe** {persona or segment} will {specific action} **because** {mechanism/reason}.

- "Action" must be observable, not a feeling. "Activate" ≠ "complete step 3 within 10 minutes."
- "Because" must state the causal mechanism, not just evidence. This is what the experiment actually tests.

### 2. Falsifiable Prediction

**Template:**
> If we {do X}, then {specific metric} will {direction — increase/decrease/reach} {number} within {timeframe}.

- The metric must be measurable with existing tooling (or call out what instrumentation the experiment requires).
- The number must be specific. "A lot" is not a prediction.

### 3. Success Threshold

**Template:**
> **Ship it** if {metric} ≥ {X}.
> **Kill it** if {metric} ≤ {Y}.
> **Iterate** if {Y} < {metric} < {X}.

- Thresholds must be set **before** the experiment runs. Setting them after is motivated reasoning.
- The gap between Ship and Kill is the iterate zone — narrow is good, too narrow is paralysis.

### 4. Minimum Viable Test

The cheapest, fastest build that could produce the prediction. Rule-of-thumb options:

| Cost tier | Examples |
|---|---|
| **Zero-build** | Landing page, fake door, email to waitlist, manual concierge service, social post |
| **Hours** | Figma prototype, Typeform flow, Airtable form, one-off script |
| **Days** | Stub feature with hardcoded outputs, Zapier automation, Stripe test-mode checkout |
| **Weeks** | Only justified when Hours / Days versions can't produce the target metric |

Default to the cheapest tier that gives a real read.

### 5. Duration

**Template:**
> **Run for {N days/weeks}, or until {sample size} — whichever comes first.**

- Duration must be set before launch, not extended to chase data.
- For user-behavior experiments: minimum 2 weeks or 30 qualified users, whichever is longer.
- For conversion/copy tests: minimum 500 impressions or 2 weeks.

### 6. Decision Rule

**Template:**
> When the experiment ends:
> - Ship → {specific next action: build v1, expand channel, log Decision X}
> - Kill → {specific next action: log Decision (Kill/Park), update Signals with Internal Learning, move on}
> - Iterate → {specific next hypothesis or variable to change}

The decision rule is a pre-commitment. If you find yourself arguing with it after results come in, your thresholds were wrong.

### 7. Instrumentation Check

Before launch, confirm:
- [ ] Metric can be measured with current tooling (or build the tracking as part of the MVT)
- [ ] Baseline is known (what's the current value of this metric?)
- [ ] Sample source is defined (existing traffic? outreach list? Specific segment?)
- [ ] End date is on your calendar

## Output

```
# Experiment — {short name} — {start date}

## Hypothesis
{statement}

## Falsifiable Prediction
If {X}, then {metric} will {direction} {number} within {duration}.

## Success Threshold
- Ship: {metric} ≥ {X}
- Kill: {metric} ≤ {Y}
- Iterate: otherwise

## Minimum Viable Test
{What you're building/doing — link to artifact or describe the concierge/fake-door setup}

## Duration
{N days/weeks} OR {sample size}, whichever first. End date: {YYYY-MM-DD}.

## Decision Rule
- Ship → {action}
- Kill → {action}
- Iterate → {action}

## Instrumentation
- Metric source: {tool/query}
- Baseline: {value}
- Sample source: {where users come from}
```

## Worked Example

**Hypothesis:** We believe solo PMs running 2+ products will sign up for a hosted weekly-review tool because their current manual process takes 45–90 minutes every Monday.

**Falsifiable Prediction:** If we put up a landing page pitching "`/weekly-review` as a service for multi-product PMs" and share it in 3 Slack/Discord communities, signup rate will reach ≥ 8% of unique visitors within 14 days.

**Success Threshold:**
- Ship: signup rate ≥ 8%
- Kill: signup rate ≤ 2%
- Iterate: 2–8%

**Minimum Viable Test:** Carrd landing page with hook ("Monday review in 10 minutes, not 90"), one-sentence value prop, email capture. No product built.

**Duration:** 14 days or 500 unique visitors, whichever first. End date: 2026-04-29.

**Decision Rule:**
- Ship → `/write-prd` for the hosted product, log Decision (Go-to-Market): *"Build weekly-review SaaS, wedge = solo-PM Slack communities."*
- Kill → `/log-decision` (Kill): *"No demand signal for hosted weekly-review. Park for 6 months."* Log Signal (Internal Learning) with reply-rate data.
- Iterate → Rewrite hook, retry in different community. Max 2 iteration rounds before Kill.

**Instrumentation:**
- Metric source: Carrd built-in analytics + ConvertKit signups
- Baseline: 0 (new asset)
- Sample source: 3 Slack/Discord communities (list names), 1 post each, no DM outreach

## Follow-ups

- Experiment designed → confirm the user commits the Decision Rule before launch (via `/log-decision` with Type: Go-to-Market, Outcome: Pending).
- Result came in (Ship) → `/write-prd` for the shippable version.
- Result came in (Kill) → `/log-decision` (Kill/Park) + `/log-signal` (Internal Learning with data).
- Result came in (Iterate) → run this skill again with the new variable.
- Experiment needed distribution strategy → consult **growth-engineer** for channel selection.
- Experiment has unclear cost ceiling → consult **systems-architect**.

## Anti-Patterns

Reject or redirect these:

- **No threshold set** — "What does 'good' look like?" If you can't answer before launching, don't launch.
- **No end date** — "We'll see how it goes" is not an experiment, it's a hope.
- **Unfalsifiable prediction** — "Users will love it" isn't testable. Name the metric.
- **Building a full product as 'the experiment'** — If the MVT is 4 weeks of build, it's not an experiment, it's a bet. Shrink it or admit it's a bet and use `/write-prd`.
- **Moving the threshold after results** — The threshold is a pre-commitment. If it's wrong, that's a lesson for the next experiment, not a reason to adjust this one.
