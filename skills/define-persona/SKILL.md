---
description: Define a customer persona grounded in real evidence — not demographics. Produces a one-pager with job-to-be-done, pain, current workaround, and buying trigger. Used for PRDs, positioning, and targeting. Writes to data/personas/.
---

# Define Persona

Persona work is usually garbage: age, income, "tech-savvy," an avatar photo. None of it changes what you build. This skill produces a persona that *does*: a specific job-to-be-done, the pain behind it, the workaround being used today, and the trigger that makes someone actually buy.

Use this before a PRD, before a positioning exercise, or when a target user has shifted and the team is drifting.

## Before Starting — Self-Hydration

1. Identify the product this persona serves (read host repo's CLAUDE.md, or ask).
2. Read:
   - `data/personas/index.md` and any existing persona files (to refine vs. replace).
   - `data/knowledge/people/` (stakeholders — to avoid confusing with customer personas).
   - Grep `data/signals/active.md` for `type:"User Feedback"` entries from the last 90 days.
   - `data/decisions/index.md` filtered by `type: Positioning` or `type: Scope`.
3. Briefly recap to the user: *"Defining persona for {product}. {N} user-feedback signals, {M} existing persona files. Building new persona, refining existing, or replacing?"*

If `data/signals/active.md` does not exist, halt and say so — a persona without signal evidence is a guess.

## Persona ≠ Stakeholder

This skill defines **customer personas** — who is being sold to / built for. It does NOT define stakeholders (colleagues, investors, partners). For stakeholder notes, use `/knowledge people`.

## Framework — 6 Fields

Every persona has these 6 fields. Fill each one concretely, with evidence. Any field written in generic language defaults to a TODO — don't let it ship.

### 1. Who They Are (in one sentence)

**Template:**
> {Role or situation} who {key defining action/context}.

**Rules:**
- Role + context, not demographics. "Solo PM managing 2+ indie products" is useful. "35-year-old man in tech" is not.
- If the persona could describe 10 million people, tighten it. Target specificity: ~10K–1M people worldwide.

**Bad:** *"Tech-savvy millennial professional."*
**Good:** *"Solo PM running 2+ indie products alongside a day job."*

### 2. Job-To-Be-Done

**Template:**
> When {situation}, I want to {motivation}, so I can {desired outcome}.

**Rules:**
- "Situation" is a specific trigger moment, not a life stage.
- "Outcome" must be something they'd brag about or feel relief over — not a feature.
- One primary JTBD per persona. If you have three, you have three personas.

**Bad:** *"Manage my products efficiently."*
**Good:** *"When it's Monday morning and I have 3 products to review, I want to see what changed and what's at risk in under 10 minutes, so I can spend my scarce focus time shipping instead of hunting."*

### 3. Pain (with evidence)

**Template:**
> **Cost:** {time / money / missed outcome — quantified}.
> **Frequency:** {daily / weekly / per-event}.
> **Evidence:** {cite ≥2 User Feedback signals by anchor, or 1 research entry}.

**Rules:**
- Pain must be measured: hours per week, $ lost, deals missed. "It's annoying" doesn't cut it.
- Frequency matters: once-a-year pain doesn't justify a weekly SaaS.
- If you can't cite 2+ signals, the pain is assumed not validated — flag `discovery-needed` and mark evidence_strength as `Thin`.

### 4. Current Workaround

**Template:**
> Today they {specific process/tools} for {amount of time / cost} because {why it's the least-bad option right now}.

**Rules:**
- Name the tools. "Notion + Linear + memory + 3 spreadsheets" is useful. "Various tools" is not.
- If you don't know the workaround, your discovery is incomplete — flag it.
- The workaround is your competitor. Beating nothing is impossible; beating Notion-plus-duct-tape is the real bar.

### 5. Buying Trigger

**Template:**
> They'd switch/buy when {specific event / moment of acute pain / status change}.

**Rules:**
- Must be a discrete event, not a vague state. "Starts new company" → event. "Is successful" → state (reject).
- This trigger becomes your targeting signal for distribution. If you can't identify the trigger, you can't target them.

**Bad:** *"When they're ready to scale."*
**Good:** *"When they launch their second product and the Monday review starts slipping past 90 minutes."*

### 6. Anti-Persona (who this is NOT)

**Template:**
> This is NOT {adjacent persona} because {they have different JTBD / different buying trigger / different price sensitivity}.

**Rules:**
- Name 1–2 adjacent personas you'll get confused with and explicitly exclude them.
- If you can't name an anti-persona, the persona is probably too broad.

**Example:** *"This is NOT enterprise PMs because they have internal tooling budgets, political constraints, and a different JTBD (align stakeholders) — not the solo PM's JTBD (prevent drift across their own products)."*

## Output

Write a new file at `data/personas/{slug}.md` (slug derived from the
short name). Append a row to `data/personas/index.md` (create the
index if missing).

**File contents:**

```markdown
---
title: {short name}
jtbd: {one-line JTBD}
last_updated: YYYY-MM-DD
evidence_strength: {Strong | Moderate | Thin}
evidence: [../signals/active.md#anchor-1, ../signals/active.md#anchor-2]
---

# Persona — {short name}

**Who:** {one sentence}

**Job-To-Be-Done:**
When {situation}, I want to {motivation}, so I can {outcome}.

**Pain:**
- Cost: {quantified}
- Frequency: {...}
- Evidence: {Signal anchors}

**Current Workaround:**
{tools + time + why}

**Buying Trigger:**
{specific event}

**Anti-Persona (NOT this):**
- {adjacent persona} — {why excluded}

**Discovery gaps:** {list any fields marked TODO, or "none"}
```

**Index row:**
`| {slug} | {short name} | {evidence_strength} | YYYY-MM-DD |`

Then return a summary to the user:

```
## Persona Defined

**Name:** {short name}
**Evidence strength:** {Strong ≥5 signals / Moderate 2–4 / Thin <2}
**Saved to:** data/personas/{slug}.md
**Index updated:** data/personas/index.md
**Open gaps:** {any TODOs}
```

## Worked Example

**Persona:** Solo Multi-Product PM (for `/weekly-review` SaaS bet)

**Who:** Solo PM running 2+ indie products simultaneously, often alongside a day job or consulting work.

**Job-To-Be-Done:** When it's Monday morning and I have multiple products to review, I want to see what changed, what's at risk, and what's next in under 10 minutes, so I can spend my scarce focus time shipping instead of aggregating status.

**Pain:**
- Cost: 45–90 minutes every Monday on manual aggregation; ~3 tasks/month slip through the cracks.
- Frequency: weekly (the review) + daily low-grade anxiety about what's dropping.
- Evidence: `../signals/active.md#three-tasks-missed-2026-03-02`, `../signals/active.md#forgot-competitor-move-2026-03-15`; 4 of 5 interviewed solo PMs described the same ritual.

**Current Workaround:** Stitching together Notion views, Linear filters, and memory. Takes 60+ minutes. It's the least-bad option because no tool today aggregates across multi-product indie setups.

**Buying Trigger:** Launches a second product AND experiences the first "I forgot something important" incident. Pain shifts from abstract to acute.

**Anti-Persona:**
- Enterprise PMs — different JTBD (align stakeholders), internal tooling, no payment authority.
- Indie solopreneurs with 1 product — Notion works fine for them; the pain is multi-product-specific.

**Evidence strength:** Moderate (4 signals, 1 research entry).
**Discovery gaps:** Need 5+ more interviews to move to Strong.

## Anti-Patterns

Reject or redirect these:

- **Demographic padding** — age, income, marital status. If you wouldn't change the product based on the value, leave it out.
- **"Tech-savvy" as a trait** — everyone claims this. Replace with the actual workaround they use (which tells you what they're already comfortable with).
- **Three JTBDs in one persona** — that's three personas. Split them.
- **No evidence cited** — if the Pain field has no Signals, mark the persona `Thin` and run discovery before it influences decisions.
- **Writing the persona you want** — write the persona your data shows. If the evidence contradicts your pitch, the pitch is wrong, not the data.
- **Copy-pasting "Sarah the Project Manager"** — generic avatars are performative. Name the role + context; skip the photo and bio.

## Follow-ups

Contextual to what the persona surfaced:

- Evidence is Thin → `/log-signal` after each user interview; run this skill again in 30 days.
- Persona is sharp + product needs specing → `/write-prd` referencing this persona file.
- Persona reveals a distribution trigger → consult **growth-engineer** on how to reach them at that trigger moment.
- Persona conflicts with existing positioning → `/log-decision` (Type: Positioning) to resolve the conflict.
- Anti-persona is actually the bigger market → reconsider the bet via `/evaluate-opportunity`.
