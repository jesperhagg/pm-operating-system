---
description: Write a Product Requirements Document using proven PM frameworks. Automatically fetches live product context from Notion before starting.
---

# Write PRD

## Before Starting — Self-Hydration

Before writing anything, gather context:

1. Identify the current product (read CLAUDE.md for Repo Identity, or ask the user)
2. Use Notion MCP to search for and retrieve:
   - Active decisions tagged to this product (last 90 days)
   - The target persona for this product
   - Current backlog priorities (top 10)
   - Any active constraints (technical, regulatory, market)
3. Summarize the context briefly to the user before proceeding

## PRD Framework

Write the PRD using this structure:

### 1. Problem Statement
- What specific user problem are we solving?
- Reference the target persona and their pain points (from Notion)
- Evidence: what signals or research support this problem?

### 2. Hypothesis
- "We believe that [solution] will [outcome] for [persona] because [evidence]"
- State the riskiest assumption

### 3. Proposed Solution
- High-level description of what we're building
- Key user flows (numbered, not exhaustive)
- In scope vs. explicitly out of scope
- Reference any prior decisions from Notion that constrain the solution

### 4. Success Metrics
- Primary metric (North Star for this feature/product)
- 2-3 secondary metrics
- How each will be measured
- What "good enough" looks like for v1

### 5. Technical Context
- Tech stack (from CLAUDE.md)
- Known constraints or dependencies
- Integration points

### 6. Open Questions & Risks
- Unresolved questions that need answers before or during build
- Key risks with mitigation ideas
- Suggested discovery activities if assumptions are untested

## Output

Save the PRD as a markdown file: docs/prd-[feature-name].md

After completing, suggest the user might want to run:
- /break-down to decompose this into kanban-ready work items
- /evaluate-opportunity if this is a new product bet
