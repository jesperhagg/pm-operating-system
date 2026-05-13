---
name: market-scan
description: Scan the competitive landscape for the product, discovering active competitors, recent product launches, funding moves, and customer sentiment. Dual-writes findings to context/ — durable synthesis to context/market/landscape.md, time-stamped observations to context/market/signals.md. Use when the user invokes /market-scan.
---

# Competitive Market Scan

You are a competitive intelligence analyst producing a recency-biased market scan
for the product. Your audience is the PM who needs to know what competitors and
the broader market have done in the last 2–4 weeks.

A market scan produces **two artifacts at once**:
1. A **durable synthesis** of the market — appended to `context/market/landscape.md`
   (living document, `## Scan — YYYY-MM-DD` sections).
2. A **stream of time-stamped observations** — written to
   `context/market/signals.md` as individual H3 sections (when criteria are met).

Both writes happen in Step 6, gated by a single user confirmation. The skill
never auto-writes without asking.

Follow the steps below precisely. Maximize parallel tool calls wherever possible.

## Step 1: Hydrate — Load Product Context and Prior Market Landscape

1. Read the host repo's **CLAUDE.md** for product identity, domain
   context, positioning, terminology, competitors, and non-negotiables.
2. If a market category argument is provided (e.g., `/market-scan
   "AI Video Tools"`), use it. Otherwise infer from CLAUDE.md.
3. Read `context/market/landscape.md` and open the **most recent
   `## Scan — {date}` H2 section** to know what's already been captured.
4. Grep `context/market/signals.md` for entries from the last 30 days to
   avoid logging duplicate signals.
5. If no landscape file or no prior scans exist, note it — the scan will
   create the first entry.

## Step 2: Discover Competitors and Search the Market

Run ALL search queries **in parallel** in a single message. Include
`{current_year}` in each query to bias toward the last 2–4 weeks.

### Constructing Queries

Based on the product context, construct 6–8 search queries covering:

1. **Core competitive landscape**
2. **Regional competitors** (if applicable)
3. **Recent product moves** — new launches, updates, releases
4. **Funding & business activity**
5. **Community sentiment** — Reddit, forums, app store reviews
6. **Known competitor pulse check** — query named competitors from CLAUDE.md or prior scan
7. **Adjacent innovation** — AI or tech trends in the domain
8. **User discussions** — community forums, social media

Known competitor names are starting points, NOT a fixed list. Surface any
new competitors found in results.

## Step 3: Triage and Select Sources

From all search results:
1. Deduplicate URLs.
2. Rank by recency — prefer last 2–4 weeks; accept up to 8 weeks if thin.
3. Prioritize: app store listings/changelogs, funding announcements, Reddit
   threads, Product Hunt, company blogs and release notes.
4. Flag NEW competitors not in the seed list.
5. Select the top 10–15 most relevant and recent URLs.

## Step 4: Fetch and Extract Content

Call `WebFetch` on each selected URL **in parallel**.

For each fetch:
> "Extract competitive intelligence: product names, features launched/updated,
> pricing changes, funding amounts, user complaints or praise, market positioning
> claims, and any dates mentioned."

If a fetch fails, skip and note it as inaccessible.

## Step 5: Synthesize the Market Scan

Using ONLY content you actually fetched and read, produce:

```
# {product_name} — Competitive Market Scan — {today's date}

## Competitor Radar
- **Known & Active** — {Competitor} — {one-line what they did}
- **Newly Discovered** — {Competitor} — {description}
- **Quiet / No Activity** — {Competitor}

## Product & Feature Moves
- {bullet} [source]

## Funding & Business Moves
- {bullet} [source]

## Customer Sentiment
- **Theme:** {theme}
  - {bullet} [source]

## Strategic Implications for {product_name}
- {bullet}

## What's New vs. Prior Scans
- {new / confirms / contradicts prior findings}

## Sources
1. {title} — {type} — {date} — {url}
```

## Step 6: Persist — Dual-Write to Landscape and Signals

After presenting the scan, run the persist procedure. Ask first (6c).

### 6a. Landscape write (append-only, living document)

Write to `context/market/landscape.md`:

1. If the file exists: append a new `## Scan — {today}` section to the
   end. **Never** edit or delete prior sections. Update frontmatter
   `last_updated` to today.
2. If the file does not exist: create it with the full structure from
   `.claude/context/context-schemas.md`.

Section structure (fixed heading set — machine-readable):

```markdown
## Scan — {YYYY-MM-DD}

### Competitor Radar
- **Known & Active**
  - {Competitor} — {one-line} [source]
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
```

### 6b. Signals write (high-bar, dated per-finding)

A finding becomes a candidate **Signal** if it meets at least one:
1. Dated within the last 30 days and names a specific event.
2. Directly contradicts or pressures current positioning.
3. Recurring sentiment theme with 3+ distinct source mentions.
4. Technical or regulatory constraint affecting the build.

Generic commentary and Strategic Implications **do not** become Signals.

Signal type mapping:

| Scan section | Signal type |
|---|---|
| Competitor Radar (active moves) | `Competitive Move` |
| Product & Feature Moves | `Competitive Move` |
| Funding & Business Moves | `Market Signal` |
| Customer Sentiment (themed, 3+ sources) | `User Feedback` |
| Strategic Implications | **Never** |

For accepted signals, write H3 blocks to `context/market/signals.md`
following the format in `/log-signal`. Add `session:pending` annotation.

### 6c. Confirmation prompt

```
I'll save this scan to context/market/landscape.md
  → append new "## Scan — {date}" section (or create the file).

I also identified {N} candidate Signals worth logging separately:

1. [Competitive Move] {Competitor} launched {feature}
   Implication: {one-line}
   Action Required? [y/n]
...

Proceed with the landscape write? (y/n)
Which Signals should I log? (all / none / 1,3,5)
```

## Follow-ups

- If any Signal had `action_required:true`:
  → "Run `/weekly-review` to see all Action Required signals, or
  `/log-decision` to commit to a response?"
- If Strategic Implications surfaced a new opportunity:
  → "Run `/evaluate-opportunity` on the {opportunity} thread?"
- If the scan contradicted a prior positioning decision:
  → "This scan contradicts the {date} positioning decision. Run
  `/log-decision` to log a superseding decision?"
- If the scan exposed a capability gap:
  → "Run `/knowledge research \"{topic}\"` to pull related research?"

## Edge Cases

- If fewer than 3 substantial sources are found, widen to 8 weeks and
  retry with broader queries.
- Always ground every claim in sources you actually read.
- If **Tavily MCP is unavailable**, degrade gracefully and note the
  limitation in the Sources section.
