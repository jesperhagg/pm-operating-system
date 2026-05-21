---
description: Define an Ideal Customer Profile — the segment to sell to — across 7 dimensions including required disqualifiers and a fit-score rubric. Solo-founder lens: emphasizes accessibility and willingness-to-pay, not enterprise procurement. Writes H2 blocks to context/users/icp.md.
---

# Ideal Customer Profile

A persona describes the *individual buyer* (JTBD, pain, trigger). An ICP
describes the *segment we sell to* (who qualifies, who explicitly does
not, and how to score fit). Most teams conflate the two and end up with
neither.

This skill produces an ICP with mandatory disqualifiers (so the team can
say "no") and a fit-score rubric (so prospects can be triaged in seconds,
not deliberated).

## When to Use

- Before any GTM motion — cold outreach, content, partnerships — to
  define who the motion targets and who it ignores.
- After 10+ leads have flowed through `context/ops/leads.md`, to codify
  what won vs. lost patterns reveal.
- Before `/pricing` — pricing without an ICP overweights generic
  willingness-to-pay assumptions.

## Before Starting — Self-Hydration

1. Identify the current product (read host repo's CLAUDE.md, or ask).
2. Read:
   - Grep `context/users/personas.md` for H2 headings; read the primary
     persona block (ICP refines outward; persona is one buyer inside it).
   - `context/ops/leads.md` — full board. Note wins, losses, and any
     "didn't fit" / "didn't qualify" patterns in the Status column.
   - Sample 2–3 won and 2–3 lost lead-detail files from
     `context/ops/leads-detail/` to identify patterns.
   - `context/market/landscape.md` — most recent `## Scan —` section for
     competitor positioning and who else is going after the same
     segment.
   - Grep `context/users/feedback.md` for "would buy" / "wouldn't buy" /
     "not for us" language in the last 90 days.
   - If `context/users/icp.md` exists, read existing ICP blocks (refine
     vs. add new).
   - If `context/learnings/ideal-customer-profile.md` exists, read the
     top 3–5 H3 entries. Apply silently to this run — do not narrate
     prior lessons back to the user.
3. Brief the user: *"Defining ICP for {product}. {N} leads on file
   ({W} won, {L} lost). Primary persona: {name}. New ICP, refining
   existing, or replacing?"*

If `context/ops/leads.md` is empty AND `context/users/feedback.md` has
fewer than 5 entries, halt: *"ICP without lead data or feedback is a
guess. Run discovery (interviews, cold outreach with a hypothesis ICP)
for 2–4 weeks before formalizing."*

## ICP ≠ Persona

This skill defines the **segment to sell to**. It is *broader* than a
persona (a segment contains many buyers) and *narrower* than a market
(a market contains many segments).

| | ICP | Persona |
|---|---|---|
| **Granularity** | Segment (firmographics, trigger, qualifier) | Individual (JTBD, pain, workaround) |
| **Used for** | GTM targeting, qualification, pricing | PRD framing, UX decisions, copy |
| **Required field** | Disqualifiers | Anti-persona |

If the user wants a persona instead, redirect to `/define-persona`.

## Framework — 7 Dimensions

Every ICP fills these 7 fields. Skipping any defaults that dimension to
`assumption: untested` and flags the gap in the output.

### 1. Firmographics

The structural attributes of the company / household / individual buyer.

**Template:**
> - Size: {employee count range, ARR, or "solo individual"}
> - Stage: {pre-revenue / early / scaling / mature}
> - Geo: {regions, with rationale — language? payment? regulation?}
> - Industry / segment: {specific, not "tech"}

**Rules:**
- "Solo individual" is a valid size — solo-founder lens often sells to
  one-person teams. Don't force B2B framing on B2C economics.
- Geo restrictions must have a *reason* (Stripe support, language,
  business hours, regulation). "US-only" with no reason is laziness.

### 2. Tech Stack (or Equivalent Environment)

What the buyer already has in place that we plug into, replace, or
require.

**Template:**
> - Required: {tools/platforms the ICP must already use}
> - Preferred: {tools that make adoption easier}
> - Disqualifying: {tools that mean we don't fit}

**Rules:**
- For non-software ICPs, substitute "process" or "environment". Don't
  skip — solo founders are bad at recognizing environmental
  prerequisites.
- Disqualifying tools are often more useful than required ones — they
  prevent wasted sales cycles.

### 3. Use Case

The specific job they hire the product for.

**Template:**
> They use {product} to {specific outcome} when {specific trigger
> situation}.

**Rules:**
- One primary use case per ICP. Multiple use cases = multiple ICPs.
- Use case must be specific enough that someone outside the ICP would
  read it and say "that's not me" — not just "huh, that sounds nice".

### 4. Buying Trigger

The discrete event that starts the buying motion. Without a trigger,
the deal sits in "we'll think about it" forever.

**Template:**
> They start evaluating us when {discrete event — hiring, pricing
> change, scale milestone, calendar event, product launch, post-mortem,
> compliance deadline}.

**Rules:**
- Must be an event, not a state ("they have N users" is a state; "they
  hit N users and reorganize roles" is an event).
- If the trigger is "they hear about us", the ICP is broken — that's
  marketing, not a trigger.

### 5. Buying Committee

Who's involved in the purchase decision. For solo-founder lens, this is
often just one person — name them anyway.

**Template:**
> - **Decision-maker:** {role + how to reach them}
> - **Influencers:** {who else weighs in, even informally}
> - **Blockers:** {who can say no without an upside — security,
>   procurement, legal, partner}

**Rules:**
- If the buying committee has 5+ roles, the ICP is enterprise —
  reconsider whether the solo-founder lens applies.
- For consumer / prosumer products: decision-maker = the user; blocker
  = "their own time / attention" — name it.

### 6. Disqualifiers (MANDATORY, non-empty)

Explicit list of attributes that mean we **do not pursue** this prospect,
even if they're warm.

**Rules:**
- This field must have at least 3 entries. Disqualifiers force
  sharpness; ICPs without them are aspirations, not segments.
- Each disqualifier names the *signal you'd see early* (so you can spot
  it before investing 3 calls).
- Common solo-founder disqualifiers: requires SOC 2, requires custom
  contract, wants on-prem, expects <24h support, asks for white-label
  on first call.

### 7. Fit-Score Rubric

A 1–5 score for inbound and outbound prospects, with criteria for each
level.

**Template:**

| Score | Criteria |
|---|---|
| 5 | Matches firmographics, tech stack, AND trigger event recent (<30 days) |
| 4 | Matches firmographics + tech stack; trigger not yet observed |
| 3 | Matches firmographics; tech stack partial |
| 2 | Adjacent segment; one disqualifier present but mitigable |
| 1 | Disqualifier present; do not pursue |

**Rules:**
- Score must be assignable in under 60 seconds per prospect. If it
  requires a sales call to score, the rubric is too vague.
- 1 means "don't pursue" — the rubric has teeth or it's decoration.

## Output

Append a new H2 block to `context/users/icp.md`. If the file does not
exist, create it with `# ICP` H1 header (defensive — `/context-init`
does not pre-scaffold this file).

Insert the new block at the **top** of the file (newest first), after
the H1 header:

```markdown
## {Short ICP name} {#slug}
<!-- last_updated:YYYY-MM-DD source_evidence:[context/ops/leads.md, context/users/feedback.md#anchor] session:pending -->

**Firmographics:**
- Size: {…}
- Stage: {…}
- Geo: {…}
- Industry: {…}

**Tech stack:**
- Required: {…}
- Preferred: {…}
- Disqualifying: {…}

**Use case:**
{one sentence}

**Buying trigger:**
{discrete event}

**Buying committee:**
- Decision-maker: {role + reach}
- Influencers: {list}
- Blockers: {list}

**Disqualifiers (min 3):**
- {…}
- {…}
- {…}

**Fit-score rubric:**

| Score | Criteria |
|---|---|
| 5 | {…} |
| 4 | {…} |
| 3 | {…} |
| 2 | {…} |
| 1 | {…} |

**Discovery gaps:** {list any fields marked `assumption: untested`, or "none"}

---
```

Return a short summary:

```
## ICP Defined
**Name:** {short name}
**Disqualifiers:** {N}
**Fit-score rubric:** complete (1–5)
**Appended to:** context/users/icp.md (#{slug})
**Open gaps:** {any TODOs / untested assumptions}
```

## Worked Example — Disqualifiers Excerpt

For a hosted weekly-review SaaS targeting solo multi-product PMs,
realistic disqualifiers include:

- **Requires SOC 2 / SSO** — signals enterprise procurement; solo
  product can't economically clear that bar in v1.
- **Team of 5+ wanting shared workspace** — different product (team
  tier); refer instead of selling.
- **Wants white-label / custom domain on first call** — agency buyer,
  not solo-PM ICP.

Each of those is observable in the first email or Discord DM, before
investing a call.

## Capture Learning

After defining the ICP, append one H3 entry to
`context/learnings/ideal-customer-profile.md` (create with
`# Learnings — ideal-customer-profile` H1 if missing). Newest first. Mark
`session:pending` — `/context-sync` will reconcile.

```markdown
### {one-line headline of what made this run distinctive} {#headline-slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD skill:ideal-customer-profile session:pending -->

**Worked:** {one sentence — which dimension sharpened the segment fastest}.
**Missed:** {one sentence — over-broad disqualifier, vague trigger, weak rubric}.
**Next time:** {one adjustment — dimension order, disqualifier minimum, rubric phrasing}.
```

Keep entries three lines, not three paragraphs.

## Follow-ups

Contextual to what the ICP surfaced:

- ICP defined → `/log-lead` to apply the fit-score rubric to current
  prospects in `context/ops/leads.md`.
- Buying committee differs from expected WTP → `/pricing` to revise
  tiers against the ICP's actual price ceiling.
- ICP narrowed the persona → `/define-persona` to refine the primary
  persona to the in-ICP segment.
- ICP has 5+ untested dimensions → suggest 2–4 weeks of cold-outreach
  discovery against the *hypothesis* ICP before formalizing.
- ICP requires enterprise patterns (SOC 2, custom contracts) →
  reconsider solo-founder fit; consult **startup-advisor**.

## Anti-Patterns

- **ICP = persona conflation** — different artifacts, different uses.
  Persona is the buyer; ICP is the segment.
- **No disqualifiers** — without "who we don't sell to", every warm
  prospect gets pursued and the team drowns in low-fit deals.
- **"Any company that needs X"** — that's not a segment; it's a wish.
  Tighten firmographics + trigger.
- **Copy-pasted SaaS ICP template** — enterprise ICPs (SOC 2,
  procurement, multi-stakeholder) don't fit solo-product economics.
- **Fit-score rubric that requires a sales call** — must be scoreable
  from the inbound signal (email, form, DM). 60 seconds max.
- **Disqualifiers that are aspirations** — "we don't sell to people who
  won't pay" is not a disqualifier; it's a complaint. Disqualifiers
  must be observable signals.
