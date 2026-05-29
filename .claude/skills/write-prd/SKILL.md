---
description: Write a Product Requirements Document using opinionated per-section templates. Forces falsifiable hypotheses and measurable success metrics. Hydrates from data/ before writing.
---

# Write PRD

Produces a PRD with explicit templates for every section. Each section requires specific content (not generic prompts), so the output is decision-ready, not a thinking exercise.

## Before Starting — Self-Hydration

1. Identify the current product (read host repo's CLAUDE.md for Repo Identity, or ask the user).
2. Read:
   - Grep `context/product/decisions.md` for `status:Active` and `type:Scope`, `type:Positioning`, or `type:Architecture` (last 90 days). Open the 3–6 most relevant H2 blocks.
   - Grep `context/users/personas.md` for H2 headings; read the primary persona block.
   - `tasks/active.md` — top 10 items from Now → Next → Later sections.
   - Grep `context/users/feedback.md` for entries from the last 30 days (`type:"User Feedback"`).
   - Grep `context/market/signals.md` for entries from the last 30 days (`type:"Technical Constraint"`).
   - If `context/learnings/write-prd.md` exists, read the top 3–5 H3 entries. Apply silently to this run — do not narrate prior lessons back to the user.
3. Summarize context briefly to the user before proceeding: *"Writing PRD for {product}. Persona: {name}. Active constraints: {list}. Recent user feedback: {summary}. Proceed?"*

If `context/users/personas.md` is empty or `context/product/decisions.md` has no Active decisions, halt and say so — do not write a PRD without grounded context. Suggest running `/define-persona` or capturing prior decisions first.

## PRD Structure — Per-Section Templates

### 1. Problem Statement

**Template:**
> {Persona name} currently {current behavior/workaround} when they need to {job-to-be-done}. This is painful because {specific cost — time / money / missed outcome}. We know this because {evidence: cite 2+ specific Signals rows OR a KB research entry OR quantified user data}.

**Rules:**
- Must cite at least 2 signal anchors from `context/users/feedback.md` or `context/market/signals.md`, or 1 research section from `context/users/research.md`. If you can't, the problem isn't validated — flag this in the PRD and propose discovery before build.
- Cite signals by anchor (e.g. `context/users/feedback.md#three-tasks-missed-2026-03-02`) and research by file path + H2 heading.
- "This is painful because" must name a concrete cost, not a feeling.

### 2. Hypothesis

**Template:**
> **We believe** {persona} will {specific action — not "engage" or "use"} {measurable frequency} **because** {evidence-backed reason}.
>
> **Riskiest assumption:** {the single assumption that, if wrong, kills the bet}.
>
> **Falsified if** {specific metric} {threshold — number + direction} after {duration — days or weeks from launch}.

**Example:**
> We believe solo PMs will run `/weekly-review` every Monday because they already have the habit of a Monday review but lack structured tooling.
>
> Riskiest assumption: the Monday-review habit is widespread enough to matter (not just my own habit).
>
> Falsified if weekly active users < 30% of signups after 3 weeks.

### 3. Proposed Solution

**Template:**
- **What it is (one sentence):** {X that lets {persona} do {job} in {time}}.
- **Core user flow:** Entry → {action 1} → {action 2} → Completion. Target ≤ 5 steps.
- **In scope (v1):** {bullet list, max 5 items}.
- **Out of scope (v1):** {explicit list of things you considered and cut, with one-line rationale each}.
- **Prior decisions that constrain this:** {cite decision H2 anchors from `context/product/decisions.md`, e.g., `context/product/decisions.md#mobile-first-only-2026-02-14` — "Mobile-first only — excludes desktop flow."}

**Rules:**
- "Out of scope" must be non-empty. If there's nothing you cut, you haven't scoped hard enough.
- Max 5 in-scope items. If more, split the PRD.

### 4. Success Metrics

**Template:**
- **North Star:** {single metric} — must hit {threshold — number} by {horizon — days/weeks post-launch}.
- **Secondary (max 3):**
  - {metric}: {threshold} by {horizon}. Measured via {source}.
  - {metric}: {threshold} by {horizon}. Measured via {source}.
- **Good enough for v1:** {minimum bar to call v1 a success — usually 60–70% of North Star target}.

**Rules:**
- North Star must be an outcome metric (activation, retention, revenue), not an output metric (signups, page views).
- Every metric must specify its measurement source (analytics tool, in-app telemetry, user survey).
- "Good enough" protects against gold-plating v1.

### 5. Technical Context

**Template:**
- **Stack:** {from CLAUDE.md — "already uses X, Y, Z"}.
- **New dependencies this introduces:** {list + reason for each, or "none"}.
- **Known constraints:** {cite Technical Constraint signals from `context/market/signals.md` by anchor, or "none flagged"}.
- **Cost-per-user estimate (if AI/infra heavy):** ${X}/user/month at 100 MAU, ${Y} at 1K, ${Z} at 10K. If unknown, flag for systems-architect consultation.
- **Integration points:** {external systems, APIs, data stores touched}.

### 6. Open Questions & Risks

**Template:**

| # | Type | Item | Mitigation / Discovery Needed |
|---|---|---|---|
| 1 | Question | {unresolved item} | {who answers / what experiment resolves it} |
| 2 | Risk | {specific risk} | {mitigation OR "accept — low impact"} |

**Rules:**
- Each question must have a named owner OR a discovery activity (interview, prototype, spike).
- Each risk must be actioned (mitigate) or explicitly accepted. "We'll see" is not an answer.
- If the list is empty, you haven't thought hard enough — the user will ask what could go wrong.

## Output

Save the PRD to `docs/prd-{feature-slug}.md` in the consumer repo. Confirm the file path with the user before writing.

Output format:
```
## PRD Saved

**File:** docs/prd-{feature-slug}.md
**Product:** {name}
**Problem evidence:** {N signals / M KB entries cited}
**Riskiest assumption:** {one sentence}
**North Star:** {metric + threshold + horizon}
**In-scope items:** {N} — **Out-of-scope items:** {M}
**Open questions:** {N} — **Risks:** {M}
```

## Capture Learning

After delivering the PRD, append one H3 entry to `context/learnings/write-prd.md` (create with `# Learnings — write-prd` H1 if missing). Newest first. Mark `session:pending` — `/context-sync` will reconcile.

```markdown
### {one-line headline of what made this run distinctive} {#headline-slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD skill:write-prd session:pending -->

**Worked:** {one sentence}.
**Missed:** {one sentence}.
**Next time:** {one adjustment}.
```

Keep entries three lines, not three paragraphs.

## Worked Example — Excerpts

**Problem Statement (for `/weekly-review` SaaS):**
> Solo PMs managing 2+ products currently stitch together Notion views, Linear filters, and memory when doing their weekly review. This is painful because it takes 45–90 minutes every Monday AND features slip through the cracks (cited: `context/users/feedback.md#three-tasks-missed-2026-03-02` Internal Learning, `context/users/feedback.md#forgot-competitor-move-2026-03-15` User Feedback). We know this because 4 of 5 interviewed solo PMs described a similar workaround.

**Hypothesis:**
> We believe solo PMs with 2+ products will run a hosted `/weekly-review` every Monday because they already block Monday time for review but hate the manual aggregation.
>
> Riskiest assumption: the Monday-review habit is common enough (not a Jesper-only habit) to support ≥30 early users.
>
> Falsified if WAU < 30% of signups by week 3 post-launch.

**Success Metrics:**
- **North Star:** D7 retention ≥ 40% by 4 weeks post-launch (measured via signup-to-second-review tracking in app).
- **Secondary:**
  - Activation: 70% of signups complete first review within 3 days (measured via app analytics).
  - Setup time: median < 10 minutes from signup to first review (measured via session logs).
- **Good enough for v1:** D7 retention ≥ 25%, activation ≥ 50%.

## Follow-ups

Contextual to what the PRD surfaced:

- Problem section cited no Signals → suggest `/log-signal` to capture user feedback before building, OR running user interviews.
- Risky assumption is buildable-to-test → suggest `/design-experiment` to frame the validation test.
- PRD is scoped → suggest `/break-down` to decompose into kanban-ready tasks.
- PRD introduces AI or expensive infra → consult **systems-architect** for cost model.
- PRD represents a new product bet → suggest `/evaluate-opportunity` before committing.
