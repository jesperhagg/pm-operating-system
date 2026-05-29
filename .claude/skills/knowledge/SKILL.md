---
description: Fetch, store, and review structured knowledge in context/. Manages people (stakeholders), research (domain insights), and strategy/reference. Market landscape is read-only here, written by /market-scan.
---

# Knowledge Management

This skill manages persistent knowledge in the consumer repo's `context/`
layer. Knowledge is organized into thematic files:

- **people** (`context/ops/people.md`) — stakeholder profiles,
  communication styles, working preferences
- **research** (`context/users/research.md`) — domain research, literature
  reviews, one-shot insights
- **strategy/reference** (`context/product/strategy.md`) — company info,
  product overviews, team structure, OKR history, positioning
- **market-landscape** (`context/market/landscape.md`) — living competitive
  document. Written exclusively by `/market-scan` as append-only dated
  sections. Read by this skill but not edited directly.

**Scope boundary:** Knowledge stores **durable, synthesized understanding**.
Time-stamped observations belong in Signals — use `/log-signal`. Customer
personas use `/define-persona`. See the Context Routing Rubric in
`.claude/context/context-schemas.md`.

## Modes

### 1. Fetch (default)

**Triggers:** `/knowledge people "name"`, `/knowledge research "topic"`,
`/knowledge strategy`, or just `/knowledge "search term"`

**Steps:**

1. Identify the category from the command. If no category, search all files.
2. Open the relevant context file.
3. Grep for H2 headings matching the search term. Show matching section
   titles and one-line summaries (metadata comment + first body line).
4. For a single match: read the full H2 section and show the body.
5. For multiple matches: show a list for the user to pick from.

**For People entries, format the output as:**

```
## {Name} — {Role}

**Quick Facts:** {role, company, background}

**Communication Style:**
- Prefers: {preferences}
- Dislikes: {anti-patterns}

**How to Work With Them:**
- {decision-making style}
- {meeting/update preferences}

**What They Care About:** {priorities, metrics, pet topics}

**Personal Notes:** {icebreakers, relationship context}
```

### 2. Store

**Triggers:** `/knowledge add`, `/knowledge store`

**Steps:**

1. Ask the user for:
   - **Category:** people, research, or strategy (Market Landscape is
     reserved for `/market-scan`).
   - **Title:** name or topic.
2. Determine the target file from the category:
   - people → `context/ops/people.md`
   - research → `context/users/research.md`
   - strategy/reference → `context/product/strategy.md`
3. Prompt for structured content based on category:
   - **people** — stakeholder profile template (Quick Facts, Communication
     Style, How to Work With Them, What They Care About, Personal Notes)
   - **research** — Key Findings, Implications, Sources, Date of Research
   - **strategy** — freeform content for the topic
4. Append a new H2 block to the target file with a metadata comment:
   `<!-- last_updated:YYYY-MM-DD source:"{source}" session:pending -->`
5. Confirm with the file path and a one-line summary.

**H2 block format:**

```markdown
## {Title} {#slug}
<!-- last_updated:YYYY-MM-DD source:"{source}" session:pending -->

{body content}

---
```

The `session:pending` annotation marks this as session-written, awaiting
reconciliation by `/context-sync`.

**Redirects:** If the content is clearly a time-stamped observation,
redirect: *"That sounds like a Signal — run `/log-signal` instead."*
If it's a customer persona, redirect to `/define-persona`.

### 3. Review

**Triggers:** `/knowledge review`

**Steps:**

1. Read frontmatter H2 metadata comments from all four target files.
2. Analyze for:
   - **Staleness** — entries with `last_updated` older than:
     - people / research / strategy: 90 days
     - market-landscape: 30 days
   - **Gaps:** categories with no entries
   - **Archived noise:** sections with `status:archived` older than 180 days
3. Present:

```
## Knowledge Review — {date}

### Stale Entries
- {file} ## {heading} — last updated: {date}

### Gaps
- {category} has no entries

### Suggestions
- Update: {stale entries worth refreshing}
- Archive: {entries that may no longer be relevant}
- Add: {suggested new entries based on gaps}
- Re-scan: market landscape past 30 days — suggest /market-scan
```

4. Ask if they want to update, archive, or add any entries.

## People Profile Template

When storing a new People entry:

```markdown
## {Name} — {Role} {#slug}
<!-- last_updated:YYYY-MM-DD source:"{context}" session:pending -->

### Quick Facts
- **Role:** {title}
- **Reports to:** {manager}
- **Tenure:** {time}
- **Background:** {previous roles}
- **Location:** {timezone}

### Communication Style
- Prefers: {preferences}
- Dislikes: {anti-patterns}
- Response times: {channel: typical response time}

### How to Work With Them
- In meetings: {preferences}
- Getting decisions: {style}
- Giving updates: {format and cadence}

### What They Care About
- Top priorities: {list}
- Key metrics: {list}
- Pet topics: {list}

### Personal Notes
- {icebreakers, interests, relationship context}

---
```

## Market Landscape Entry Structure

Market Landscape entries are maintained by `/market-scan` — this skill
reads them but does not edit them. When surfacing a landscape entry in
Fetch mode, show only the **most recent `## Scan —`** section unless the
user asks for history. If the latest scan is older than 30 days, suggest
running `/market-scan`.

## Follow-ups

After fetching People knowledge:
→ "Want me to prep for a meeting with {name}?"

After storing Research knowledge:
→ "Want to check how this connects to your current backlog? Run `/fetch-context`."

After fetching a Market Landscape entry older than 30 days:
→ "This scan is {N} days old. Want to run `/market-scan` to refresh it?"

After a review:
→ "Want me to help fill the gaps?"
