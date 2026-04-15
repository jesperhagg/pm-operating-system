---
description: Guided kill-or-park workflow for a product, feature, or bet that isn't working. Captures the lesson, logs the decision, and cleans up memory so the portfolio stays honest.
---

# Sunset Product

Killing or parking a bet is emotionally expensive — which is why solo-founder portfolios drift and dead products linger. This skill makes the closing ritual cheap: final retro, logged decision, migrated signals, clean memory. No debate about whether to kill — you've already decided. This structures the closing move.

## When to Use

- A product/feature/bet is below its Kill threshold (from `/design-experiment` or a PRD).
- A bet has been Pending-Outcome for 60+ days with no traction signal.
- You've decided to park something and want to leave a trail for a future revisit.
- `/memory-review` surfaced stale bets you haven't formally closed.

If you're NOT sure it should be killed: stop and run `/evaluate-opportunity` or `/design-experiment` first. This skill assumes the kill call is made.

## Before Starting — Self-Hydration

1. Identify which product/bet is being sunset (read host repo's CLAUDE.md for active products, or ask).
2. Use Notion MCP to fetch:
   - The original Decision that launched this bet (Type: Go-to-Market or Scope)
   - All Signals linked to this product (last 180 days)
   - Any PRDs or Experiments tied to it (Decisions referencing the product)
   - Active tasks in the backlog tagged to this product
3. Briefly recap to the user: *"Sunsetting {product}. Launched {date} via Decision '{title}'. {N} signals, {M} active tasks, {K} related decisions on file. Confirm kill or park?"*

If Notion MCP is unavailable, halt and say so — sunsetting without the trail produces lost lessons.

## Step 1 — Classify the Exit

Ask the user (if not already stated):

| Exit type | When to use | What happens |
|---|---|---|
| **Kill** | Bet failed its hypothesis. No plan to revisit. | Full archival. Decision logged as Kill. Signals archived. Tasks deleted or reassigned. |
| **Park** | Bet didn't work *now* but the thesis might hold later (market not ready, wrong wedge, etc.). | Decision logged as Park with explicit revisit trigger. Signals archived but tagged. Tasks closed but context saved. |
| **Graduate** | Bet succeeded and is being absorbed into another product / rolled into core offering. | Decision logged as Graduate. Signals and context migrated to the absorbing product. |

Default to Kill unless the user articulates a real revisit trigger or absorption target.

## Step 2 — Final Outcome Assessment

Capture the post-mortem in 5 sentences max. Do not let this sprawl into a retrospective document.

**Template:**
> **Hypothesis:** {what we believed}
> **Actual outcome:** {what happened — with numbers if available}
> **Why it didn't work (or why we're parking):** {root cause — be blunt, no hedging}
> **What we learned:** {the one durable takeaway — transferable to future bets}
> **What would need to change to revisit (Park only):** {specific trigger: market shift, new capability, different persona, price point change}

Rules:
- "Actual outcome" must cite numbers if any exist (signups, retention, revenue, user feedback count). If none exist — say so. That is itself a finding.
- "What we learned" must be something you *didn't* know before this bet. If the lesson is "we should have done more user research," the retro is too shallow — push harder on the root cause.
- No blaming external factors without evidence. "Market wasn't ready" needs a specific data point.

## Step 3 — Log the Decision

Create a Notion Decision entry via `/log-decision` logic (do not re-ask questions already answered):

- **Type:** Kill / Park / Graduate
- **Title:** `{Verb} {product}: {one-line reason}` (e.g., "Kill weekly-review SaaS: signup rate 1.2% vs. 8% threshold")
- **Date:** today
- **Outcome:** Invalidated (Kill), Pending (Park — until revisit trigger fires), Validated (Graduate)
- **Body:** The 5-sentence retro from Step 2.
- **Links:** Original launch Decision, any related Experiments, any related PRDs.

For **Park**, also set:
- **Revisit trigger:** the specific condition from Step 2.
- **Next review date:** today + 6 months (or user-specified).

## Step 4 — Log the Lesson as a Signal

