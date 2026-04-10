---
description: Fetch, store, and review structured knowledge in Notion. Manages three knowledge categories — People (stakeholder profiles), Reference (company/product/team docs), and Research (domain insights, trends, literature).
---

# Knowledge Management

This skill manages persistent knowledge in a Notion "Knowledge Base" database.
Knowledge is organized into four categories:

- **People** — stakeholder profiles, communication styles, working preferences
- **Reference** — company info, product overviews, team structure, OKR history
- **Research** — domain research, literature reviews, one-shot insights
- **Market Landscape** — living documents of the competitive landscape for a
  product's market. Written exclusively by `/market-scan` as append-only
  dated sections. Read by this skill but not typically edited directly.

**Scope boundary:** Knowledge Base stores **durable, synthesized
understanding**. Time-stamped observations (competitor launched X yesterday,
user said Y, we discovered Z) belong in the **Signals** database — use
`/log-signal` for those. See the DB Routing Rubric in CLAUDE.md.

## Expected Notion Database: Knowledge Base

This skill queries the shared Knowledge Base database (see **Notion
Database Schema** in CLAUDE.md for full property definitions). This is a
single database shared across all products — filter by the **Product**
property to scope results to the current product.

The page body contains the actual knowledge content in rich text. The
`Last Edited Time` property (built-in) is used for staleness detection.

## How to Identify the Current Product

1. Read the repo's CLAUDE.md file
2. Look for the "Repo Identity" section or product name
3. Use as default filter when querying the Knowledge Base
4. If no product identity exists, ask the user

## Modes

### 1. Fetch (default)

**Triggers:** `/knowledge people "name"`, `/knowledge research "topic"`,
`/knowledge reference`, or just `/knowledge "search term"`

**Steps:**

1. Identify the category from the command (people, reference, research).
   If no category specified, search across all categories.
2. Use Notion MCP to search the Knowledge Base database, filtering by:
   - Category (if specified)
   - Search term (title or content match)
   - Product (current product context, if known)
3. Return a concise summary of matching entries. For multiple results,
   show a list with titles and one-line summaries. For a single result,
   show the full content.

**For People entries, format the output as:**

```
## {Name} — {Role}

**Quick Facts:** {tenure, background, location}

**Communication Style:**
- Prefers: {preferences}
- Dislikes: {anti-patterns}
- Response times: {by channel}

**How to Work With Them:**
- {decision-making style}
- {meeting preferences}
- {update format preferences}

**What They Care About:** {priorities, metrics, pet topics}

**Personal Notes:** {icebreakers, interests, relationship context}
```

### 2. Store

**Triggers:** `/knowledge add`, `/knowledge store`

**Steps:**

1. Ask the user for:
   - **Category:** People, Reference, or Research (Market Landscape is
     reserved for `/market-scan` — do not create these manually)
   - **Title:** Name or topic
   - **Product:** Which product this applies to (or "All")
   - **Tags:** Optional freeform tags
2. Based on the category, prompt for structured content:
   - **People:** Use the stakeholder profile template (Quick Facts,
     Communication Style, How to Work With Them, What They Care About,
     Personal Notes)
   - **Reference:** Freeform content covering the topic
   - **Research:** Structured with Key Findings, Implications, Sources,
     Date of Research
3. Create a new page in the Notion Knowledge Base via MCP with the
   collected properties and content.
4. Confirm creation and show a summary.

**Redirects:** If the user tries to store content that is clearly a
time-stamped observation (dated event, recent finding, competitor move),
redirect them: *"That sounds like a Signal, not a Knowledge Base entry.
Want to run `/log-signal` instead?"*

### 3. Review

**Triggers:** `/knowledge review`

**Steps:**

1. Fetch all entries from the Notion Knowledge Base.
2. Analyze for:
   - **Staleness** (category-dependent):
     - People / Reference / Research: not updated in 90+ days
     - Market Landscape: not updated in 30+ days (market moves faster)
   - **Gaps:** Categories with few or no entries for a given product
     (e.g., "You have 0 People entries for Product X")
   - **Volume:** Flag if any category exceeds 30 entries (suggest pruning)
   - **Relevance:** Entries tagged to products that no longer appear in
     the portfolio
3. Present a review summary:

```
## Knowledge Base Review — {date}

**Total entries:** {count} (People: {n}, Reference: {n}, Research: {n}, Market Landscape: {n})

### Stale Entries
- {title} — Category: {cat}, Last updated: {date}, Threshold: {30d or 90d}

### Gaps
- {product} has no {category} entries

### Suggestions
- Update: {list of stale entries worth refreshing}
- Archive: {list of entries that may no longer be relevant}
- Add: {suggested new entries based on gaps}
- Re-scan: {Market Landscape entries past the 30-day threshold — suggest running /market-scan}
```

4. Ask the user if they want to update, archive, or add any entries.

## Caching

If Knowledge Base entries have already been fetched in this conversation,
reuse them rather than re-querying Notion. Re-fetch if the user explicitly
asks for fresh data or if a store operation was just performed.

## People Profile Template

When storing a new People entry, use this template as the page body structure:

```markdown
# {Name} — {Role}

## Quick Facts
- **Role:** {title}
- **Reports to:** {manager}
- **Tenure:** {time at company}
- **Background:** {previous roles, education}
- **Location:** {office/remote, timezone}

## Communication Style

**Prefers:**
- {preference 1}
- {preference 2}

**Dislikes:**
- {anti-pattern 1}
- {anti-pattern 2}

**Response times:**
- {channel}: {typical response time}

## How to Work With Them

### In Meetings
- {meeting preferences}

### Getting Decisions
- {decision-making style and process}

### Giving Updates
- {preferred format and cadence}

## What They Care About

**Top priorities:**
1. {priority}

**Key metrics they track:**
- {metric}

**Pet topics:**
- {topic they're passionate about}

## Personal Notes
- {icebreakers, interests, family, relationship context}
```

## Market Landscape Entry Structure

Market Landscape entries are maintained by `/market-scan` — this skill
reads them but does not typically edit them. When fetched, expect the
following machine-readable structure so heading-based parsing works:

```markdown
# {Product} — Market Landscape — {Market Category}

_Living document. New scans append dated sections below._

## Scan — {YYYY-MM-DD}

### Competitor Radar
### Product & Feature Moves
### Funding & Business Moves
### Customer Sentiment
### Strategic Implications
### What's New vs. Prior Scans
### Sources

## Scan — {YYYY-MM-DD}
...
```

When surfacing a Market Landscape entry in Fetch mode, show only the
**most recent `## Scan —`** sub-section unless the user asks for history.

## Suggested Follow-ups

After fetching People knowledge, suggest: "Want me to prep for a meeting
with {name}?"

After storing Research knowledge, suggest: "Want me to check how this
connects to your current backlog? Run `/fetch-context`."

After fetching a Market Landscape entry older than 30 days, suggest:
"This scan is {N} days old. Want to run `/market-scan` to refresh it?"

After a review, suggest: "Want me to help fill the gaps? I can draft
entries for missing categories."
