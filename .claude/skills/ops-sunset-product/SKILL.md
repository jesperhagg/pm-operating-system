---
description: Guided kill-or-park workflow for a product or bet that isn't working. Captures the lesson, logs the decision, and archives the trail so the portfolio stays honest.
---

# Sunset Product

Killing or parking a bet is emotionally expensive — which is why solo-founder portfolios drift and dead products linger. This skill makes the closing ritual cheap: final retro, logged decision, migrated signals, clean context layer. No debate about whether to kill — you've already decided. This structures the closing move.

## When to Use

- A product / bet is below its Kill threshold (from `/disc-design-experiment` or a PRD).
- A bet has been `outcome:Pending` for 60+ days with no traction signal.
- You've decided to park something and want to leave a trail for a future revisit.
- `/ctx-context-sync` surfaced a stale bet in governance tasks with no recent activity.

If you're NOT sure it should be killed: stop and run `/strat-evaluate-opportunity` or `/disc-design-experiment` first. This skill assumes the kill call is made.

**One product per repo.** Sunsetting a repo-level product means archiving this repo's `context/` trail. If you're sunsetting a *feature* (not the whole product), scope the cleanup to signals, decisions, and tasks specifically tagged to that feature — the repo itself stays active.

## Before Starting — Self-Hydration

1. Identify what's being sunset — the whole product (this repo) or a specific feature. Ask if ambiguous.
2. Read:
   - `CLAUDE.md` — confirm repo identity and original bet framing.
   - Grep `context/product/decisions.md` for the original launch H2 block and any related experiments.
   - Grep `context/market/signals.md` and `context/users/feedback.md` for the full last 180 days of entries related to the scope.
   - `tasks/active.md` — identify active tasks tied to this scope.
   - Grep `context/product/decisions.md` for `outcome:Pending` entries about to be resolved.
3. Briefly recap: *"Sunsetting {scope}. Launched {date}. {N} signals, {M} active tasks, {K} related decisions. Confirm Kill, Park, or Graduate?"*

If `context/` is empty, halt — there's nothing to sunset or archive.

## Step 1 — Classify the Exit

| Exit type | When to use | What happens |
|---|---|---|
| **Kill** | Bet failed its hypothesis. No plan to revisit. | Full archival. Decision logged. Signals moved to archive. Tasks closed. |
| **Park** | Bet didn't work *now* but thesis might hold later. | Decision logged with revisit trigger. Signals archived but referenced. Tasks closed with note. |
| **Graduate** | Bet succeeded; absorbed into another product. | Decision logged. Context migrated to absorbing repo. |

Default to Kill unless the user articulates a real revisit trigger or absorption target.

## Step 2 — Final Outcome Assessment

Capture the post-mortem in 5 sentences max.

**Template:**
> **Hypothesis:** {what we believed}
> **Actual outcome:** {what happened — with numbers if available}
> **Why it didn't work (or why we're parking):** {root cause — be blunt}
> **What we learned:** {the one durable takeaway — transferable to future bets}
> **What would need to change to revisit (Park only):** {specific trigger}

Rules:
- "Actual outcome" must cite numbers if any exist. If none — say so.
- "What we learned" must be something you *didn't* know before this bet.
- No blaming external factors without evidence.

## Step 3 — Log the Decision

Use `/strat-log-decision` logic to append a new H2 block to `context/product/decisions.md`:

- **Type:** `Kill/Park`
- **Title:** `{Verb} {scope}: {one-line reason}`
- **Date:** today
- **Status:** `Active`
- **Outcome:** `Invalidated` (Kill), `Pending` (Park), `Validated` (Graduate)
- **Body sections:** Context (the bet framing), Impact (what sunsetting means for the portfolio), Outcome Notes (the 5-sentence retro from Step 2).
- **linked_decision:** anchor to the original launch decision H2.
- **linked_signals:** anchors for the key evidence signals.

For **Park**, also include in the Outcome Notes:
- **Revisit trigger:** the specific condition from Step 2.
- **Next review date:** today + 6 months.

## Step 4 — Log the Lesson as a Signal

Append a new H3 to the top of `context/market/signals.md` (via `/gtm-log-signal` logic):

```markdown
### {One durable takeaway from Step 2} {#takeaway-slug-YYYY-MM-DD}
<!-- date:{today} type:"Internal Learning" source:"sunset retro — {scope}" action_required:false linked_decision:"context/product/decisions.md#{kill-decision-anchor}" session:pending -->

**Implication:** {1–2 sentences on why this is transferable to future bets.}
```

