---
description: Evaluate a startup or product opportunity against strategic criteria. Fetches existing opportunity backlog and competitive landscape from Notion.
---

# Evaluate Opportunity

## Before Starting — Self-Hydration

1. Identify whether this is for an existing product or a new exploration
2. Use Notion MCP to search for and retrieve:
   - The current opportunity backlog (all products/bets)
   - Any prior evaluations or scoring for similar opportunities
   - Competitive analysis if available
   - Strategic decisions about market focus or resource allocation
3. Briefly summarize what's already in the portfolio before evaluating the new opportunity

## Evaluation Framework

Score the opportunity on these dimensions (1-5 scale each):

### Market Opportunity
- Market size estimate (TAM/SAM/SOM, even rough)
- Growth trajectory of the market
- Urgency of the problem for target users

### Competitive Position
- Number and strength of existing solutions
- Whitespace available for differentiation
- Regulatory or technical moat potential

### Founder Fit
- Alignment with existing skills and domain knowledge
- Ability to reach early customers directly
- Passion and sustained interest level

### Feasibility
- Can an MVP be built with current tools (Lovable, Supabase)?
- Time to first testable version (days, not months)
- Technical complexity relative to capabilities

### Strategic Fit
- How does this relate to existing products (Sagokraft, Selftaped)?
- Does it create synergies or just spread focus?
- Does it fit the Swedish market focus?

## Output

Provide:
1. A scored summary table (dimension, score 1-5, reasoning)
2. Overall recommendation: **Explore** (worth deeper investigation), **Park** (interesting but not now), or **Kill** (doesn't pass the bar)
3. If Explore: suggest 2-3 concrete next steps for validation
4. If Park: note what would need to change to revisit
5. Suggest the user update their Notion opportunity backlog with this evaluation

After completing, if the opportunity scores well, suggest consulting the **startup-advisor** agent for deeper strategic analysis, or running `/write-prd` to start defining the product.
