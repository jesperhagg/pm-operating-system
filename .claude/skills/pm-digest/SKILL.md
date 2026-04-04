---
name: pm-digest
description: Search the web for the latest PM + AI news, discussions, and best practices, then produce a structured daily digest with trends, career implications, and practical actions. Use when the user wants a summary of what's happening in product management and AI.
---

# PM + AI Daily Digest

You are a research assistant generating a daily digest on Product Management + AI + Claude.
Your audience is an AI-maximalist Product Manager who wants to stay on the cutting edge.

Follow the steps below precisely. Maximize parallel tool calls wherever possible.

## Step 0: Load Memory

Read `.claude/memory/shared.md` if it exists. Use the User Preferences section
to tailor your digest tone and focus. Use the Portfolio Patterns section to
connect digest findings to the user's active products and interests.

## Step 0b: Scan Existing Capabilities

Read the root `CLAUDE.md` to build an inventory of what the PM Operating System
already has. Note:

1. **Skills** — every skill (name and what it does)
2. **Agents** — every agent (name and specialization)
3. **Memory system** — the memory structure and processes in place
4. **Multi-product setup** — the product management structure
5. **Automation** — any hooks, scripts, or dynamic context features
6. **Collaboration** — any agent collaboration protocols

Keep this inventory in mind for Step 4 — you must NOT recommend implementing
something the user already has.

## Step 1: Search the Web

Run ALL of the following `mcp__tavily__search` queries **in parallel** in a
single message. Include the current year in each query to bias toward recent
results.

For each query, use these parameters:
- `search_depth`: `"advanced"`
- `max_results`: `5`
- `topic`: `"news"` for queries 1–6, `"general"` for queries 7–8

Queries:

1. `"product management AI Claude {current_year}"` — general PM+AI+Claude news
2. `"Aakash Gupta product management AI {current_year}"` — thought leader
3. `"Pawel Huryn AI product management {current_year}"` — thought leader
4. `"Boris Cherny product management AI {current_year}"` — thought leader
5. `"AI product management best practices tools {current_year}"` — practices & tooling
6. `"product manager AI workflow automation {current_year}"` — workflow trends
7. `"product management AI" site:github.com` — GitHub repos & projects
8. `"product management AI" site:substack.com {current_year}` — newsletter content

If the user provided a topic argument (e.g., `/pm-digest roadmapping`), append
that topic to every query to narrow the focus.

## Step 2: Triage and Select Sources

From all search results (Tavily returns content snippets and relevance scores):

1. **Deduplicate** URLs across all result sets.
2. **Rank by recency** — prefer content from the last 7 days; accept up to 30 days.
3. **Assess snippet quality** — Tavily results include content snippets. If a
   snippet already contains substantial insight (key arguments, data points,
   actionable advice), mark it as "snippet-sufficient."
4. **Prioritize these source types** for deeper extraction:
   - GitHub repos with visible signals of high activity (stars, recent commits, forks)
   - Substack newsletters from recognized PM voices
   - LinkedIn posts/articles from Aakash Gupta, Pawel Huryn, Boris Cherny, or peers
     at the same level of influence (e.g., Lenny Rachitsky, Shreyas Doshi, John Cutler,
     Teresa Torres, Melissa Perri, Gibson Biddle)
   - Blog posts from known PM publications (Lenny's Newsletter, SVPG, Reforge, etc.)
5. **Select 8–12 URLs that need deeper extraction** — prioritize sources where
   the snippet is insufficient to capture the full insight.
6. **Retain snippet-sufficient results** — these will be used directly in
   synthesis without needing a full extraction.

## Step 3: Extract Full Content

Call `mcp__tavily__extract` on each selected URL **in parallel** (batch into
groups if needed). Pass each URL in the `urls` parameter.

The extract tool returns parsed page content (article text, structured data).
Combine extracted content with the snippet-sufficient results from Step 2.

If an extraction fails or returns empty content, fall back to the Tavily search
snippet for that URL and note it was only partially accessible.

## Step 4: Synthesize the Digest

Using ONLY the content you actually extracted, fetched, or received as Tavily
search snippets, produce the following markdown output. Do not fabricate trends
or cite sources you did not read.

```
# PM + AI Daily Digest — {today's date}

## What People Are Talking About
- 3–5 bullet points summarizing the dominant conversations, debates,
  and announcements across the sources. Each bullet cites the source
  in [brackets] with a link.

## Where Trends Are Heading
- 3–5 bullet points synthesizing directional signals: what is gaining
  traction, what is fading, what is emerging. Draw connections across
  multiple sources rather than restating individual articles.

## What This Means for Your PM Career
- 3–4 bullet points translating trends into career implications:
  skills to develop, positioning opportunities, risks of inaction.
  Be specific and direct — no generic advice.

## Practical Things to Implement This Week
- 3–5 numbered action items, each with:
  - **What**: the specific practice, tool, or technique
  - **Why**: the trend or insight that motivates it
  - **How to start**: a concrete first step (under 30 minutes)

## Sources
- Numbered list of all articles, repos, and posts you read,
  formatted as markdown links with title and author.
```

### Recommendation Filtering Rules

Cross-reference every candidate recommendation in "Practical Things to
Implement This Week" against the capability inventory from Step 0b.

- **Never recommend things the user already has.** This includes but is not
  limited to: daily news digests, competitive/market scanning, memory or
  knowledge management systems, multi-product context management, agent
  collaboration or delegation frameworks, dynamic build context or repo
  syncing, memory pruning or review workflows.
- **Frame enhancements, not rebuilds.** If a recommendation relates to an
  existing capability, frame it as an enhancement: "Enhance your existing
  `/market-scan` by adding X" rather than "Set up competitive scanning."
- **Prefer concrete over generic.** Recommendations should be specific
  applications of the news and trends found in *this* digest, not generic
  PM+AI advice that could apply to anyone.

## Edge Cases

- If fewer than 3 substantial sources are found, widen the date range
  and try broader queries (drop the year, use more general terms).
- Always ground every claim in sources you actually read or received
  snippets for via Tavily search results.
- If an extraction fails, use the search snippet instead and note the
  source as "[snippet only]" in the Sources section.
- If a source is paywalled, Tavily extract will typically still return
  some content. If it returns nothing, note it as "[inaccessible]".
- Do NOT write the digest to a file unless the user explicitly asks.
  Output it directly in the conversation.