This is the single most valuable output of sunsetting. A killed bet with no recorded learning is wasted tuition.

## Step 5 — Clean Up the Context Layer

Execute in this order (confirm each batch before moving on):

1. **Active Signals tied to this scope:**
   - Kill → Move H3 blocks from `context/market/signals.md` and `context/users/feedback.md` to `context/market/archive/signals-YYYY-QN.md`.
   - Park → Leave in active files until quarterly rollover; ensure `linked_decision` points to the Park decision.
   - Graduate → Copy relevant H3 blocks to the absorbing repo's signal files.

2. **Active tasks in backlog:**
   - Kill / Park → Move lines from `tasks/active.md` to `tasks/done.md`, appending ` done:{today} sunset:"{decision-anchor}"` to the metadata comment. Change `[ ]` to `[x]`.
   - Graduate → Move task lines to the absorbing repo's `tasks/active.md`.

3. **Prior Pending-Outcome Decisions for this scope:**
   - Grep `context/product/decisions.md` for `outcome:Pending` H2 blocks in this scope.
   - Update each block's inline metadata: set `outcome:Invalidated` (Kill), `outcome:Validated` (Graduate), or leave Pending (Park). Add `outcome_date:{today}`. Append notes to the `### Outcome Notes` section.

4. **Knowledge / strategy entries specifically about this scope:**
   - Kill → Add a note in the relevant section of `context/product/strategy.md` or `context/users/research.md` referencing the Kill decision.
   - Park → Leave active; add a note referencing the Park decision and revisit trigger.
   - Graduate → Move relevant sections to the absorbing repo.

5. **Personas tied to this scope:**
   - Kill → Add a `<!-- status:archived reason:"sunset {scope}" -->` comment to the persona H2 block in `context/users/personas.md`.
   - Park / Graduate → Leave active.

6. **Local shared memory (`.claude/memory/shared.md`), if present:**
   - Remove active cross-agent learnings that only applied to this scope.
   - Move them to `.claude/memory/shared-archive.md` under `## Archived — {date} — {scope} sunset`.

## Step 6 — Calendar the Revisit (Park only)

> *"Set a calendar reminder for {today + 6 months}: 'Review park trigger for {scope}: {revisit trigger}'. The Park decision stays `outcome:Pending` until then."*

For Kill exits: no follow-up. The lesson is logged. Move on.

## Step 7 — Repo-Level Archival (whole-product Kill only)

- Suggest the user archive the repo on GitHub (manual action — do not execute without confirmation).
- Prompt: *"Want to update `CLAUDE.md` with a `SUNSET` banner noting the kill date and link to the Kill decision anchor?"*

## Output

```
# Sunset — {scope} — {Kill / Park / Graduate} — {date}

## Retro
- Hypothesis: {...}
- Actual outcome: {...}
- Why: {...}
- Learned: {...}
{Park only: Revisit trigger: {...}}

## Logged
- Decision: context/product/decisions.md#{kill-anchor}
- Signal (Internal Learning): "{one-sentence lesson}" → context/market/signals.md

## Cleaned
- Signals archived: {N}
- Tasks closed: {M}
- Prior Pending Decisions resolved: {K}
- Knowledge / strategy sections noted: {J}
- Personas archived: {P}
- Local memory pruned: {yes/no}

## Next
{Kill: "Done. Lesson logged. Move on."}
{Park: "Revisit trigger on calendar: {date} — {trigger}."}
{Graduate: "Context migrated to {absorbing-repo}. Run /ops-tasks there to see the merged backlog."}
```

## Anti-Patterns

- **Soft kills ("paused indefinitely")** — pick Kill or Park with a revisit trigger.
- **Retro without numbers** — if you can't cite data, say so explicitly.
- **Blaming the market without evidence** — "users didn't get it" usually means "the pitch was wrong."
- **Vague Park triggers** — "when the time is right" isn't a trigger.
- **Skipping the Signal** — if you don't capture the lesson, the next bet will repeat this mistake.

## Follow-ups

- **Kill** with a clear replacement idea → `/strat-evaluate-opportunity`.
- **Park** with a revisit trigger → `/ops-pm-digest` or `/gtm-market-scan` should surface it when conditions change.
- **Graduate** → `/disc-break-down` to reshape the absorbing product's backlog.
- Multiple bets sunset in a row → `/ctx-context-sync` to ensure the context layer is consistent.
- Killed due to cost/unit-economics → consult **systems-architect** before the next bet.
- Killed due to distribution failure → consult **growth-engineer** before the next bet.
