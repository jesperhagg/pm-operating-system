---
description: Log a product decision to Notion and local memory. Captures the decision with structured metadata (product, type, status, context, impact) so it can be referenced by future skills.
---

# Log Decision

## Before Starting — Self-Hydration

1. Identify the current product (read CLAUDE.md for Repo Identity, or ask the user)
2. If the decision was just discussed in this conversation, extract it from context
3. If not, ask the user:
   - What was decided?
   - Which product does this apply to?
4. Use Notion MCP to fetch recent decisions for this product (last 30 days)
   to check for duplicates or related decisions

## Decision Structure

Capture the decision with these fields:

### Required Fields
- **Summary** — one-sentence description of what was decided
- **Product** — the product this decision applies to (multi-select in Notion)
- **Type** — one of: Architecture, Scope, Positioning, Pricing, Go-to-Market,
  Technical, Design, Partnership, Kill/Park
- **Status** — one of: Active, Superseded, Experimental
- **Date** — today's date

### Context Fields
- **Context** — why this decision was made (2-3 sentences). What alternatives
  were considered? What evidence or reasoning drove the choice?
- **Impact** — what this decision changes or constrains going forward.
  Reference specific features, flows, or priorities affected.
- **Linked Decision** — if this supersedes or builds on a prior decision,
  reference it

## Writing to Notion

Use Notion MCP to create a new page in the Decisions database:
- Set the Product multi-select to the identified product
- Set Type, Status, Date, Summary, Context, and Impact fields
- If a linked decision exists, add the reference

If Notion MCP is not available or the write fails:
- Log the decision to `.claude/memory/shared.md` under a Decisions section as
  a local fallback
- Format: `- [{date}] **{product}** — **{type}**: {summary} — {context} (Impact: {impact})`

## Output

Confirm what was logged:

```
## Decision Logged

**Product:** {product}
**Type:** {type}
**Summary:** {summary}
**Status:** {status}
**Written to:** Notion Decisions database [or local memory fallback]
```

## After Completing

Suggest the user might want to:
- Run `/evaluate-opportunity` if this decision opens or closes a product bet
- Run `/write-prd` if this decision defines scope for a new feature
- Run `/break-down` if an existing PRD needs updating based on this decision
