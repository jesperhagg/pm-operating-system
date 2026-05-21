---
description: Define a customer persona grounded in real evidence — not demographics. Produces a one-pager with job-to-be-done, pain, current workaround, and buying trigger. Used for PRDs, positioning, and targeting. Writes to context/users/personas.md.
---

# Define Persona

Persona work is usually garbage: age, income, "tech-savvy," an avatar photo. None of it changes what you build. This skill produces a persona that *does*: a specific job-to-be-done, the pain behind it, the workaround being used today, and the trigger that makes someone actually buy.

Use this before a PRD, before a positioning exercise, or when a target user has shifted and the team is drifting.

## Before Starting — Self-Hydration

1. Identify the product this persona serves (read host repo's CLAUDE.md, or ask).
2. Read:
   - `context/users/personas.md` — grep for existing H2 persona blocks to refine vs. replace.
   - `context/ops/people.md` — stakeholders to avoid confusing with customer personas.
   - Grep `context/users/feedback.md` for `type:"User Feedback"` entries from the last 90 days.
   - Grep `context/product/decisions.md` for `type:Positioning` or `type:Scope` entries.
   - If `context/learnings/define-persona.md` exists, read the top 3–5 H3 entries. Apply silently to this run — do not narrate prior lessons back to the user.
3. Briefly recap to the user: *"Defining persona for {product}. {N} user-feedback signals, {M} existing personas. Building new, refining existing, or replacing?"*

If `context/users/feedback.md` is empty, halt and say so — a persona without signal evidence is a guess.

## Persona ≠ Stakeholder

This skill defines **customer personas** — who is being sold to / built for. It does NOT define stakeholders (colleagues, investors, partners). For stakeholder notes, use `/knowledge people`.

## Framework — 6 Fields

Every persona has these 6 fields. Fill each one concretely, with evidence. Any field written in generic language defaults to a TODO — don't let it ship.

### 1. Who They Are (in one sentence)

**Template:**
> {Role or situation} who {key defining action/context}.

**Rules:**
- Role + context, not demographics. "Solo PM managing 2+ indie products" is useful. "35-year-old man in tech" is not.
- If the persona could describe 10 million people, tighten it.

### 2. Job-To-Be-Done

**Template:**
> When {situation}, I want to {motivation}, so I can {desired outcome}.

**Rules:**
- "Situation" is a specific trigger moment, not a life stage.
- One primary JTBD per persona. If you have three, you have three personas.

### 3. Pain (with evidence)

**Template:**
> **Cost:** {time / money / missed outcome — quantified}.
> **Frequency:** {daily / weekly / per-event}.
> **Evidence:** {cite ≥2 feedback/signal anchors, or 1 research entry}.

**Rules:**
- Pain must be measured. "It's annoying" doesn't cut it.
- If you can't cite 2+ signals, mark evidence_strength as `Thin`.

### 4. Current Workaround

**Template:**
> Today they {specific process/tools} for {amount of time / cost} because {why it's the least-bad option right now}.

**Rules:**
- Name the tools. "Various tools" is not useful.
- The workaround is your real competitor.

### 5. Buying Trigger

**Template:**
> They'd switch/buy when {specific event / moment of acute pain / status change}.

**Rules:**
- Must be a discrete event, not a vague state.

### 6. Anti-Persona (who this is NOT)

**Template:**
> This is NOT {adjacent persona} because {they have different JTBD / different buying trigger / different price sensitivity}.

## Output

Append a new H2 block to `context/users/personas.md`. If the file does
not exist, create it with a `# Personas` H1 header.

Insert at the **top** of the file (newest first), after the H1 header:

```markdown
## {Short name} {#slug}
<!-- jtbd:"{one-line JTBD}" last_updated:YYYY-MM-DD evidence_strength:{Strong|Moderate|Thin} evidence:[context/users/feedback.md#anchor-1, context/users/feedback.md#anchor-2] session:pending -->

**Who:** {one sentence}

**Job-To-Be-Done:**
When {situation}, I want to {motivation}, so I can {outcome}.

**Pain:**
- Cost: {quantified}
- Frequency: {...}
- Evidence: {anchor refs}

**Current Workaround:**
{tools + time + why}

**Buying Trigger:**
{specific event}

**Anti-Persona (NOT this):**
- {adjacent persona} — {why excluded}

**Discovery gaps:** {list any fields marked TODO, or "none"}

---
```

The `session:pending` annotation marks this as session-written, awaiting
reconciliation by `/context-sync`.

Then return a summary to the user:

```
## Persona Defined

**Name:** {short name}
**Evidence strength:** {Strong ≥5 signals / Moderate 2–4 / Thin <2}
**Appended to:** context/users/personas.md
**Anchor:** #{slug}
**Open gaps:** {any TODOs}
```

## Capture Learning

After delivering the persona, append one H3 entry to `context/learnings/define-persona.md` (create with `# Learnings — define-persona` H1 if missing). Newest first. Mark `session:pending` — `/context-sync` will reconcile.

```markdown
### {one-line headline of what made this run distinctive} {#headline-slug-YYYY-MM-DD}
<!-- date:YYYY-MM-DD skill:define-persona session:pending -->

**Worked:** {one sentence}.
**Missed:** {one sentence}.
**Next time:** {one adjustment}.
```

Keep entries three lines, not three paragraphs.

## Follow-ups

Contextual to what the persona surfaced:

- Evidence is Thin → `/log-signal` after each user interview; run this skill again in 30 days.
- Persona is sharp + product needs specing → `/write-prd` referencing this persona.
- Persona reveals a distribution trigger → consult **growth-engineer**.
- Persona conflicts with existing positioning → `/log-decision` (Type: Positioning).
- Anti-persona is actually the bigger market → `/evaluate-opportunity`.

## Anti-Patterns

- **Demographic padding** — age, income, marital status.
- **"Tech-savvy" as a trait** — replace with the actual workaround.
- **Three JTBDs in one persona** — that's three personas. Split them.
- **No evidence cited** — if Pain has no signals, mark `Thin` and run discovery first.
- **Writing the persona you want** — write what your data shows.
