---
description: Guided kill-or-park workflow for a product or bet that isn't working. Captures the lesson, logs the decision, and archives the trail so the portfolio stays honest.
---

# Sunset Product

Killing or parking a bet is emotionally expensive — which is why solo-founder portfolios drift and dead products linger. This skill makes the closing ritual cheap: final retro, logged decision, migrated signals, clean data layer. No debate about whether to kill — you've already decided. This structures the closing move.

## When to Use

- A product / bet is below its Kill threshold (from `/design-experiment` or a PRD).
- A bet has been `outcome: Pending` for 60+ days with no traction signal.
- You've decided to park something and want to leave a trail for a future revisit.
- `/memory-review` surfaced a stale bet you haven't formally closed.

If you're NOT sure it should be killed: stop and run `/evaluate-opportunity` or `/design-experiment` first. This skill assumes the kill call is made.

**One product per repo.** Sunsetting a repo-level product means archiving this repo's `data/` trail. If you're sunsetting a *feature* (not the whole product), scope the cleanup to signals, decisions, and tasks specifically tagged to that feature — but the repo itself stays active.

## Before Starting — Self-Hydration

1. Identify what's being sunset — the whole product (this repo) or a specific feature inside it. Ask if ambiguous.
2. Read:
   - `CLAUDE.md` — confirm repo identity and original bet framing.
   - `data/decisions/index.md` — open the original launch Decision and any related Experiments / PRDs.
   - Grep `data/signals/active.md` for the full last 180 days of entries related to the scope.
   - `data/tasks/active.md` — identify active tasks tied to this scope.
   - `data/decisions/index.md` — list rows with `outcome: Pending` that are about to be resolved by this sunset.
3. Briefly recap: *"Sunsetting {scope}. Launched {date} via `{decision file}`. {N} signals, {M} active tasks, {K} related decisions on file. Confirm Kill, Park, or Graduate?"*

If `data/` is empty, halt and say so — there's nothing to sunset or no trail to archive.

## Step 1 — Classify the Exit

| Exit type | When to use | What happens |
|---|---|---|
| **Kill** | Bet failed its hypothesis. No plan to revisit. | Full archival. Decision logged as Kill. Signals moved to archive. Tasks moved to done.md as abandoned. |
| **Park** | Bet didn't work *now* but the thesis might hold later. | Decision logged as Park with explicit revisit trigger. Signals archived but referenced. Tasks moved to done with note. |
| **Graduate** | Bet succeeded and is being absorbed into another product / rolled into core offering. | Decision logged as Graduate. Context migrated (ideally via git) to the absorbing repo. |

Default to Kill unless the user articulates a real revisit trigger or absorption target.

## Step 2 — Final Outcome Assessment

Capture the post-mortem in 5 sentences max. Do not let this sprawl.

**Template:**
> **Hypothesis:** {what we believed}
> **Actual outcome:** {what happened — with numbers if available}
> **Why it didn't work (or why we're parking):** {root cause — be blunt, no hedging}
> **What we learned:** {the one durable takeaway — transferable to future bets}
> **What would need to change to revisit (Park only):** {specific trigger: market shift, new capability, different persona, price-point change}

Rules:
- "Actual outcome" must cite numbers if any exist. If none exist — say so. That's itself a finding.
- "What we learned" must be something you *didn't* know before this bet.
- No blaming external factors without evidence.

## Step 3 — Log the Decision

Invoke `/log-decision` logic (do not re-ask questions already answered). Write a file at `data/decisions/{today}-{kill|park|graduate}-{slug}.md`:

- **Type:** `Kill/Park`
- **Title:** `{Verb} {scope}: {one-line reason}` (e.g., "Kill hosted weekly-review SaaS: signup rate 1.3% vs. 8% threshold")
- **Date:** today
- **Status:** `Active` (the Kill/Park decision itself is the current active stance)
- **Outcome:** `Invalidated` (Kill), `Pending` (Park — until revisit trigger fires), `Validated` (Graduate)
- **Body sections:** Context (the bet framing), Impact (what sunsetting means for the portfolio), Outcome Notes (the 5-sentence retro from Step 2).
- **linked_decision:** relative path to the original launch Decision.
- **linked_signals:** relative anchors for the key evidence signals.

For **Park**, also include in the body:
- **Revisit trigger:** the specific condition from Step 2.
- **Next review date:** today + 6 months (or user-specified).

Append the row to `data/decisions/index.md`.

## Step 4 — Log the Lesson as a Signal

Append a new H3 to the top of `data/signals/active.md` (via `/log-signal` logic):

```markdown
### {One durable takeaway from Step 2}
<!-- date:{today} type:"Internal Learning" source:"sunset retro — {scope}" action_required:false linked_decision:"../decisions/{today}-{slug}.md" -->

**Implication:** {1–2 sentences on why this is transferable to future bets.}
```

This is the single most valuable output of sunsetting. A killed bet with no recorded learning is wasted tuition.

## Step 5 — Clean Up the Data Layer

Execute in this order (confirm each batch before moving on):

1. **Active Signals tied to this scope:**
   - Kill → Move H3 blocks from `data/signals/active.md` to `data/signals/archive/YYYY-QN.md`.
   - Park → Leave in `active.md` until the quarterly rollover, but edit the linked_decision to point at the Park decision so they're reachable.
   - Graduate → Move the relevant H3 blocks to the absorbing repo's `data/signals/active.md` (copy-paste; this crosses repo boundaries).

