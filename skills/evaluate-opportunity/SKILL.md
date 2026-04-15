---
description: Evaluate a startup or product opportunity against strategic criteria. Produces a 5-dimension score (1–5 anchored), verdict, and concrete next steps. Fetches existing opportunity backlog and competitive landscape from Notion.
---

# Evaluate Opportunity

Score a product/startup opportunity on five dimensions against explicit anchors. Outputs a scored summary, a verdict (Explore / Park / Kill), and concrete next steps.

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

### 1. Market Opportunity

| Score | Anchor |
|---|---|
| 1 | Niche or speculative. No sizing data. Problem is nice-to-have for target users. |
| 2 | Small or shrinking market. Rough SAM < $100M. Problem is real but low-urgency. |
| 3 | Mid-size, stable market. SAM $100M–$1B. Clear pain but not bleeding. |
| 4 | Large, growing market. SAM > $1B, growing 15%+/year. Problem users actively seek solutions for. |
| 5 | Massive, compounding market. SAM > $10B with a real tailwind (regulatory, tech shift, demographic). Problem is urgent and expensive to ignore. |

### 2. Competitive Position

| Score | Anchor |
|---|---|
| 1 | Crowded market with 5+ well-funded incumbents. No clear wedge. Table-stakes features already commoditized. |
| 2 | Several competitors, differentiation is marginal (better UX, lower price) and easy to clone. |
| 3 | 2–3 serious players, clear whitespace on one axis (segment, workflow, or price). Moat is possible but not obvious. |
| 4 | Fragmented or weak competition. Structural moat plausible (data network, switching cost, regulatory, distribution). |
| 5 | No direct competition, or incumbents structurally can't serve this need. Strong moat potential (proprietary data, exclusive distribution, regulatory capture). |

### 3. Founder Fit

| Score | Anchor |
|---|---|
| 1 | No domain knowledge, no direct access to customers, no obvious path to expertise. |
| 2 | Adjacent experience. Would need 3+ months to build competence. Cold outreach to reach first users. |
| 3 | Some domain familiarity. Direct access to 5–10 prospective users via network. Sustained interest plausible. |
| 4 | Deep domain experience (5+ years) OR warm access to 25+ prospective users. Strong conviction. |
| 5 | Uniquely positioned — lived experience, insider network, or rare expertise. Direct access to 50+ ideal users. Couldn't-stop-if-I-tried conviction. |

### 4. Feasibility

| Score | Anchor |
|---|---|
| 1 | Requires capability you don't have (regulated industry, hardware, specialized ML). MVP > 6 months. |
| 2 | Technically possible but stretches stack. MVP 2–6 months. Unknown cost tail. |
| 3 | Buildable with current stack. MVP 4–8 weeks. Cost-per-user unclear but bounded. |
| 4 | Buildable with current stack. MVP 1–2 weeks. Cost model understood within 2x. |
| 5 | Prototype in days. Cost-per-user known. You've built something like this before. |

### 5. Strategic Fit

| Score | Anchor |
|---|---|
| 1 | Orthogonal to portfolio. Would split focus and compete with existing bets for attention. |
| 2 | Weak connection. Would require new persona, new channel, new tech. |
| 3 | Neutral. Doesn't conflict but doesn't compound. |
| 4 | Reuses persona, channel, OR tech stack from an existing bet. One shared asset. |
| 5 | Compounds with existing portfolio — same persona + channel, or creates a shared data/distribution asset. Reinforces current market focus. |

## Output

```
# Opportunity Evaluation — {opportunity name} — {date}

## Summary
{2–3 sentences: what the opportunity is and why it matters now.}

## Scores

| Dimension | Score | Reasoning (with evidence) |
|---|---|---|
| Market Opportunity | {1–5} | {anchor-backed reasoning + citation} |
| Competitive Position | {1–5} | {...} |
| Founder Fit | {1–5} | {...} |
| Feasibility | {1–5} | {...} |
| Strategic Fit | {1–5} | {...} |
| **Total** | **{sum}/25** | |

## Verdict
**{Explore / Park / Kill}**

- **Explore** (total ≥ 18, no dimension < 3): worth validating. Run 2–3 concrete next steps below.
- **Park** (total 12–17, or one dimension = 1): interesting but not now. Note what would need to change to revisit.
- **Kill** (total < 12, or two dimensions = 1): doesn't pass the bar. Don't pursue.

## Next Steps (for Explore) / Trigger to Revisit (for Park)
1. {...}
2. {...}
3. {...}

## Suggested Notion Update
- Add to Opportunity Backlog with status: {Explore / Park / Kill}
- Log a Decision (Type: Kill/Park) if this supersedes an active bet.
```

## Worked Example

**Opportunity:** AI-powered weekly review tool for solo PMs.

| Dimension | Score | Reasoning |
|---|---|---|
| Market Opportunity | 3 | Solo PM / indie maker market growing (~200K worldwide, 20%/yr per Indie Hackers 2025 data). Pain is real (backlog drift, stalled products) but not urgent/expensive. |
| Competitive Position | 3 | Linear, Notion AI, and Height cover adjacent ground. Whitespace: portfolio-level (multi-product) rollup with AI-native triage. Moat is user workflow depth, not structural. |
| Founder Fit | 5 | Built PM OS plugin. 10+ years PM experience. Direct access to 50+ solo-PM peers via founder network. |
| Feasibility | 5 | Already have skill framework + Notion integration running. Weekly review skill exists; this is productizing it. MVP = 1 week. |
| Strategic Fit | 4 | Reuses the PM OS architecture and persona. Creates a shared distribution asset (early users overlap with plugin users). Doesn't conflict with current bets. |
| **Total** | **20/25** | |

**Verdict:** Explore.

**Next steps:**
1. Interview 5 solo PMs about their current weekly review ritual — what works, what they skip.
2. Ship a hosted version of `/weekly-review` behind a waitlist in 1 week. Track signup rate.
3. Log a Decision (Type: Go-to-Market) committing to the wedge: "weekly-review SaaS for solo PMs with 2+ products."

## Follow-ups

Contextual to the verdict:

- **Explore** + high Founder Fit: suggest `/design-experiment` to frame the first validation test.
- **Explore** + low Feasibility: suggest consulting the **systems-architect** agent on the tech cost ceiling.
- **Park**: `/log-decision` with Type: Park, noting trigger to revisit.
- **Kill**: `/log-decision` with Type: Kill, linking the evaluation as context.
- Any verdict: suggest updating the Notion opportunity backlog.
