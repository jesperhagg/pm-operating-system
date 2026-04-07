---
name: market-scan
description: Scan the competitive landscape for a product, discovering active competitors, recent product launches, funding moves, and customer sentiment. Use when the user invokes /market-scan with an optional product name argument.
---

# Competitive Market Scan

You are a competitive intelligence analyst producing a recency-biased market scan
for a specific product. Your audience is the product's PM who needs to know what
competitors and the broader market have done in the last 2–4 weeks.

Follow the steps below precisely. Maximize parallel tool calls wherever possible.

## Step 0: Load Product Context and Memory

1. If a product name argument is provided, use it. Otherwise, read the **host
   repo's `CLAUDE.md`** for product identity.
2. If the product still cannot be identified, ask:
   > "Which product should I scan?"
3. Read the host repo's `CLAUDE.md` for domain context, positioning,
   terminology, competitors, and non-negotiables.
4. Use **Notion MCP** to fetch prior competitive insights and strategic signals
   for this product. Use these to contextualize new findings — note which
   findings confirm, contradict, or extend prior entries.

## Step 1: Discover Competitors and Search the Market

Run ALL search queries **in parallel** in a single message. Include
`{current_year}` in each query to bias toward the last 2–4 weeks.

### Constructing Queries

Based on the product context loaded in Step 0, construct 6–8 search queries
covering these categories:

1. **Core competitive landscape** — discover who is active in the product's
   domain (use the product's category keywords)
2. **Regional competitors** — if the product targets a specific geography,
   include regional terms
3. **Recent product moves** — new launches, updates, or releases in the space
4. **Funding & business signals** — funding rounds, investments, partnerships
5. **Community sentiment** — Reddit, forums, app store reviews for the
   product's category
6. **Known competitor pulse check** — if competitors are listed in the
   product's CLAUDE.md or Notion context, query them by name
7. **Adjacent innovation** — AI or technology trends in the product's domain
8. **User discussions** — community forums, social media discussions about the
   problem space

**Important:** Known competitor names from the product context are starting
points, NOT a fixed list. Treat these as seeds. Any new competitors,
alternatives, or tools that surface in ANY query result are equally valid and
should be tracked.

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
- **Memory:** After presenting the scan, ask the user: "Would you like me to
  save any of these findings to Notion?" If yes, use Notion MCP to log selected
  findings as insights for the product.
- The seed-name queries are starting points, not exhaustive lists. Always
  surface and report new competitors found through other queries.
- If the user runs `/market-scan` without a product argument in a conversation
  where they are already clearly working on one product, infer the product from
  context but confirm before proceeding.