Create a **Signal** entry (Type: Internal Learning) with:
- **Title:** the one durable takeaway from Step 2
- **Description:** 1–2 sentences of context (what bet produced this learning, why it's transferable)
- **Action Required:** false (this is a lesson, not a to-do)
- **Linked Decision:** the Kill/Park/Graduate Decision from Step 3

This is the single most valuable output of sunsetting. A killed bet with no recorded learning is wasted tuition.

## Step 5 — Clean Up Memory

Execute in this order (confirm each batch before moving on):

1. **Active Signals tied to this product:**
   - Kill → Archive via Notion MCP (Status: Archived). Do not delete.
   - Park → Archive, but add tag `parked-{product-slug}` so they resurface on revisit.
   - Graduate → Reassign Product field to the absorbing product.

2. **Active tasks in backlog:**
   - Kill → Delete or mark Abandoned (per host repo convention).
   - Park → Close with note "Parked with {product} on {date} — see Decision {link}."
   - Graduate → Reassign to absorbing product.

3. **Prior Pending-Outcome Decisions for this product:**
   - Update Outcome field now that you have the resolution: mostly Invalidated (Kill), some may be Validated if partial wins informed the learning.

4. **Knowledge Base entries specifically about this product:**
   - Kill → Update Status to Archived. Keep the content — it's history.
   - Park → Keep active but add note "Related to parked bet: {product}."
   - Graduate → Retag to the absorbing product.

5. **Local shared memory (`.claude/memory/shared.md`), if present:**
   - Remove any active cross-agent learnings that only applied to this product.
   - Move them to `.claude/memory/shared-archive.md` under `## Archived — {date} — {product} sunset`.

## Step 6 — Calendar the Revisit (Park only)

For Park exits, tell the user the specific next action:
> *"Set a calendar reminder for {today + 6 months}: 'Review park trigger for {product}: {revisit trigger}'. The Decision Outcome stays Pending until then."*

For Kill exits: no follow-up. The lesson is logged. Move on.

## Output

```
# Sunset — {product} — {Kill / Park / Graduate} — {date}

## Retro
- Hypothesis: {...}
- Actual outcome: {...}
- Why: {...}
- Learned: {...}
{Park only: Revisit trigger: {...}}

## Logged
- Decision: "{title}" (Type: {Kill/Park/Graduate}, Outcome: {Invalidated/Pending/Validated})
- Signal (Internal Learning): "{one-sentence lesson}"

## Cleaned
- Signals archived: {N} {Park: "(tagged parked-{slug})"}
- Tasks closed: {M}
- Prior Pending Decisions resolved: {K}
- KB entries archived/retagged: {J}
- Local memory pruned: {yes/no}

## Next
{Kill: "Done. Lesson logged. Move on."}
{Park: "Revisit trigger on calendar: {date} — {trigger}."}
{Graduate: "Context migrated to {absorbing-product}. Rerun /tasks to see merged backlog."}
```

## Worked Example

**Product:** Hosted `/weekly-review` SaaS (fake-door landing page experiment).

**Retro:**
- **Hypothesis:** Solo PMs with 2+ products would sign up for a hosted weekly-review tool because their manual process takes 45–90 minutes every Monday.
- **Actual outcome:** 312 unique visitors over 14 days across 3 communities, 4 signups (1.3% signup rate vs. 8% Ship threshold, 2% Kill threshold).
- **Why it didn't work:** Pain is real but not acute enough to pay for a separate tool — most respondents said they'd use a Notion template before paying for hosted. Price-to-pain ratio is off.
- **What we learned:** For solo-PM tooling, the wedge has to be "I couldn't do this at all" not "I could do this faster." Faster-but-still-possible doesn't clear the indie-maker willingness-to-pay bar.

**Logged:**
- Decision: *"Kill hosted /weekly-review SaaS: signup rate 1.3% vs. 8% threshold"* (Type: Kill, Outcome: Invalidated)
- Signal (Internal Learning): *"Solo-PM tooling wedge must be 'impossible without tool' not 'faster with tool' — WTP bar is high."*

**Cleaned:**
- 8 signals archived
- 2 tasks closed (landing page maintenance, signup monitoring)
- 1 Pending Decision resolved (launch decision from 2026-04-15)
- 0 KB entries (nothing had been written yet)
- Local memory: removed 1 cross-agent learning about Carrd setup

**Next:** Done. Lesson logged. Move on.

## Anti-Patterns

Reject or redirect these:

- **Soft kills ("paused indefinitely")** — pick Kill or Park with a revisit trigger. Limbo is worse than either.
- **Retro without numbers** — if you can't cite data, say so explicitly. Don't fabricate reasons.
- **Blaming the market without evidence** — "users didn't get it" usually means "the pitch was wrong." Be honest about which.
- **Vague Park triggers** — "when the time is right" isn't a trigger. "When we have 100+ active plugin users" is.
- **Skipping the Signal** — if you don't capture the lesson, the next bet will repeat this one's mistake.

## Follow-ups

Contextual to the exit type:

- **Kill** with a clear replacement idea → `/evaluate-opportunity` for the replacement before committing.
- **Park** with a revisit trigger → log the trigger as a monitoring item; `/pm-digest` or `/market-scan` should surface it when conditions change.
- **Graduate** → `/break-down` to reshape the absorbing product's backlog with migrated context.
- Multiple products sunset in a row → suggest `/memory-review` to catch related stale entries you haven't closed.
- Killed due to cost/unit-economics → consult **systems-architect** before the next bet.
- Killed due to distribution failure → consult **growth-engineer** before the next bet.
