---
description: Evaluate a startup or product opportunity from a solo-founder / indie-builder lens. Scores 4 dimensions (Market, Competition, Founder Fit, Feasibility) on indie-scale anchors, then generates 2–3 concrete go-to-market strategies and ranks them by likelihood of success. Fetches existing opportunity backlog and competitive landscape from Notion.
---

# Evaluate Opportunity

Score a product/startup opportunity from a solo-founder / indie-builder perspective, then generate and rank concrete strategies for pursuing it. Output is a scored summary + ranked strategy options + a recommended path.

The lens: **not chasing $B markets**. Optimizing for "buildable by one person, makes real money, defensible enough that I'm not crushed in month 6."

## Before Starting — Self-Hydration

1. Identify whether this is for an existing product or a new exploration (read host repo's CLAUDE.md; ask if ambiguous).
2. Use Notion MCP to fetch:
   - Current opportunity backlog (all products/bets)
   - Prior evaluations or scoring for similar opportunities
   - Competitive landscape (Knowledge Base → Market Landscape) if one exists
   - Active Decisions about market focus or resource allocation
3. Briefly summarize what's already in the portfolio before scoring the new opportunity.

If Notion MCP is unavailable, halt and say so — do not score without portfolio context.

## Scoring Framework

Score each dimension 1–5 using the anchors below. **A score must cite specific evidence** (Notion Signal, KB entry, public data, or stated assumption). Unsupported scores default to the lower anchor.

### 1. Market (indie-scaled)

Sized for what one person can realistically capture, not TAM theatre.

| Score | Anchor |
|---|---|
| 1 | Hobby market. Hard to imagine >$2K MRR ceiling. Audience tiny, broke, or both. |
| 2 | Niche but thin. Plausible $2–5K MRR. Buyers exist but are hard to reach or won't pay much. |
| 3 | Lifestyle-business range. $5–20K MRR plausible in 12 months. Reachable audience, willing to pay, clear pain. |
| 4 | Durable indie business. $20–50K MRR plausible in 12 months. Growing demand, clear willingness to pay, multiple buyer segments. |
| 5 | Indie cash machine. $50K+ MRR plausible in 12 months OR 1K+ paying users reachable. Tailwind (new platform, regulation, behavior shift) actively pulling demand in. |

### 2. Competition

Even as a solo, you need to know the shape of the field.

| Score | Anchor |
|---|---|
| 1 | Saturated. Multiple well-funded incumbents + dozens of indie clones. No defensible wedge. Race to the bottom on price. |
| 2 | Crowded. Several established players. Differentiation possible but easy to copy (UX, price, one feature). |
| 3 | Active but with whitespace. 2–4 serious players, clear underserved segment / workflow / price tier. A solo can carve a niche. |
| 4 | Sparse or fragmented. Incumbents are slow, generic, or structurally can't serve this niche. Solo-defensible wedge (taste, speed, community, distribution). |
| 5 | Empty or asleep. No direct competition, OR incumbents actively ignore this segment. Wedge compounds (audience, content, data, integration depth). |

### 3. Founder Fit

| Score | Anchor |
|---|---|
| 1 | No domain knowledge, no access to customers, no obvious path in. |
| 2 | Adjacent experience. Need 3+ months to build competence. Cold outreach to reach first users. |
| 3 | Some domain familiarity. Direct access to 5–10 prospective users via network. Sustained interest plausible. |
| 4 | Deep domain experience OR warm access to 25+ prospective users. Strong conviction. |
| 5 | Uniquely positioned — lived experience, insider network, or rare expertise. Direct access to 50+ ideal users. Couldn't-stop-if-I-tried conviction. |

### 4. Feasibility

| Score | Anchor |
|---|---|
| 1 | Requires capability you don't have (regulated, hardware, specialized ML, large team). MVP > 6 months. |
| 2 | Technically possible but stretches stack. MVP 2–6 months. Unknown cost tail. |
| 3 | Buildable with current stack. MVP 4–8 weeks. Cost-per-user bounded. |
| 4 | Buildable with current stack. MVP 1–2 weeks. Cost model understood within 2x. |
| 5 | Prototype in days. Cost-per-user known. You've built something like this before. |

## Strategy Generation

After scoring, generate **2–3 distinct strategies** for actually pursuing this opportunity. Strategies are concrete go-to-market + product shapes, not generic advice.

Each strategy must specify:
- **Shape** — what you build + how you charge (e.g. "open-source CLI + paid cloud", "$29/mo SaaS sold via cold outreach", "free tool + paid templates marketplace", "one-time purchase desktop app", "consulting → productize").
- **Wedge** — the specific reason this beats incumbents for a specific buyer.
- **First 100 users** — concrete acquisition channel (community, SEO, cold outreach, content, partner, marketplace).

Score each strategy on:

| Field | Notes |
|---|---|
| **Likelihood (1–5)** | Honest probability this actually reaches $5K MRR in 12 months given the dimension scores above. |
| **Time to first $1** | Weeks. Be specific. |
| **Why it could fail** | One sentence — the most likely failure mode (not a list). |
| **What would unlock 5★** | One concrete change (a partnership, a piece of evidence, a skill) that would push likelihood up. |

Strategies should be genuinely different — varying the buyer, the channel, the price model, or the build shape. Two flavors of "B2B SaaS with cold outreach" is one strategy, not two.

## Output

```
# Opportunity Evaluation — {opportunity name} — {date}

## Summary
{2–3 sentences: what the opportunity is and why it's worth a look now.}

## Scores

| Dimension | Score | Reasoning (with evidence) |
|---|---|---|
| Market (indie-scaled) | {1–5} | {anchor-backed reasoning + citation} |
| Competition | {1–5} | {...} |
| Founder Fit | {1–5} | {...} |
| Feasibility | {1–5} | {...} |
| **Total** | **{sum}/20** | |

## Strategies

### Strategy A — {short name}
- **Shape:** {build + pricing}
- **Wedge:** {specific reason this wins for a specific buyer}
- **First 100 users:** {concrete channel}
- **Likelihood:** {1–5}
- **Time to first $1:** {weeks}
- **Why it could fail:** {one sentence}
- **What would unlock 5★:** {one concrete change}

### Strategy B — {short name}
{same fields}

### Strategy C — {short name, optional}
{same fields}

## Recommendation
**{Pursue Strategy X / Pursue narrow / Park / Kill}**

- **Pursue** — best strategy ≥ 4 likelihood, dimension total ≥ 14, no dimension < 3. Ship the first validation step this week.
- **Pursue narrow** — best strategy = 3 likelihood, dimension total ≥ 12. Worth a time-boxed test (2–4 weeks) before committing.
- **Park** — no strategy ≥ 3 likelihood, OR one dimension = 1. Note the trigger that would change the call.
- **Kill** — no strategy ≥ 3 AND dimension total < 10. Don't pursue.

{One sentence on why this strategy beats the others.}

## Next Steps
1. {Concrete validation step for the recommended strategy this week.}
2. {...}
3. {...}

## Suggested Notion Update
- Add to Opportunity Backlog with status: {Pursue / Park / Kill} and the chosen strategy name.
- Log a Decision (Type: Kill/Park) if this supersedes an active bet.
```

## Worked Example

**Opportunity:** AI-powered weekly review tool for solo PMs.

| Dimension | Score | Reasoning |
|---|---|---|
| Market (indie-scaled) | 3 | Solo PM / indie maker audience ~200K worldwide (Indie Hackers 2025). $5–20K MRR plausible at $20/mo with 250–1000 paying users. Pain real but not bleeding — willingness-to-pay unproven. |
| Competition | 3 | Linear, Notion AI, Height cover adjacent ground but none focus on portfolio-level rollup for multi-product solos. Whitespace exists; not empty. |
| Founder Fit | 5 | Built PM OS plugin. 10+ yrs PM experience. Direct access to 50+ solo-PM peers via founder network. |
| Feasibility | 5 | Skill framework + Notion integration already running. MVP = 1 week. |
| **Total** | **16/20** | |

### Strategy A — Hosted /weekly-review SaaS
- **Shape:** $19/mo hosted version of the existing `/weekly-review` skill. Login + Notion OAuth. Weekly digest emailed.
- **Wedge:** Only tool that rolls up *multiple* products for one PM. Linear/Notion are single-workspace.
- **First 100 users:** Indie Hackers + r/ProductManagement posts; founder network DM (50 warm).
- **Likelihood:** 4
- **Time to first $1:** 3 weeks (1 wk MVP, 2 wks waitlist → launch).
- **Why it could fail:** Solo PMs already cobble this together in Notion and won't pay $19/mo for the polish.
- **What would unlock 5★:** 10 of the 50 warm contacts pre-pay before MVP ships.

### Strategy B — Free OSS plugin + paid team tier
- **Shape:** PM OS plugin stays free + open. Paid tier ($49/mo) for shared team digests, multi-user Notion sync.
- **Wedge:** Distribution via the OSS plugin you already ship. Upgrade path is automatic for power users.
- **First 100 users:** Existing plugin users — convert 5–10% to paid.
- **Likelihood:** 3
- **Time to first $1:** 6 weeks (need real install base first).
- **Why it could fail:** Plugin install base is too small to convert meaningfully; team buyers need different positioning entirely.
- **What would unlock 5★:** Plugin hits 500+ active installs first.

### Strategy C — Productized weekly review service
- **Shape:** $200/mo done-for-you weekly review for solo founders. You + the skill do the work; deliver async.
- **Wedge:** Buyers who want the *outcome* (clarity), not another tool to maintain.
- **First 100 users:** Cold outreach to indie founders w/ 2+ products on Twitter/X.
- **Likelihood:** 2
- **Time to first $1:** 2 weeks.
- **Why it could fail:** Doesn't scale solo past ~15 clients; high-touch capacity ceiling kills it before it compounds.
- **What would unlock 5★:** Productize delivery to <30 min/client/week.

## Recommendation
**Pursue Strategy A.**

Highest likelihood, fastest revenue, leverages founder fit and warm network. Strategy B is the right *follow-on* once A proves WTP; Strategy C trades long-term ceiling for short-term cash and isn't worth it given A's 3-week timeline.

## Next Steps
1. DM 10 of the 50 warm contacts this week — frame: "would you pre-pay $19/mo for hosted weekly review of all your products?"
2. If ≥3 yes → ship the 1-week MVP.
3. If <3 yes → revisit. The pain isn't sharp enough at this price.

## Follow-ups

Contextual to the recommendation:

- **Pursue** → suggest `/design-experiment` to frame the first validation test for the chosen strategy.
- **Pursue narrow** + low Feasibility → suggest consulting the **systems-architect** agent on the tech cost ceiling.
- **Park** → `/log-decision` with Type: Park, noting the trigger to revisit.
- **Kill** → `/log-decision` with Type: Kill, linking the evaluation as context.
- Any verdict: suggest updating the Notion opportunity backlog with the chosen strategy name.
