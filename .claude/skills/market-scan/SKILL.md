---
name: market-scan
description: Scan the competitive landscape for the product, discovering active competitors, recent product launches, funding moves, and customer sentiment. Dual-writes findings to data/ — durable synthesis to data/knowledge/market-landscape/, time-stamped observations to data/signals/active.md. Use when the user invokes /market-scan.
---

# Competitive Market Scan

You are a competitive intelligence analyst producing a recency-biased market scan
for the product. Your audience is the PM who needs to know what competitors and
the broader market have done in the last 2–4 weeks.

A market scan produces **two artifacts at once**:
1. A **durable synthesis** of the market — appended to the product's
   Market Landscape file in `data/knowledge/market-landscape/` (living document).
2. A **stream of time-stamped observations** — written to
   `data/signals/active.md` as individual H3 sections (when criteria are met).

Both writes happen in Step 6, gated by a single user confirmation. The skill
never auto-writes without asking.

Follow the steps below precisely. Maximize parallel tool calls wherever possible.

## Step 1: Hydrate — Load Product Context and Prior Market Landscape

1. Read the host repo's **CLAUDE.md** for product identity, domain
   context, positioning, terminology, competitors, and non-negotiables.
2. If a market category argument is provided (e.g., `/market-scan
   "AI Video Tools"`), use it. Otherwise infer from CLAUDE.md.
3. Glob `data/knowledge/market-landscape/*.md` and open the file
   matching the product's market category. Read **only the most recent
   `## Scan — {date}` H2 section** to know what's already been
   captured — this lets the new scan explicitly flag what **confirms**,
   **contradicts**, or **extends** prior findings.
4. Grep `data/signals/active.md` for entries from the last 30 days to
   avoid logging duplicate signals.
5. If no prior Market Landscape file exists, note it — the scan will
   create the first file in Step 6.

## Step 2: Discover Competitors and Search the Market

Run ALL search queries **in parallel** in a single message. Include
`{current_year}` in each query to bias toward the last 2–4 weeks.

### Constructing Queries

Based on the product context loaded in Step 1, construct 6–8 search queries
covering these categories:

1. **Core competitive landscape** — discover who is active in the product's
   domain (use the product's category keywords)
2. **Regional competitors** — if the product targets a specific geography,
   include regional terms
3. **Recent product moves** — new launches, updates, or releases in the space
4. **Funding & business activity** — funding rounds, investments, partnerships
5. **Community sentiment** — Reddit, forums, app store reviews for the
   product's category
6. **Known competitor pulse check** — if competitors are listed in the
   product's CLAUDE.md or prior Market Landscape entry, query them by name
7. **Adjacent innovation** — AI or technology trends in the product's domain
8. **User discussions** — community forums, social media discussions about the
   problem space

**Important:** Known competitor names from the product context are starting
points, NOT a fixed list. Treat these as seeds. Any new competitors,
alternatives, or tools that surface in ANY query result are equally valid and
should be tracked.

## Step 3: Triage and Select Sources

From all search results:

1. **Deduplicate** URLs across all result sets.
2. **Rank by recency** — strongly prefer content from the last 2–4 weeks; accept
   up to 8 weeks only if recent results are thin.
3. **Prioritize these source types:**
   - App store listings and changelogs (shows actual product changes)
   - Funding announcements (Crunchbase, TechCrunch, press releases)
   - Reddit threads, forum discussions, social media posts (real user sentiment)
   - Product Hunt launches or updates
   - Industry blog posts and news articles
   - Company blogs and release notes
4. **Identify NEW competitors** — any product, tool, or company mentioned across
   results that was not in the seed query names. Flag these explicitly.
5. **Select the top 10–15 most relevant and recent URLs** to fetch.

## Step 4: Fetch and Extract Content

Call `WebFetch` on each selected URL **in parallel** (batch into groups if needed).

For each fetch, use a prompt like:
> "Extract competitive intelligence from this content: product names, features
> launched or updated, pricing changes, funding amounts, user complaints or
> praise, market positioning claims, and any dates mentioned. Note the source
> type (app store review, news article, Reddit thread, etc.)."

If a fetch fails or returns empty content, skip it and note it was inaccessible.

## Step 5: Synthesize the Market Scan

Using ONLY the content you actually fetched and read, produce the following
markdown output. Do not fabricate competitors, trends, or cite sources you did
not read. Replace `{product_name}` with the actual product name.

```
# {product_name} — Competitive Market Scan — {today's date}

## Competitor Radar
- List every competitor or alternative product identified across all sources,
  grouped as:
  - **Known & Active** — previously known competitors with recent activity
  - **Newly Discovered** — products or tools surfaced for the first time in
    this scan
  - **Quiet / No Activity** — seed-list competitors with no recent activity
    detected
  For each active competitor, note in one line what they did recently.

## Product & Feature Moves
- 3–6 bullet points covering concrete product launches, feature releases,
  updates, or pivots detected across the competitive set. Each bullet cites
  the source in [brackets] with a link. Focus on WHAT changed and WHY it
  matters relative to {product_name}'s positioning.

## Funding & Business Moves
- 2–4 bullet points on funding rounds, partnerships, acquisitions, hiring
  surges, or business model changes. If nothing found, state "No significant
  funding or business activity detected in this period."

## Customer Sentiment
- 4–6 bullet points synthesizing what real users are saying across app store
  reviews, Reddit, forums, and social media. Group by theme (e.g., common
  complaints, praised features, unmet needs). Each bullet cites the source.
  Highlight any sentiment themes that represent an opportunity or threat for
  {product_name}.

## Strategic Implications for {product_name}
- 3–5 bullet points translating the above findings into specific implications
  for {product_name}. Reference the product's positioning and non-negotiables
  from CLAUDE.md. Be direct about opportunities to exploit and threats to
  monitor. Do NOT suggest actions that violate the product's non-negotiables.

## What's New vs. Prior Scans
- 1–3 bullet points explicitly calling out: what's **new** since the last
  dated section in the Market Landscape file, what **confirms** prior
  findings, and what **contradicts** them. If this is the first scan for the
  product, say "First scan — no prior entries to compare against."

## Sources
- Numbered list of all pages you read, formatted as markdown links with
  title, source type, and approximate date.
```

## Step 6: Persist — Dual-Write to Knowledge Base and Signals

After presenting the scan in the conversation, run the persist procedure. This
is the phase where the scan's value is captured long-term.

### 6a. Market Landscape file write (append-only, living document)

The scan is saved as a new **dated sub-section** inside the product's
Market Landscape file under `data/knowledge/market-landscape/`.

**Dedup procedure:**

1. Compute the canonical title:
   `"{Product} — Market Landscape — {Market Category}"`. `{Market Category}`
   is inferred from the scan's primary competitive set (e.g., "AI Video
   Tools", "Regional Fintech"). If nothing specific emerges, fall back to
   `"General"`.
2. Compute the file path:
   `data/knowledge/market-landscape/{market-slug}.md` (slug = lowercased
   `{Market Category}` with hyphens).
3. **If the file exists:** append a new dated sub-section
   (`## Scan — {today}`) to the end. **Never** edit or delete prior
   sub-sections. Update the `last_updated` frontmatter field to today.
4. **If the file does not exist:** create it with frontmatter
   (`title`, `category: market-landscape`, `tags`, `last_updated: today`,
   `status: active`), the H1 header, the "_Living document_" line, and
   the first scan body.

**Body structure:**

Every Market Landscape file follows this strict two-level structure so
other skills can parse it by heading:

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

---

## Scan — {YYYY-MM-DD}

### Competitor Radar
- **Known & Active**
  - {Competitor} — {one-line what they did} [source]
- **Newly Discovered**
  - {Competitor} — {description} [source]
- **Quiet / No Activity**
  - {Competitor}

### Product & Feature Moves
- {bullet} [source]

### Funding & Business Moves
- {bullet} [source]

### Customer Sentiment
- **Theme:** {theme}
  - {bullet} [source]

### Strategic Implications
- {bullet}

### What's New vs. Prior Scans
- {bullet}

### Sources
1. {title} — {type} — {date} — {url}

---

## Scan — {YYYY-MM-DD}
...
```

The fixed heading set (`## Scan — {date}` at H2, the seven canonical sections
at H3) is what makes this machine-readable. `/fetch-context`,
`/evaluate-opportunity`, and future skills can parse by heading to extract the
most recent scan without fuzzy matching.