2. **Active tasks in backlog:**
   - Kill / Park → Move lines from `data/tasks/active.md` to `data/tasks/done.md`, appending ` done:{today} sunset:"{decision slug}"` to the metadata comment. Change `[ ]` to `[x]`.
   - Graduate → Move task lines to the absorbing repo's `data/tasks/active.md`.

3. **Prior Pending-Outcome Decisions for this scope:**
   - Open each file. Update frontmatter `outcome:` (usually `Invalidated` for Kill, possibly `Validated` for a partial win) and `outcome_date: {today}`. Append notes to the `## Outcome Notes` section. Update the row in `data/decisions/index.md`.
   - For Kill: also flip `status:` to `Archived` on decisions that are explicitly superseded by the Kill decision.

4. **Knowledge entries specifically about this scope:**
   - Kill → Edit frontmatter `status: archived` on relevant files (keep the content, it's history).
   - Park → Leave `status: active` but add a note referencing the Park decision.
   - Graduate → Move the file to the absorbing repo's `data/knowledge/` (same category).

5. **Personas tied to this scope:**
   - Kill → Edit frontmatter `status: archived` on personas specifically tied to the killed scope.
   - Park / Graduate → Leave active; the persona may outlive the bet.

6. **Local shared memory (`.claude/memory/shared.md`), if present:**
   - Remove any active cross-agent learnings that only applied to this scope.
   - Move them to `.claude/memory/shared-archive.md` under `## Archived — {date} — {scope} sunset`.

## Step 6 — Calendar the Revisit (Park only)

For Park exits, tell the user the specific next action:
> *"Set a calendar reminder for {today + 6 months}: 'Review park trigger for {scope}: {revisit trigger}'. The Park decision stays `outcome: Pending` until then."*

For Kill exits: no follow-up. The lesson is logged. Move on.

## Step 7 — Repo-Level Archival (whole-product Kill only)

If Kill covers the whole repo / product:
- Suggest the user archive the repo on GitHub (manual action — do not execute without confirmation).
- Prompt: *"Want to update the repo's `CLAUDE.md` with a `SUNSET` banner noting the kill date and link to the Kill decision file?"*

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
- Decision: `data/decisions/{file}.md` (Type: {Kill/Park/Graduate}, Outcome: {Invalidated/Pending/Validated})
- Signal (Internal Learning): "{one-sentence lesson}" → `data/signals/active.md`

## Cleaned
- Signals archived: {N}
- Tasks closed: {M}
- Prior Pending Decisions resolved: {K}
- Knowledge entries archived/retagged: {J}
- Personas archived: {P}
- Local memory pruned: {yes/no}

## Next
{Kill: "Done. Lesson logged. Move on."}
{Park: "Revisit trigger on calendar: {date} — {trigger}."}
{Graduate: "Context migrated to {absorbing-repo}. Run /tasks there to see the merged backlog."}
```

## Worked Example

**Scope:** Hosted `/weekly-review` SaaS (fake-door landing page experiment).

**Retro:**
- **Hypothesis:** Solo PMs with 2+ products would sign up for a hosted weekly-review tool because their manual process takes 45–90 minutes every Monday.
- **Actual outcome:** 312 unique visitors over 14 days, 4 signups (1.3% signup rate vs. 8% Ship threshold, 2% Kill threshold).
- **Why:** Pain is real but not acute enough — most respondents said they'd use a Notion template before paying.
- **Learned:** For solo-PM tooling, the wedge has to be "I couldn't do this at all" not "I could do this faster."

**Logged:**
- Decision: `data/decisions/2026-04-20-kill-weekly-review-saas.md` (Type: Kill, Outcome: Invalidated)
- Signal: *"Solo-PM tooling wedge must be 'impossible without tool' not 'faster with tool' — WTP bar is high."*

**Cleaned:**
- 8 signals archived to `data/signals/archive/2026-Q2.md`
- 2 tasks moved to `data/tasks/done.md`
- 1 prior Pending Decision (2026-04-15 launch decision) → Outcome: Invalidated
- 0 KB entries (nothing had been written yet)
- Local memory: removed 1 stale cross-agent learning about Carrd setup

**Next:** Done. Lesson logged. Move on.

## Anti-Patterns

Reject or redirect these:

- **Soft kills ("paused indefinitely")** — pick Kill or Park with a revisit trigger. Limbo is worse than either.
- **Retro without numbers** — if you can't cite data, say so explicitly. Don't fabricate reasons.
- **Blaming the market without evidence** — "users didn't get it" usually means "the pitch was wrong."
- **Vague Park triggers** — "when the time is right" isn't a trigger. "When we hit 500 active plugin users" is.
- **Skipping the Signal** — if you don't capture the lesson, the next bet will repeat this one's mistake.

## Follow-ups

- **Kill** with a clear replacement idea → `/evaluate-opportunity` for the replacement.
- **Park** with a revisit trigger → `/pm-digest` or `/market-scan` should surface it when conditions change.
- **Graduate** → `/break-down` to reshape the absorbing product's backlog with migrated context.
- Multiple bets sunset in a row → `/memory-review` to catch related stale entries.
- Killed due to cost/unit-economics → consult **systems-architect** before the next bet.
- Killed due to distribution failure → consult **growth-engineer** before the next bet.
