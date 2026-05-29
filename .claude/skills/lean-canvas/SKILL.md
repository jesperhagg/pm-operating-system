---
description: Produce a Lean Canvas — 9 boxes on one page covering Problem, Customer Segment, Unique Value Prop, Solution, Channels, Revenue Streams, Cost Structure, Key Metrics, and Unfair Advantage. Each box must cite evidence from context/ or be marked `assumption: untested`. Forces concrete commitments instead of brainstorming.
---

# Lean Canvas

Adapted from Ash Maurya's Lean Canvas, tightened for solo founders: every
box requires either a citation to a real signal in `context/` or an explicit
`assumption: untested` flag. No hand-waving. The output is a one-page
artifact saved to `docs/`, not a thinking exercise that stays in chat.

Use this before committing to a build (instead of a PRD when scope is still
fuzzy) or after a major pivot to re-anchor on the current bet.

## Before Starting — Self-Hydration

1. Identify the current product (read host repo's CLAUDE.md, or ask).
2. Read:
   - Grep `context/users/personas.md` for H2 headings; read the primary
     persona block.
   - `context/market/landscape.md` — most recent `## Scan — YYYY-MM-DD`
     section (competitor positioning + price points).
   - Grep `context/product/decisions.md` for `status:Active` and
     `type:Positioning`, `type:Scope`, or `type:Pricing` (last 180 days).
   - Grep `context/users/feedback.md` for entries from the last 90 days
     (`type:"User Feedback"`).
   - If `context/users/icp.md` exists, read the primary ICP block.
   - If `context/learnings/lean-canvas.md` exists, read the top 3–5 H3
     entries. Apply silently to this run — do not narrate prior lessons
     back to the user.
3. Brief the user: *"Drafting Lean Canvas for {product}. Primary persona:
   {name}. {N} competitor positions on file. {M} recent feedback signals.
   Proceed?"*

If `context/users/personas.md` is empty AND no ICP exists, halt and suggest
`/define-persona` or `/ideal-customer-profile` first — the Customer Segment
box can't be filled without a target.

## Framework — 9 Boxes

Every box must end with either:
- **Evidence:** {anchor reference to a `context/` file}, OR
- **`assumption: untested`** with a one-line proposed validation.

Boxes filled with a generic phrase and no evidence default to
`assumption: untested`.

### 1. Problem

The 1–3 top problems the customer experiences today. Order by acuity.

**Rules:**
- Each problem must be a *pain the customer feels weekly or more often* —
  not an abstract industry trend.
- For each problem, name the **existing alternative** (the workaround the
  customer uses today). The workaround is the real competitor.

### 2. Customer Segment

The specific segment, not "everyone who could benefit."

**Rules:**
- Must be tighter than a persona category. "Solo PMs" is a category.
  "Solo PMs managing ≥2 indie products who self-identify on Indie Hackers"
  is a segment.
- Name the **early adopter** — a sub-slice within the segment whose pain
  is sharpest and who is reachable today.

### 3. Unique Value Proposition

Single, clear, compelling message. Why you are different and worth buying.

**Template:**
> {High-level outcome} for {early adopter} without {existing alternative's
> biggest cost — time / money / friction}.

**Rules:**
- One sentence. If it takes two, it isn't unique enough.
- Don't paste the competitor's claim with a different brand name on it.
- "High-concept pitch" (optional second line): one analogy in the form
  "X for Y" (e.g., "Linear for indie multi-product founders").

### 4. Solution

The smallest set of features that resolves the Problem box.

**Rules:**
- Max 3 features. If you need more, you haven't picked the riskiest
  problem.
- Each feature maps to one Problem-box item.

### 5. Channels

Path to early adopters. Not all possible channels — the **first one**.

**Rules:**
- Pick one primary channel for the first 100 users (community, SEO,
  cold outreach, partner, marketplace, content). State why it fits the
  segment.
- If you list three channels, you have no channel.
- Channel must be a place the early adopter already spends time — not
  a place you'd have to create demand.

### 6. Revenue Streams

Pricing model + anchor price.

**Rules:**
- Value metric + anchor price (run `/pricing` for the full structure if
  this box is the most uncertain).
- Must include unit economics in one line: cost per active customer at
  anchor usage → gross margin at anchor.

### 7. Cost Structure

The handful of costs that actually move the unit economics.

**Rules:**
- List only costs that scale with usage or are required for v1.
- Solo-founder reality: your time is the largest cost — name an
  hours-per-week ceiling.

### 8. Key Metrics

The 1 outcome metric + 2–3 leading indicators that signal whether the bet
is working.

**Rules:**
- One outcome metric (retention, revenue, activation rate). Pick the one
  closest to actual customer value — see `/north-star-metric` if you need
  to choose deliberately.
- 2–3 leading indicators that move *before* the outcome moves.
- **Kill-criterion for the whole bet** — a single condition that, if met,
  means we stop pursuing this canvas. Mandatory; do not skip.

### 9. Unfair Advantage

Something competitors can't easily copy or buy.

**Rules:**
- Features are not an unfair advantage. Audience, insider knowledge,
  proprietary data, distribution lock-in, and earned trust are.
- "Founder is X" is fine if X is rare and durable (e.g., "founder is the
  primary user with 10 years of domain experience").
- If the box reads "we move faster" or "better UX", mark
  `assumption: untested` and propose how to validate moat over time.

## Output

Save to `docs/lean-canvas-{product-slug}.md`. Confirm the path with the
user before writing.

```markdown
# Lean Canvas — {product} — {YYYY-MM-DD}

## 1. Problem
- {Problem 1} — existing alternative: {workaround}
- {Problem 2} — existing alternative: {workaround}
- {Problem 3} — existing alternative: {workaround}

Evidence: {anchor refs or `assumption: untested`}

## 2. Customer Segment
- Segment: {tight definition}
- Early adopter: {sub-slice + where they're reachable today}

Evidence: {…}

## 3. Unique Value Proposition
> {one-sentence UVP}

High-concept pitch (optional): {X for Y}

Evidence: {…}

## 4. Solution
- {Feature 1} → resolves Problem 1
- {Feature 2} → resolves Problem 2
- {Feature 3} → resolves Problem 3

Evidence: {…}

## 5. Channels
Primary channel for first 100 users: {channel + why it fits}

Evidence: {…}

## 6. Revenue Streams
- Value metric: {…}
- Anchor price: ${X} per {unit} per month
- Unit economics: ${cost} cost → {gross margin %}

Evidence: {…}

## 7. Cost Structure
- {cost 1} — scales with {…}
- {cost 2} — fixed
- Founder time ceiling: {N hours/week}

Evidence: {…}

## 8. Key Metrics
- **Outcome:** {metric + threshold + horizon}
- **Leading:** {1–3 indicators}
- **Kill-criterion:** {single condition}

Evidence: {…}

## 9. Unfair Advantage
{moat description}

Evidence: {…}

---

## Untested Assumptions
{Bulleted list of every box marked `assumption: untested` plus the proposed validation.}

## Riskiest Box
{Single box whose failure would kill the bet fastest — basis for next experiment.}
```

After writing, return a short summary:

```
## Lean Canvas Saved
**File:** docs/lean-canvas-{product-slug}.md
**Boxes with evidence:** {N}/9
**Boxes marked untested:** {M}/9
**Riskiest box:** {box name}
```

## Worked Example — Riskiest-Box Excerpt

For a hosted weekly-review SaaS for solo multi-product PMs, the riskiest
box might be **Channels**: the founder hypothesizes that the first 100
users come from Indie Hackers + r/ProductManagement community posts, but
no signal yet shows those communities convert at ≥2% of impressions.
Validation: post once in each community with a waitlist landing page;
ship/kill on signup rate, not engagement.

## Capture Learning

After writing the canvas, append one H3 entry to
`context/learnings/lean-canvas.md` (create with `# Learnings — lean-canvas`
H1 if missing). Newest first. Mark `session:pending` — `/context-sync` will
reconcile.

```markdown
### {one-line headline of what made this run distinctive} {#headline-slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD skill:lean-canvas session:pending -->

**Worked:** {one sentence — which boxes tightened the bet}.
**Missed:** {one sentence — which boxes stayed hand-wavy despite the rules}.
**Next time:** {one adjustment — rule tweak, evidence threshold, order shift}.
```

Keep entries three lines, not three paragraphs.

## Follow-ups

Contextual to what the canvas surfaced:

- Riskiest box identified → `/design-experiment` to frame the falsification
  test for that single box.
- Revenue Streams thin or `assumption: untested` → `/pricing` to set value
  metric, anchor, and WTP validation.
- Customer Segment vague or no ICP on file → `/ideal-customer-profile`.
- Problem box has < 2 evidence citations → `/log-signal` to capture user
  interviews before committing.
- Multiple boxes untested → `/evaluate-opportunity` to score whether the
  bet is worth pursuing at all.

## Anti-Patterns

- **Vague segment** — "SMBs", "developers", "PMs". Tighten to a sub-slice
  reachable today.
- **Copy-pasted UVP** — "fastest, simplest, easiest" is what every
  competitor claims. State the specific cost you remove.
- **Hand-waved Key Metrics** — "engagement", "retention" with no number.
  Each metric needs a threshold and a horizon.
- **Features as Unfair Advantage** — features get copied. Audience,
  data, distribution, and earned trust don't.
- **No kill-criterion** — without one, the canvas describes a hope, not
  a bet.
- **Filling every box with `assumption: untested`** — that's a brainstorm,
  not a canvas. Halt and run discovery first.
