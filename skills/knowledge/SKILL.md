---
description: Fetch, store, and review structured knowledge in data/knowledge/. Manages four knowledge categories — People (stakeholders), Reference (company/product/team docs), Research (domain insights), and Market Landscape (read-only here, written by /market-scan).
---

# Knowledge Management

This skill manages persistent knowledge in `data/knowledge/` in the
consumer repo. Knowledge is organized into four category subfolders:

- **people** (`data/knowledge/people/`) — stakeholder profiles,
  communication styles, working preferences
- **reference** (`data/knowledge/reference/`) — company info, product
  overviews, team structure, OKR history
- **research** (`data/knowledge/research/`) — domain research, literature
  reviews, one-shot insights
- **market-landscape** (`data/knowledge/market-landscape/`) — living
  documents of the competitive landscape. Written exclusively by
  `/market-scan` as append-only dated sections. Read by this skill but
  not edited directly.

**Scope boundary:** Knowledge stores **durable, synthesized
understanding**. Time-stamped observations (competitor launched X
yesterday, user said Y, we discovered Z) belong in Signals — use
`/log-signal` for those. Customer personas have their own location
(`data/personas/`); use `/define-persona`. See the DB Routing Rubric
in `.claude/context/data-schemas.md`.

## File Layout

Each entry is one file per topic. Frontmatter:

```yaml
---
title: Jane Doe — CEO at Acme
category: people             # people | reference | research | market-landscape
tags: [stakeholder, fund]
last_updated: YYYY-MM-DD
status: active               # active | archived
---
```

No `index.md` per subfolder — glob + frontmatter is the discovery
mechanism.

## Modes

### 1. Fetch (default)

**Triggers:** `/knowledge people "name"`, `/knowledge research "topic"`,
`/knowledge reference`, or just `/knowledge "search term"`

**Steps:**

1. Identify the category from the command (people, reference, research,
   market-landscape). If no category specified, search across all four.
2. Glob `data/knowledge/{category}/*.md` (or all categories).
3. Filter by frontmatter: `status: active`, plus any tag or title match
   from the search term.
4. For multiple results: show a list with file paths and one-line
   summaries (read just the frontmatter title + first body line).
5. For a single result: read the full file and show the body.

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
   - **Category:** people, reference, or research (Market Landscape is
     reserved for `/market-scan` — do not create these manually).
   - **Title:** name or topic.
   - **Tags:** optional freeform tags.
2. Compute the slug from the title and the file path:
   `data/knowledge/{category}/{slug}.md`. If the file exists, ask
   whether to overwrite or pick a new slug.
3. Based on the category, prompt for structured content:
   - **people** — use the stakeholder profile template (Quick Facts,
     Communication Style, How to Work With Them, What They Care About,
     Personal Notes)
   - **reference** — freeform content covering the topic
   - **research** — structured with Key Findings, Implications, Sources,
     Date of Research
4. Write the file with frontmatter (`title`, `category`, `tags`,
   `last_updated: today`, `status: active`) followed by the body.
5. Confirm creation with the file path and a one-line summary.

**Redirects:** If the user tries to store content that is clearly a
time-stamped observation (dated event, recent finding, competitor move),
redirect them: *"That sounds like a Signal, not a Knowledge entry.
Want to run `/log-signal` instead?"* If it's a customer persona,
redirect to `/define-persona`.

### 3. Review

**Triggers:** `/knowledge review`

**Steps:**

1. Glob `data/knowledge/**/*.md`. Read frontmatter only (not bodies)
   for each file.
2. Analyze for:
   - **Staleness** (category-dependent):
     - people / reference / research: `last_updated` older than 90 days
     - market-landscape: `last_updated` older than 30 days (market moves
       faster)
   - **Gaps:** Categories with few or no entries (e.g., "0 People entries
     on file")
   - **Volume:** Flag if any category exceeds 30 entries (suggest pruning)
   - **Archived noise:** Files with `status: archived` older than 180
     days that could be deleted instead of kept.
3. Present a review summary:

```
## Knowledge Review — {date}

**Total entries:** {count} (people: {n}, reference: {n}, research: {n}, market-landscape: {n})

### Stale Entries
- {file path} — Category: {cat}, Last updated: {date}, Threshold: {30d or 90d}

### Gaps
- {category} has no entries

### Suggestions
- Update: {list of stale entries worth refreshing}
- Archive: {list of entries that may no longer be relevant}
- Add: {suggested new entries based on gaps}
- Re-scan: {market-landscape entries past the 30-day threshold — suggest /market-scan}
```

4. Ask the user if they want to update, archive, or add any entries.

## People Profile Template

When storing a new People entry, use this template as the body
structure (after the YAML frontmatter):

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
reads them but does not edit them. Expect this machine-readable
structure so heading-based parsing works:

```markdown
---
title: {Product} — Market Landscape — {Market Category}
category: market-landscape
tags: [...]
last_updated: YYYY-MM-DD
status: active
---

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
**most recent `## Scan —`** sub-section unless the user asks for
history.

## Suggested Follow-ups

After fetching People knowledge, suggest: "Want me to prep for a meeting
with {name}?"

After storing Research knowledge, suggest: "Want me to check how this
connects to your current backlog? Run `/fetch-context`."

After fetching a Market Landscape entry older than 30 days, suggest:
"This scan is {N} days old. Want to run `/market-scan` to refresh it?"

After a review, suggest: "Want me to help fill the gaps? I can draft
entries for missing categories."
