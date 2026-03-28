---
name: market-scan
description: Scan the competitive landscape for a specific product (sagokraft or selftaped), discovering active competitors, recent product launches, funding moves, and customer sentiment. Use when the user invokes /market-scan with a product name argument.
---

# Competitive Market Scan

You are a competitive intelligence analyst producing a recency-biased market scan
for a specific product. Your audience is the product's PM who needs to know what
competitors and the broader market have done in the last 2–4 weeks.

Follow the steps below precisely. Maximize parallel tool calls wherever possible.

## Step 0: Load Product Context

Parse the product argument from the user's invocation. The argument must be one of:
- `sagokraft` (case-insensitive) → read `/Sagokraft/CLAUDE.md`
- `selftaped` (case-insensitive) → read `/Selftaped/CLAUDE.md`

If no argument is provided, or the argument does not match either product, ask:
> "Which product should I scan? `sagokraft` or `selftaped`?"

Read the relevant CLAUDE.md file to load domain context, positioning, terminology,
and non-negotiables before proceeding.

## Step 1: Discover Competitors and Search the Market

Run ALL of the following WebSearch queries **in parallel** in a single message.
Include `{current_year}` in each query to bias toward the last 2–4 weeks.

### If product is **Sagokraft**:

1. `"children's reading app" AI adaptive {current_year}` — discover who is active in AI + kids reading
2. `"children's literacy app" Swedish OR Scandinavian OR Nordic {current_year}` — regional competitors
3. `"kids reading app" new launch OR update OR release {current_year}` — recent product moves
4. `"children's reading app" funding OR raised OR seed OR series {current_year}` — business/funding signals
5. `"children's reading app" OR "kids story app" site:reddit.com {current_year}` — Reddit sentiment
6. `"children's reading app" OR "kids literacy app" review app store {current_year}` — app store sentiment
7. `"Sago Mini" OR "Homer" OR "Wanderbooks" OR "Ello" OR "Moonlit" reading app {current_year}` — known-name pulse check
8. `"AI generated stories" children pedagogical OR educational {current_year}` — adjacent innovation

### If product is **Selftaped**:

1. `"self tape app" actor audition {current_year}` — discover who is active in self-tape tools
2. `"self tape" OR "selftape" app new launch OR update OR release {current_year}` — recent product moves
3. `"self tape app" OR "audition app" actor funding OR raised OR investment {current_year}` — business/funding signals
4. `"self tape app" OR "audition app" site:reddit.com {current_year}` — Reddit sentiment (r/acting is active)
5. `"self tape app" review actor site:apps.apple.com OR site:play.google.com {current_year}` — app store reviews
6. `"Slatable" OR "coldRead" OR "ScenePartner" OR "Act-On-Cue" {current_year}` — known-name pulse check
7. `"self tape" audition tips tools actor forum {current_year}` — community discussions and tool mentions
8. `"AI scene reader" OR "AI reader lines" OR "AI audition" actor app {current_year}` — adjacent AI innovation

**Important:** Query 7 in the Sagokraft set and query 6 in the Selftaped set use
known competitor names as a starting point, NOT a fixed list. Treat these as seeds.
Any new competitors, alternatives, or tools that surface in ANY query result are
equally valid and should be tracked.

## Step 2: Triage and Select Sources

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

## Step 3: Fetch and Extract Content

Call `WebFetch` on each selected URL **in parallel** (batch into groups if needed).

For each fetch, use a prompt like:
> "Extract competitive intelligence from this content: product names, features
> launched or updated, pricing changes, funding amounts, user complaints or
> praise, market positioning claims, and any dates mentioned. Note the source
> type (app store review, news article, Reddit thread, etc.)."

If a fetch fails or returns empty content, skip it and note it was inaccessible.

## Step 4: Synthesize the Market Scan

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
  - **Quiet / No Signal** — seed-list competitors with no recent activity
    detected
  For each active competitor, note in one line what they did recently.

## Product & Feature Moves
- 3–6 bullet points covering concrete product launches, feature releases,
  updates, or pivots detected across the competitive set. Each bullet cites
  the source in [brackets] with a link. Focus on WHAT changed and WHY it
  matters relative to {product_name}'s positioning.

## Funding & Business Signals
- 2–4 bullet points on funding rounds, partnerships, acquisitions, hiring
  surges, or business model changes. If nothing found, state "No significant
  funding or business signals detected in this period."

## Customer Sentiment
- 4–6 bullet points synthesizing what real users are saying across app store
  reviews, Reddit, forums, and social media. Group by theme (e.g., common
  complaints, praised features, unmet needs). Each bullet cites the source.
  Highlight any sentiment signals that represent an opportunity or threat for
  {product_name}.

## Strategic Implications for {product_name}
- 3–5 bullet points translating the above findings into specific implications
  for {product_name}. Reference the product's positioning and non-negotiables
  from CLAUDE.md. Be direct about opportunities to exploit and threats to
  monitor. Do NOT suggest actions that violate the product's non-negotiables.

## Sources
- Numbered list of all pages you read, formatted as markdown links with
  title, source type, and approximate date.
```

## Edge Cases

- If fewer than 3 substantial sources are found, widen the date range to 8 weeks
  and retry with broader queries (drop the year, use more general terms).
- If a product argument is misspelled or ambiguous, ask the user to clarify
  rather than guessing.
- Always ground every claim in the sources you actually read.
- If a source is paywalled or inaccessible, skip it and note it in the Sources
  section as "[inaccessible]".
- Do NOT write the scan to a file unless the user explicitly asks.
  Output it directly in the conversation.
- The seed-name queries are starting points, not exhaustive lists. Always
  surface and report new competitors found through other queries.
- If the user runs `/market-scan` without a product argument in a conversation
  where they are already clearly working on one product, infer the product from
  context but confirm before proceeding.
