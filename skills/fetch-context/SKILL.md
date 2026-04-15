---
description: Fetch live product context from Notion. Foundation skill used by other PM skills to self-hydrate with decisions, personas, backlog, recent Signals, and Market Landscape entries.
---

# Fetch Product Context

This is a utility skill that fetches live context from Notion for the current product. Other skills call on this pattern before doing their work.

**What this skill reads from:**
- **Decisions** database — commitments the PM has made
- **Signals** database — recent time-stamped observations
- **Knowledge Base** — personas, reference, research, Market Landscape
- **Task Management** — active backlog and in-progress work

See the **DB Routing Rubric** in `.claude/context/notion-schemas.md` for what each database holds.

## How to Identify the Current Product

1. Read the repo's CLAUDE.md file
2. Look for the "Repo Identity" section
3. Extract the product name
4. If no Repo Identity section exists, ask the user which product they're working on

## What to Fetch from Notion

All products share the same Notion databases (see `.claude/context/notion-schemas.md`
for schema). Always filter by the **Product** property matching the
identified product.

Use the Notion MCP integration to search for and retrieve:

### Decisions (always fetch)
- Search Notion for pages related to "decisions" for the identified product
- Filter to active/recent decisions (last 90 days preferred)
- Summarize: what was decided, when, and any constraints imposed

### Personas (fetch when skill needs user context)
- Search Notion for the target persona associated with this product
- Extract: who they are, key pain points, jobs to be done

### Backlog priorities (fetch when skill needs scope context)
- Search Notion for the product backlog
- Focus on top 10 items by priority
- Note current phase (Explore, Validate, Build, Scale)

### Recent Signals (fetch when skill needs market or user-feedback context)
- Query the **Signals** database, filtered by `Product = {product}` and
  `Date` within the last 30 days (extend to 60 days if thin).
- Group by `Type`: User Feedback, Technical Constraint, Market Signal,
  Competitive Move, Internal Learning.
- Highlight any with `Action Required = true`.
- Include any opportunity scoring or evaluation data from the Decisions
  database (type = `Scope` or `Go-to-Market`).

### Market Landscape (fetch when skill needs competitive context)
- Query the **Knowledge Base** for entries with
  `Category = Market Landscape AND Product contains {product}`.
- Surface the most recent `## Scan —` sub-section from the matching entry.
- If the latest scan is older than 30 days, note it and suggest running
  `/market-scan` to refresh.

## Caching Within a Session

If context for this product has already been fetched in this conversation, reuse it rather than re-querying Notion. Only re-fetch if the user explicitly asks for fresh context or if a different product is being discussed.

## Output

Present a brief context summary to the user:
- Product: [name]
- Key decisions: [2-3 bullet summary]
- Persona: [one-line summary]
- Current focus: [phase + top priorities]

This skill can be invoked directly for a quick context briefing, or used as a foundation step by other skills.