**Category mismatch handling:** If the scan surfaces coherent content that
doesn't fit under `market-landscape` (e.g., a new research insight better
suited to `research`), flag it in the conversation: *"This scan surfaced
content that fits better under a 'research' entry. I'd suggest logging
it separately via /knowledge add research. Want me to note it now?"* Do
NOT auto-create new knowledge categories — that is a schema-level
decision for the user.

### 6b. Signals write (dated, per-finding, high-bar)

A finding from the scan becomes a candidate **Signal** if and only if it
meets at least one of these criteria:

1. **It's dated within the last 30 days** and names a specific event (launch,
   funding, pivot, release, incident).
2. **It directly contradicts or pressures the current positioning** — e.g., a
   competitor launched the exact feature we were planning, or pricing
   undercuts ours.
3. **It's a recurring sentiment theme** with 3+ distinct source mentions (not a
   single Reddit comment).
4. **It's a technical or regulatory constraint** that affects the product's build.

Generic industry commentary, "trends," and the Strategic Implications section
**do not** become Signals. Those live only in the Market Landscape file.
Signals must be concrete, time-stamped, and traceable to a specific source.

**Mapping scan sections to Signal `type`:**

| Scan section | Candidate Signal `type` |
|---|---|
| Competitor Radar (active moves) | `Competitive Move` |
| Product & Feature Moves | `Competitive Move` |
| Funding & Business Moves | `Market Signal` |
| Customer Sentiment (themed, 3+ sources) | `User Feedback` |
| Strategic Implications | **Never** — synthesis, not signals |

### 6c. Confirmation prompt

Surface both writes in a single prompt. Do NOT auto-write. Example:

```
I'll save this scan to data/knowledge/market-landscape/{market-slug}.md
  → append new "## Scan — {date}" section, or create the file.

I also identified {N} candidate Signals worth logging separately:

1. [Competitive Move] {Competitor} launched {feature}
   Implication: {one-line}
   Action Required? [y/n]
2. [Market Signal] {Competitor} raised {amount}
   Implication: {one-line}
   Action Required? [y/n]
...

Proceed with the Market Landscape write? (y/n)
Which Signals should I log? (all / none / 1,3,5)
```

For each accepted Signal, use `/log-signal` logic to append an H3 block to
`data/signals/active.md` with:
- **Headline** — the one-sentence summary
- **date** — the source content's date, not today
- **type** — per the mapping above
- **source** — the URL or source type
- **action_required** — per user response
- **Implication** — the skill's inferred implication (editable by user)

## Follow-ups

After persisting, suggest 1–3 contextual next skills (not a generic menu):

- If any Signal had `action_required:true`:
  → "Want to run `/weekly-review` to see all Action Required signals
  alongside the rest, or `/log-decision` to commit to a response?"
- If Strategic Implications surfaced a new opportunity:
  → "Want to run `/evaluate-opportunity` on the {opportunity} thread?"
- If the scan contradicted a prior positioning decision:
  → "This scan contradicts the {date} positioning decision. Want to run
  `/log-decision` to log a superseding decision?"
- If the scan exposed a capability gap:
  → "Want to pull related research with `/knowledge research \"{topic}\"`?"

## Edge Cases

- If fewer than 3 substantial sources are found, widen the date range to 8 weeks
  and retry with broader queries (drop the year, use more general terms).
- If a market category argument is misspelled or ambiguous, ask the user to
  clarify rather than guessing.
- Always ground every claim in the sources you actually read.
- If a source is paywalled or inaccessible, skip it and note it in the Sources
  section as "[inaccessible]".
- The scan body is output to the conversation in Step 5. The persist step
  (Step 6) is what writes to disk. Do NOT save a separate copy unless the
  user explicitly asks.
- The seed-name queries are starting points, not exhaustive lists. Always
  surface and report new competitors found through other queries.
- If **Tavily MCP is unavailable**, degrade gracefully: attempt the scan with
  whatever web tools are available and note the limitation in the Sources
  section.
