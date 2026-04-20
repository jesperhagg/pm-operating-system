---
description: Structure a pricing decision. Picks a value metric, sets an anchor price, designs tiers, and proposes a WTP validation test before committing. Forces pricing before polish.
---

# Pricing

Solo founders usually price too late and too low. This skill forces the pricing decision early — before the polish phase, before distribution spend — and produces a specific number to test, not a range to debate.

Output: a value metric, an anchor price, 2–3 tiers, and a willingness-to-pay (WTP) validation plan.

## When to Use

- Before launch: setting v1 pricing.
- Post-launch: repricing after retention/conversion data comes in.
- Mid-build: when scope creep is pushing the cost basis up and pricing assumptions need revisiting.

If you have no persona yet → run `/define-persona` first. Pricing without a persona is guessing what a generic user would pay.

## Before Starting — Self-Hydration

1. Identify the product being priced (read host repo's CLAUDE.md, or ask).
2. Read:
   - `data/personas/index.md` and the primary persona file at `data/personas/{slug}.md`.
   - Grep `data/signals/active.md` for WTP or "too expensive" / "worth it" / pricing language (last 90 days).
   - `data/decisions/index.md` — filter `Type: Pricing` (all history) and open relevant decision files.
   - Current cost-per-user estimate from any PRD in `docs/` or prior `systems-architect` notes in `data/knowledge/reference/`.
   - `data/knowledge/market-landscape/*.md` — most recent `## Scan —` section, looking for competitor price points.
3. Briefly recap to the user: *"Pricing for {product}. Persona: {name}. Unit cost: {$X or unknown}. {N} competitor price points on file. Proceed?"*

If `data/personas/` is empty, halt and suggest `/define-persona` first — pricing without a persona is guessing.

## Framework — 5 Decisions

### 1. Pick the Value Metric

The value metric is *what you count to charge*. It determines whether pricing scales with customer value.

| Metric type | Examples | When to use |
|---|---|---|
| **Per-seat** | $X/user/month | Team tools where more users = more value. |
| **Per-usage** | $X/1000 API calls, $X/GB | Infra or AI where cost scales with load. |
| **Per-outcome** | $X/deal closed, $X/review completed | When customer measures ROI directly. |
| **Per-capacity** | $X up to N projects/products | Solo tools where user count = 1 but usage scales. |
| **Flat** | $X/month, unlimited | Simple, predictable, leaves money on the table at the top. |

**Rules:**
- The value metric must rise as the customer's value rises. If it doesn't, you've picked a proxy — reconsider.
- Default for solo-user tools: per-capacity (projects, products, reviews). Avoid per-seat for tools a single person uses.
- If you can't explain the metric in one sentence, customers won't either. Simplify.

**Bad:** *"Pro tier — more features."* (No metric. Just gating.)
**Good:** *"$X/month per active product tracked."* (Clear value scaling.)

### 2. Set the Anchor Price

The anchor is your primary tier price. It sets all expectations around it.

**Template:**
> Anchor: **${X}** per {value metric unit} per month.

**Approaches (pick one, state which):**

| Approach | Formula | When it fits |
|---|---|---|
| **Cost-plus** | Unit cost × 5–10 (for SaaS) | When you know unit cost and margin matters. |
| **Value-based** | 10% of quantified value delivered | When you can quantify ROI (time saved, revenue added). |
| **Competitive** | Anchor ±20% of nearest comparable | When category has established price points. |
| **Indie-maker** | $10 / $25 / $50 / $100/month psychological steps | When category is new and category-making matters more than capture. |

**Rules:**
- State the approach explicitly. "$29/month because competitors are $25–$39" is a choice. "$29/month because it felt right" is not.
- For solo-PM / indie-maker tools: default to $10, $25, $50, or $100/month anchors. Tiny price steps send "hobby tool" signal. Big steps send "serious tool."
- Cost-plus at 5× minimum for SaaS (accounts for CAC, support, churn).
- If unit cost is unknown AND product is AI/infra heavy → halt. Consult **systems-architect** first. Pricing without cost visibility is betting.

### 3. Design Tiers (Max 3)

**Template:**

| Tier | Price | Value metric allowance | Who it's for |
|---|---|---|---|
| Free / Starter | $0 | {limited allowance — acts as demo/trial, not long-term home} | {trial users} |
| **Anchor** | ${X} | {the primary bucket} | {primary persona} |
| Pro / Team | ${2–3× X} | {generous allowance + 1–2 differentiated features} | {power users, teams} |

**Rules:**
- Three tiers max. Four confuses. Two is fine if pricing is simple.
- Free tier is optional — only include if (a) zero marginal cost per free user OR (b) viral/network-effect dynamics. Otherwise default to a trial, not a free tier.
- The Anchor tier should be where ~70% of revenue lives. Tier placement is deliberate.
- Don't gate killer features behind Pro unless you want the free/starter tier to be a dead end. Free users won't upgrade for features they never tried.
- Annual discount: default 2 months free (17% discount). Don't over-discount annual — it tanks MRR predictability.

**Anti-gating rules:**
- ✅ Gate: scale (more products, more users, more API calls), team features (SSO, roles, audit log), priority support.
- ❌ Don't gate: core value prop, onboarding, basic reporting. These drive activation.

### 4. WTP Validation Plan

Pricing is a hypothesis. Test it before committing.

**Method options (pick 1–2 based on stage):**

| Method | Cost | When it fits |
|---|---|---|
| **Price-sensitivity interviews** | Hours | Pre-launch, no traffic yet. 5–10 target-persona calls asking "what would you expect this to cost?" and "at what price is this too expensive to take seriously?" |
| **Van Westendorp survey** | Day | 30+ respondents. Four questions: too cheap / bargain / expensive / too expensive. Outputs acceptable price range. |
| **Landing page price test** | Days | A/B two price points on the same landing page. Measure signup rate. Clean read on elasticity. |
| **Stripe checkout observation** | Days | Real paid checkout at anchor price. Measure cart completion rate. Kill if < 20% of "interested" users convert. |

**Rules:**
- Don't skip validation because "we can always change it later." Changing price post-launch is painful — customers churn or feel cheated.
- For paid validation: use a 14-day refund guarantee to reduce friction without discounting.
- Sample size minimum: 30 qualified responses for surveys, 100 unique visitors for landing page tests, 10 checkout attempts for Stripe observation.

### 5. Price Floor and Ceiling (Kill Criteria)

Set these BEFORE launch:

**Template:**
> - **Raise price if:** {specific signal — e.g., "> 50% of interviews say 'that's cheap,' or cart conversion > 40%"}.
> - **Lower price / reconsider if:** {specific signal — e.g., "cart conversion < 15% or > 40% of respondents flag 'too expensive'"}.
> - **Kill bet if:** {pricing can't clear unit cost × 3 AND persona's WTP ceiling}.

**Rules:**
- If unit cost × 3 exceeds WTP ceiling, the business doesn't work at this persona. Either change persona or change product.
- Don't adjust price to salvage a failed WTP test. Pricing is a symptom — the problem is usually persona-fit or value-prop clarity.

## Output

```
# Pricing — {product} — {date}

## Value Metric
{metric + one-sentence rationale}

## Anchor Price
${X} per {unit} per month (approach: {cost-plus / value-based / competitive / indie-maker})

## Tiers

| Tier | Price | {Value metric} | For |
|---|---|---|---|
| {...} | {...} | {...} | {...} |

## Validation Plan
- Method: {...}
- Sample target: {N}
- Duration: {days/weeks}
- Decision thresholds: raise if {X}, lower if {Y}, kill if {Z}

## Unit Economics Check
- Est. unit cost at anchor usage: ${...}
- Gross margin at anchor: {%}
- CAC ceiling (payback ≤ 12 months): ${...}

## Risks
- {risk + mitigation}
```

## Worked Example

**Product:** Hosted `/weekly-review` SaaS for solo multi-product PMs.

**Value Metric:** Per active product tracked per month. (Value scales with how many products a PM is juggling — the exact pain being solved.)

**Anchor Price:** $15 / active product / month. Approach: indie-maker. Rationale: Solo PMs managing 2 products hit $30/month — below Notion's $20/user but above "hobby" signal. At 3 products ($45), still below a single SaaS subscription they'd expense.

**Tiers:**

| Tier | Price | Active products | For |
|---|---|---|---|
| Starter | $0 | 1 product, 30-day trial | First-time evaluators |
| **Anchor** | $15 / product / month | Unlimited | Solo PMs with 2–5 products |
| Team | $49/month flat | Unlimited + 3 seats | Partnerships / indie studios |

**Validation Plan:**
- Method: Landing page A/B test ($15/product vs. $25/product) + 5 persona interviews.
- Sample target: 300 unique visitors per variant; 5 interviews.
- Duration: 14 days.
- Decision: Raise to $25 if signup rate parity (<10% diff). Lower to $10 if $15 variant < 2% signup. Kill if neither variant > 2%.

**Unit Economics Check:**
- Est. unit cost: $2/product (Notion API + Claude synthesis + hosting). At 3 products = $6 cost, $45 revenue → 87% gross margin.
- CAC ceiling: ~$180 for 12-month payback at $45 ARPU with 90% retention.

**Risks:**
- Per-product metric may confuse teams. Mitigation: Starter tier has 1 product to reduce decision friction at top of funnel.
- Unit cost scales with Claude synthesis usage. Mitigation: Cap synthesis depth on Starter; meter it on Anchor.

## Anti-Patterns

Reject or redirect these:

- **Pricing by gut feel** — "$29 feels right" isn't pricing, it's a wish. Name the approach.
- **Copying competitor pricing without the cost basis** — competitors may have different unit economics. Reason from your costs AND your value.
- **"We'll figure out pricing later"** — later is too late. Cost, persona, and willingness-to-pay are intertwined. Deferring pricing defers the honest check on unit economics.
- **Infinite tiers** — every extra tier is a confused prospect. Max 3.
- **Gating the core value prop** — free tiers that don't deliver value produce no upgrades. Free must prove value; Pro must add scale.
- **Psychological-pricing tricks at the anchor** ($29.99) — for B2B / solo-PM tools, round numbers ($25, $29, $49) signal professional. Cents signal consumer.
- **Lifetime deals on AppSumo etc.** — for SaaS with per-user cost, lifetime deals guarantee negative unit economics. Avoid unless product has near-zero marginal cost.

## Follow-ups

Contextual to what pricing surfaced:

- Validation plan designed → `/design-experiment` to formalize Ship/Kill thresholds for the WTP test.
- Unit cost unclear or AI-heavy → consult **systems-architect** to model cost-per-user at 100 / 1K / 10K MAU.
- Gross margin < 50% at anchor → consult **systems-architect** on cost reduction OR revisit persona for higher-WTP segment.
- Pricing changes strategy → `/log-decision` (Type: Go-to-Market) capturing value metric, anchor, and kill criteria.
- WTP test fails → `/sunset-product` (Park with revisit trigger: "pricing works when {condition}").
- Pricing needs distribution strategy → consult **growth-engineer** on channels that match the anchor price point.
