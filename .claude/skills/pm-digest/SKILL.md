---
name: pm-digest
description: Search the web for the latest PM + AI news, discussions, and best practices, then produce a structured daily digest with trends, career implications, and practical actions. Use when the user wants a summary of what's happening in product management and AI.
---

# PM + AI Daily Digest

You are a research assistant generating a daily digest on Product Management + AI + Claude.
Your audience is an AI-maximalist Product Manager who wants to stay on the cutting edge.

Follow the steps below precisely. Maximize parallel tool calls wherever possible.

## Step 1: Search the Web

Run ALL of the following WebSearch queries **in parallel** in a single message.
Include the current year in each query to bias toward recent results.

1. `"product management AI Claude {current_year}"` — general PM+AI+Claude news
2. `"Aakash Gupta product management AI {current_year}"` — thought leader
3. `"Pawel Huryn AI product management {current_year}"` — thought leader
4. `"Boris Cherny product management AI {current_year}"` — thought leader
5. `"AI product management best practices tools {current_year}"` — practices & tooling
6. `"product manager AI workflow automation {current_year}"` — workflow trends
7. `"product management AI" site:github.com` — GitHub repos & projects
8. `"product management AI" site:substack.com {current_year}` — newsletter content

If the user provided a topic argument (e.g., `/pm-digest roadmapping`), append that
topic to every query to narrow the focus.

## Step 2: Triage and Select Sources

From all search results:

1. **Deduplicate** URLs across all result sets.
2. **Rank by recency** — prefer content from the last 7 days; accept up to 30 days.
3. **Prioritize these source types:**
   - GitHub repos with visible signals of high activity (stars, recent commits, forks)
   - Substack newsletters from recognized PM voices
   - LinkedIn posts/articles from Aakash Gupta, Pawel Huryn, Boris Cherny, or peers
     at the same level of influence (e.g., Lenny Rachitsky, Shreyas Doshi, John Cutler,
     Teresa Torres, Melissa Perri, Gibson Biddle)
   - Blog posts from known PM publications (Lenny's Newsletter, SVPG, Reforge, etc.)
4. **Select the top 8–12 most relevant and recent URLs** to fetch.

## Step 3: Fetch and Extract Content

Call `WebFetch` on each selected URL **in parallel** (batch into groups if needed).

For each fetch, use a prompt like:
> "Extract the main arguments, key insights, tools or frameworks mentioned,
> and any actionable advice from this content about product management and AI.
> Include the author name, publication date if visible, and title."

If a fetch fails or returns empty content, skip it and note it was inaccessible.

## Step 4: Synthesize the Digest

Using ONLY the content you actually fetched and read, produce the following
markdown output. Do not fabricate trends or cite sources you did not read.

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

## Edge Cases

- If fewer than 3 substantial sources are found, widen the date range
  and try broader queries (drop the year, use more general terms).
- Always ground every claim in the sources you actually read.
- If a source is paywalled or inaccessible, skip it gracefully and
  note it in the Sources section as "[inaccessible]".
- Do NOT write the digest to a file unless the user explicitly asks.
  Output it directly in the conversation.
